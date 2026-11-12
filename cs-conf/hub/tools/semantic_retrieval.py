#!/usr/bin/env python3
"""Local hybrid retrieval and metadata-only paper comparison for the hub."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import struct
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

HUB_ROOT = Path(__file__).resolve().parents[1]
MODEL_NAME = "BAAI/bge-small-en-v1.5"
DIMENSION = 384
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
BM25_WEIGHTS = (8.0, 4.0, 1.0)  # title, authors, abstract
RRF_K = 60
CHUNK_WORDS = 180
CHUNK_OVERLAP = 40
FORMAT = "cs-conference-semantic-index-v1"


def default_index_dir() -> Path:
    override = os.environ.get("CS_CONF_HUB_INDEX_DIR")
    if override:
        return Path(override).expanduser()
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "cs-conference-hub" / "semantic-index"
    return Path.home() / ".cache" / "cs-conference-hub" / "semantic-index"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _private_index_path(index_dir: Path, hub_root: Path) -> Path:
    path = index_dir.expanduser().resolve()
    root = hub_root.resolve()
    if path == root or root in path.parents:
        raise ValueError("The semantic index must be outside the hub repository; use the local cache path.")
    return path


def catalog_shards(hub_root: Path = HUB_ROOT) -> Tuple[str, str, List[dict]]:
    root = hub_root.resolve()
    catalog_path = root / "catalog.json"
    raw = catalog_path.read_bytes()
    catalog = json.loads(raw)
    if catalog.get("schema") != "cs-conf-catalog-v1" or not isinstance(catalog.get("venues"), dict):
        raise ValueError("catalog.json has an unsupported schema")
    shards = []
    for venue in sorted(catalog["venues"]):
        metadata = catalog["venues"][venue]
        for year in sorted(metadata.get("available_years", [])):
            entry = metadata.get("years", {}).get(str(year))
            if not isinstance(entry, dict) or not entry.get("file"):
                raise ValueError("catalog.json is missing a shard entry for {} {}".format(venue, year))
            path = (root / entry["file"]).resolve()
            if root not in path.parents:
                raise ValueError("catalog shard path escapes the hub directory: {}".format(entry["file"]))
            shards.append({
                "venue": venue,
                "year": int(year),
                "entry": entry,
                "path": path,
                "catalog_source_url": catalog.get("source_dataset", ""),
            })
    return str(catalog_path), sha256_bytes(raw), shards


def read_shard(spec: dict) -> Tuple[dict, dict]:
    raw = spec["path"].read_bytes()
    digest = sha256_bytes(raw)
    entry = spec["entry"]
    if entry.get("bytes") is not None and len(raw) != entry["bytes"]:
        raise ValueError("shard byte count differs from catalog: {}".format(spec["path"]))
    if entry.get("sha256") and digest != entry["sha256"]:
        raise ValueError("shard checksum differs from catalog: {}".format(spec["path"]))
    bundle = json.loads(raw)
    papers = bundle.get("papers")
    if not isinstance(papers, list) or int(bundle.get("year", -1)) != spec["year"]:
        raise ValueError("invalid shard schema: {}".format(spec["path"]))
    if bundle.get("venue", spec["venue"]) != spec["venue"]:
        raise ValueError("shard venue differs from catalog: {}".format(spec["path"]))
    if entry.get("count") is not None and len(papers) != entry["count"]:
        raise ValueError("shard record count differs from catalog: {}".format(spec["path"]))
    source_url = next((value for value in (
        entry.get("source_url"), entry.get("dataset_url"), spec.get("catalog_source_url"), bundle.get("source"),
    ) if isinstance(value, str) and value.startswith("https://")), "")
    provenance = {
        "venue": spec["venue"],
        "year": spec["year"],
        "file": entry["file"],
        "bytes": len(raw),
        "records": len(papers),
        "sha256": digest,
        "source_url": source_url,
    }
    return bundle, provenance


def _record_text(value) -> str:
    return value.strip() if isinstance(value, str) else ""


def _paper_fields(paper: dict, venue: str, year: int, source_url: str) -> Tuple[str, ...]:
    title = _record_text(paper.get("title"))
    if not title:
        return ()
    authors_value = paper.get("authors")
    if isinstance(authors_value, list):
        authors = ", ".join(_record_text(name) for name in authors_value if _record_text(name))
    else:
        authors = _record_text(authors_value)
    abstract = _record_text(paper.get("abstract"))
    paper_url = _record_text(paper.get("paper_url") or paper.get("cvf_url") or paper.get("openaccess_url"))
    return (
        _record_text(paper.get("id")), venue, int(year), title, authors, abstract,
        paper_url, source_url, int(not bool(abstract)),
    )


def _normalized_vector(values: Iterable[float], dimension: int = DIMENSION) -> List[float]:
    vector = [float(value) for value in values]
    if len(vector) != dimension or any(not math.isfinite(value) for value in vector):
        raise ValueError("embedder must return finite {}-dimensional vectors".format(dimension))
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        raise ValueError("embedder returned a zero vector")
    return [value / norm for value in vector]


def _encode(embedder, texts: Sequence[str], query: bool = False) -> List[List[float]]:
    values = [QUERY_PREFIX + text if query else text for text in texts]
    if hasattr(embedder, "encode"):
        encoded = embedder.encode(
            values, normalize_embeddings=True, convert_to_numpy=True,
            show_progress_bar=False,
        )
    else:
        encoded = embedder(values)
    rows = list(encoded)
    if len(rows) != len(values):
        raise ValueError("embedder returned a different number of vectors than inputs")
    return [_normalized_vector(row) for row in rows]


def _npy_header(row_count: int, dimension: int) -> bytes:
    header = "{'descr': '<f2', 'fortran_order': False, 'shape': (%d, %d), }" % (row_count, dimension)
    encoded = header.encode("ascii")
    padding = (64 - ((10 + len(encoded) + 1) % 64)) % 64
    encoded += b" " * padding + b"\n"
    if len(encoded) > 65535:
        raise ValueError("vector array header is too large")
    return b"\x93NUMPY\x01\x00" + struct.pack("<H", len(encoded)) + encoded


def _write_vectors(path: Path, connection: sqlite3.Connection, embedder, row_count: int, batch_size: int) -> None:
    format_string = "<{}e".format(DIMENSION)
    cursor = connection.execute("SELECT title, abstract FROM papers ORDER BY rowid")
    with path.open("wb") as output:
        output.write(_npy_header(row_count, DIMENSION))
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            texts = [title if not abstract else title + "\n\n" + abstract for title, abstract in rows]
            vectors = _encode(embedder, texts)
            for vector in vectors:
                output.write(struct.pack(format_string, *vector))
        output.flush()
        os.fsync(output.fileno())
    path.chmod(0o600)


def read_npy_info(path: Path) -> Tuple[int, int, int]:
    with path.open("rb") as source:
        if source.read(8) != b"\x93NUMPY\x01\x00":
            raise ValueError("unsupported vector file; expected NumPy .npy v1")
        header_length = struct.unpack("<H", source.read(2))[0]
        header = ast.literal_eval(source.read(header_length).decode("ascii").strip())
        if header.get("descr") != "<f2" or header.get("fortran_order"):
            raise ValueError("vector file must contain row-major float16 vectors")
        rows, dimension = header["shape"]
        rows, dimension = int(rows), int(dimension)
        offset = 10 + header_length
        if rows < 0 or dimension < 1 or path.stat().st_size != offset + rows * dimension * 2:
            raise ValueError("vector file is truncated or has an invalid shape")
        return rows, dimension, offset


def build_index(
    index_dir: Path,
    embedder,
    model_revision: str = "injected-test-embedder",
    hub_root: Path = HUB_ROOT,
    rebuild: bool = False,
    batch_size: int = 64,
) -> dict:
    """Build a complete cache index in staging, then publish it as one directory."""
    target = _private_index_path(Path(index_dir), hub_root)
    if target.exists() and not target.is_dir():
        raise ValueError("index path exists and is not a directory: {}".format(target))
    if target.exists() and not rebuild:
        raise FileExistsError("index already exists; pass --rebuild to replace it")
    if batch_size < 1:
        raise ValueError("batch size must be positive")
    catalog_path, catalog_digest, specs = catalog_shards(hub_root)
    if not specs:
        raise ValueError("catalog.json contains no available shards")
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = target.with_name("." + target.name + ".staging-" + uuid.uuid4().hex)
    stage.mkdir(mode=0o700)
    connection = None
    try:
        database_path = stage / "papers.sqlite3"
        connection = sqlite3.connect(str(database_path))
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("CREATE TABLE papers (corpus_id TEXT, venue TEXT NOT NULL, year INTEGER NOT NULL, title TEXT NOT NULL, authors TEXT NOT NULL, abstract TEXT NOT NULL, paper_url TEXT NOT NULL, source_url TEXT NOT NULL, abstract_missing INTEGER NOT NULL)")
        shard_manifest = []
        insert_sql = "INSERT INTO papers (corpus_id,venue,year,title,authors,abstract,paper_url,source_url,abstract_missing) VALUES (?,?,?,?,?,?,?,?,?)"
        for spec in specs:
            bundle, provenance = read_shard(spec)
            source_url = provenance["source_url"] if provenance["source_url"].startswith("https://") else ""
            for paper in bundle["papers"]:
                fields = _paper_fields(paper, spec["venue"], spec["year"], source_url)
                if fields:
                    connection.execute(insert_sql, fields)
            shard_manifest.append(provenance)
            del bundle
        connection.execute("CREATE INDEX papers_venue_year ON papers(venue, year)")
        connection.execute("CREATE VIRTUAL TABLE paper_fts USING fts5(title, authors, abstract, content='papers', content_rowid='rowid', tokenize='unicode61 remove_diacritics 2')")
        connection.execute("INSERT INTO paper_fts(paper_fts) VALUES('rebuild')")
        connection.commit()
        row_count = connection.execute("SELECT count(*) FROM papers").fetchone()[0]
        if row_count < 1:
            raise ValueError("catalog shards contain no papers with titles")
        missing_abstracts = connection.execute("SELECT count(*) FROM papers WHERE abstract_missing=1").fetchone()[0]
        _write_vectors(stage / "paper-vectors.npy", connection, embedder, row_count, batch_size)
        connection.execute("PRAGMA optimize")
        connection.close()
        connection = None
        database_path.chmod(0o600)
        vector_path = stage / "paper-vectors.npy"
        vector_rows, dimension, _ = read_npy_info(vector_path)
        if vector_rows != row_count or dimension != DIMENSION:
            raise ValueError("vector count or dimension does not match the paper table")
        manifest = {
            "format": FORMAT,
            "built_at_utc": utc_now(),
            "catalog_path": str(Path(catalog_path).relative_to(Path(hub_root).resolve())),
            "catalog_sha256": catalog_digest,
            "paper_count": row_count,
            "abstract_missing_count": missing_abstracts,
            "vector_dimension": dimension,
            "vector_dtype": "float16",
            "vector_rowid_mapping": "paper rowid N is stored at vector row N-1",
            "embedding_model": MODEL_NAME,
            "embedding_model_revision": model_revision,
            "paper_embedding_text": "title plus abstract; title only when abstract is missing",
            "query_prefix": QUERY_PREFIX,
            "fts5_bm25_weights": {"title": BM25_WEIGHTS[0], "authors": BM25_WEIGHTS[1], "abstract": BM25_WEIGHTS[2]},
            "rrf_k": RRF_K,
            "source_shards": shard_manifest,
            "files": {
                "papers.sqlite3": {"bytes": (stage / "papers.sqlite3").stat().st_size, "sha256": sha256_file(stage / "papers.sqlite3")},
                "paper-vectors.npy": {"bytes": vector_path.stat().st_size, "sha256": sha256_file(vector_path)},
            },
        }
        manifest_path = stage / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest_path.chmod(0o600)
        backup = None
        if target.exists():
            backup = target.with_name("." + target.name + ".previous-" + uuid.uuid4().hex)
            os.replace(str(target), str(backup))
        try:
            os.replace(str(stage), str(target))
        except Exception:
            if backup is not None and backup.exists():
                os.replace(str(backup), str(target))
            raise
        if backup is not None:
            shutil.rmtree(backup)
        return manifest
    except Exception:
        if connection is not None:
            connection.close()
        if stage.exists():
            shutil.rmtree(stage)
        raise


def load_manifest(index_dir: Path) -> dict:
    path = index_dir / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("format") != FORMAT or manifest.get("vector_dimension") != DIMENSION:
        raise ValueError("index manifest is missing or has an unsupported format")
    for name in ("papers.sqlite3", "paper-vectors.npy"):
        if not (index_dir / name).is_file():
            raise ValueError("index is incomplete: {} is missing".format(name))
    rows, dimension, _ = read_npy_info(index_dir / "paper-vectors.npy")
    if rows != manifest.get("paper_count") or dimension != DIMENSION:
        raise ValueError("index vectors do not align with the manifest")
    return manifest


def _fts_query(query: str) -> str:
    tokens = []
    for token in re.findall(r"[^\W_]+", query, flags=re.UNICODE):
        folded = token.casefold()
        if folded not in tokens:
            tokens.append(folded)
    if not tokens:
        raise ValueError("query must contain at least one searchable word")
    expression = " OR ".join('"{}"'.format(token) for token in tokens)
    if len(tokens) > 1:
        phrase = 'authors : "{}"'.format(" ".join(tokens))
        expression = "({}) OR {}".format(expression, phrase)
    return expression


def _filters(venues: Optional[Sequence[str]], years: Optional[Sequence[int]], alias: str = "p") -> Tuple[str, List[object]]:
    clauses = []
    values: List[object] = []
    if venues:
        clauses.append("{}.venue IN ({})".format(alias, ",".join("?" for _ in venues)))
        values.extend(venue.upper() for venue in venues)
    if years:
        clauses.append("{}.year IN ({})".format(alias, ",".join("?" for _ in years)))
        values.extend(int(year) for year in years)
    return (" AND " + " AND ".join(clauses) if clauses else ""), values


def _open_database(index_dir: Path) -> sqlite3.Connection:
    uri = (index_dir / "papers.sqlite3").resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    return connection


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norm_left = math.sqrt(sum(value * value for value in left))
    norm_right = math.sqrt(sum(value * value for value in right))
    return dot / (norm_left * norm_right) if norm_left and norm_right else 0.0


def _selected_vectors(path: Path, row_ids: Sequence[int]) -> Dict[int, List[float]]:
    if not row_ids:
        return {}
    try:
        import numpy as np
    except ImportError:
        np = None
    if np is not None:
        matrix = np.load(str(path), mmap_mode="r")
        selected = {}
        for row_id in row_ids:
            selected[row_id] = [float(value) for value in matrix[row_id - 1].astype("float32")]
        return selected
    _, dimension, offset = read_npy_info(path)
    selected = {}
    with path.open("rb") as source:
        for row_id in row_ids:
            source.seek(offset + (row_id - 1) * dimension * 2)
            raw = source.read(dimension * 2)
            if len(raw) != dimension * 2:
                raise ValueError("vector file ended before row {}".format(row_id))
            selected[row_id] = list(struct.unpack("<{}e".format(dimension), raw))
    return selected


def _dense_scores(index_dir: Path, row_ids: Sequence[int], query_vector: Sequence[float]) -> List[Tuple[int, float]]:
    if not row_ids:
        return []
    try:
        import numpy as np
    except ImportError:
        np = None
    scores = []
    if np is None:
        path = index_dir / "paper-vectors.npy"
        _, dimension, offset = read_npy_info(path)
        with path.open("rb") as source:
            for row_id in row_ids:
                source.seek(offset + (row_id - 1) * dimension * 2)
                raw = source.read(dimension * 2)
                if len(raw) != dimension * 2:
                    raise ValueError("vector file ended before row {}".format(row_id))
                vector = struct.unpack("<{}e".format(dimension), raw)
                scores.append((row_id, _cosine(query_vector, vector)))
    else:
        matrix = np.load(str(index_dir / "paper-vectors.npy"), mmap_mode="r")
        query = np.asarray(query_vector, dtype=np.float32)
        for start in range(0, len(row_ids), 8192):
            ids = row_ids[start:start + 8192]
            block = matrix[[row_id - 1 for row_id in ids]].astype(np.float32)
            norms = np.linalg.norm(block, axis=1)
            values = block @ query
            values = values / np.maximum(norms, 1e-12)
            scores.extend((row_id, float(score)) for row_id, score in zip(ids, values))
    scores.sort(key=lambda pair: (-pair[1], pair[0]))
    return scores


def _metadata(connection: sqlite3.Connection, row_ids: Sequence[int]) -> Dict[int, sqlite3.Row]:
    output = {}
    for start in range(0, len(row_ids), 800):
        group = row_ids[start:start + 800]
        marks = ",".join("?" for _ in group)
        rows = connection.execute("SELECT rowid AS row_id, corpus_id, venue, year, title, authors, abstract, paper_url, source_url, abstract_missing FROM papers WHERE rowid IN ({})".format(marks), group)
        output.update((row["row_id"], row) for row in rows)
    return output


def search_index(
    index_dir: Path,
    query: str,
    venues: Optional[Sequence[str]] = None,
    years: Optional[Sequence[int]] = None,
    limit: int = 10,
    embedder=None,
) -> List[dict]:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    index_dir = Path(index_dir).expanduser()
    load_manifest(index_dir)
    fts_text = _fts_query(query)
    query_vector = _encode(embedder, [query], query=True)[0]
    connection = _open_database(index_dir)
    try:
        filter_sql, filter_values = _filters(venues, years)
        row_ids = [row[0] for row in connection.execute("SELECT p.rowid FROM papers p WHERE 1=1" + filter_sql + " ORDER BY p.rowid", filter_values)]
        if not row_ids:
            return []
        window = min(len(row_ids), max(200, limit * 20))
        lexical = connection.execute(
            "SELECT p.rowid, bm25(paper_fts, ?, ?, ?) AS score "
            "FROM paper_fts JOIN papers p ON p.rowid=paper_fts.rowid "
            "WHERE paper_fts MATCH ?" + filter_sql +
            " ORDER BY score ASC, p.rowid ASC LIMIT ?",
            list(BM25_WEIGHTS) + [fts_text] + filter_values + [window],
        ).fetchall()
        bm25_rank = {row["rowid"]: rank for rank, row in enumerate(lexical, 1)}
        dense = _dense_scores(index_dir, row_ids, query_vector)
        dense_rank = {row_id: rank for rank, (row_id, _) in enumerate(dense[:window], 1)}
        cosine_scores = dict(dense)
        candidate_ids = set(bm25_rank) | set(dense_rank)
        fused = {}
        for row_id in candidate_ids:
            score = 0.0
            if row_id in bm25_rank:
                score += 1.0 / (RRF_K + bm25_rank[row_id])
            if row_id in dense_rank:
                score += 1.0 / (RRF_K + dense_rank[row_id])
            fused[row_id] = score
        ordered = sorted(candidate_ids, key=lambda row_id: (-fused[row_id], -cosine_scores[row_id], bm25_rank.get(row_id, 10 ** 9), row_id))[:limit]
        records = _metadata(connection, ordered)
        return [
            {
                "paper_id": records[row_id]["corpus_id"],
                "venue": records[row_id]["venue"],
                "year": records[row_id]["year"],
                "title": records[row_id]["title"],
                "authors": records[row_id]["authors"],
                "paper_url": records[row_id]["paper_url"],
                "source_url": records[row_id]["source_url"],
                "abstract_missing": bool(records[row_id]["abstract_missing"]),
                "bm25_rank": bm25_rank.get(row_id),
                "dense_rank": dense_rank.get(row_id),
                "cosine_similarity": cosine_scores[row_id],
                "rrf_score": fused[row_id],
                "rrf_rank": rank,
            }
            for rank, row_id in enumerate(ordered, 1)
        ]
    finally:
        connection.close()


def chunk_text(text: str, chunk_words: int = CHUNK_WORDS, overlap: int = CHUNK_OVERLAP) -> List[str]:
    if chunk_words < 1 or overlap < 0 or overlap >= chunk_words:
        raise ValueError("chunk size must be positive and overlap smaller than chunk size")
    words = text.split()
    if not words:
        return []
    step = chunk_words - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunk = words[start:start + chunk_words]
        if not chunk:
            break
        chunks.append(" ".join(chunk))
        if start + chunk_words >= len(words):
            break
    return chunks


def extract_draft_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".txt", ".md"):
        text = path.read_text(encoding="utf-8-sig")
    elif suffix == ".pdf":
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError("PDF comparison requires optional PyMuPDF; install it explicitly with uv in your local environment.") from exc
        try:
            with fitz.open(str(path)) as document:
                text = "\n".join(page.get_text("text") for page in document)
        except Exception as exc:
            raise RuntimeError("Could not read the local PDF: {}".format(exc)) from exc
    else:
        raise ValueError("draft must be a .txt, .md, or .pdf file")
    if not text.strip():
        raise ValueError("draft contains no readable text")
    return text


def compare_draft(index_dir: Path, draft_text: str, embedder, limit: int = 10) -> List[dict]:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    index_dir = Path(index_dir).expanduser()
    load_manifest(index_dir)
    chunks = chunk_text(draft_text)
    if not chunks:
        raise ValueError("draft contains no readable text")
    chunk_vectors = _encode(embedder, chunks, query=True)
    document_vector = _normalized_vector(
        [sum(vector[column] for vector in chunk_vectors) / len(chunk_vectors) for column in range(DIMENSION)]
    )
    connection = _open_database(index_dir)
    try:
        row_ids = [row[0] for row in connection.execute("SELECT rowid FROM papers ORDER BY rowid")]
        document_scores = _dense_scores(index_dir, row_ids, document_vector)
        top = document_scores[:limit]
        vectors = _selected_vectors(index_dir / "paper-vectors.npy", [row_id for row_id, _ in top])
        records = _metadata(connection, [row_id for row_id, _ in top])
        output = []
        for row_id, document_score in top:
            per_chunk = [_cosine(chunk, vectors[row_id]) for chunk in chunk_vectors]
            best_index = max(range(len(per_chunk)), key=lambda index: per_chunk[index])
            excerpt = chunks[best_index]
            if len(excerpt) > 280:
                excerpt = excerpt[:277].rsplit(" ", 1)[0] + "..."
            row = records[row_id]
            output.append({
                "paper_id": row["corpus_id"],
                "venue": row["venue"],
                "year": row["year"],
                "title": row["title"],
                "authors": row["authors"],
                "paper_url": row["paper_url"],
                "source_url": row["source_url"],
                "abstract_missing": bool(row["abstract_missing"]),
                "document_cosine": document_score,
                "strongest_chunk_index": best_index + 1,
                "strongest_chunk_cosine": per_chunk[best_index],
                "draft_excerpt": excerpt,
            })
        return output
    finally:
        connection.close()


def _model_path(model_name: str, revision: Optional[str], allow_download: bool) -> Tuple[Path, str]:
    local = Path(model_name).expanduser()
    if local.is_dir():
        return local, "local"
    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise RuntimeError("semantic commands require sentence-transformers and huggingface-hub in the selected Python environment") from exc
    try:
        path = snapshot_download(
            repo_id=model_name,
            revision=revision,
            local_files_only=not allow_download,
        )
    except Exception as exc:
        if allow_download:
            raise RuntimeError("could not load model weights during explicit build: {}".format(exc)) from exc
        raise RuntimeError("model weights are not cached locally; run the explicit build command once to fetch them") from exc
    return Path(path), Path(path).name


def _sentence_transformer(model_path: Path):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("semantic commands require sentence-transformers; install it explicitly with uv in a local environment") from exc
    model = SentenceTransformer(str(model_path), device="cpu")
    if model.get_sentence_embedding_dimension() != DIMENSION:
        raise RuntimeError("expected a {}-dimension embedding model".format(DIMENSION))
    return model


def _display_search(results: Sequence[dict]) -> None:
    if not results:
        print("No matches.")
        return
    for result in results:
        lexical = "—" if result["bm25_rank"] is None else str(result["bm25_rank"])
        print("[{}] {} {} · {} · BM25 rank {} · cosine {:.5f} · RRF {:.6f}".format(
            result["rrf_rank"], result["venue"], result["year"], result["title"],
            lexical, result["cosine_similarity"], result["rrf_score"],
        ))
        print("    Authors: {}".format(result["authors"] or "Unavailable"))
        if result["abstract_missing"]:
            print("    Abstract unavailable")
        print("    Paper: {}".format(result["paper_url"] or "No paper URL in source metadata"))
        print("    Dataset source: {}".format(result["source_url"] or "Unavailable"))


def _display_compare(results: Sequence[dict]) -> None:
    print("Archive records contain titles and abstracts, not full papers. These metadata comparisons are not full-paper novelty detection.")
    if not results:
        print("No indexed papers.")
        return
    for result in results:
        print("[{}] {} {} · {} · document cosine {:.5f} · strongest draft chunk #{} cosine {:.5f}".format(
            result["venue"], result["year"], result["title"], result["paper_id"],
            result["document_cosine"], result["strongest_chunk_index"], result["strongest_chunk_cosine"],
        ))
        print("    Authors: {}".format(result["authors"] or "Unavailable"))
        if result["abstract_missing"]:
            print("    Abstract unavailable; this indexed vector represents title metadata only")
        print("    Draft excerpt: {}".format(result["draft_excerpt"]))
        print("    Paper: {}".format(result["paper_url"] or "No paper URL in source metadata"))
        print("    Dataset source: {}".format(result["source_url"] or "Unavailable"))


def _build_command(args) -> int:
    index_dir = _private_index_path(args.index_dir, HUB_ROOT)
    if args.batch_size < 1:
        raise ValueError("batch size must be positive")
    if index_dir.exists() and not args.rebuild:
        raise FileExistsError("index already exists; pass --rebuild to replace it")
    _catalog_path, _catalog_hash, specs = catalog_shards(HUB_ROOT)
    if not specs:
        raise ValueError("catalog.json contains no available shards")
    # Weight resolution can access the network only from this explicit command.
    model_path, revision = _model_path(MODEL_NAME, None, allow_download=True)
    model = _sentence_transformer(model_path)
    manifest = build_index(index_dir, model, revision, HUB_ROOT, args.rebuild, args.batch_size)
    print("Built {} papers in {}".format(manifest["paper_count"], index_dir))
    print("Vectors: {} float16 values; missing abstracts: {}".format(manifest["vector_dimension"], manifest["abstract_missing_count"]))
    return 0


def _runtime_embedder(index_dir: Path):
    manifest = load_manifest(index_dir)
    model_path, _revision = _model_path(
        manifest["embedding_model"], manifest["embedding_model_revision"], allow_download=False,
    )
    return _sentence_transformer(model_path)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build", help="build the local index; this explicit command may download model weights")
    build.add_argument("--index-dir", type=Path, default=default_index_dir())
    build.add_argument("--rebuild", action="store_true", help="replace an existing complete index after staging succeeds")
    build.add_argument("--batch-size", type=int, default=64)
    search = subparsers.add_parser("search", help="hybrid lexical and dense search")
    search.add_argument("query", help="natural-language query")
    search.add_argument("--index-dir", type=Path, default=default_index_dir())
    search.add_argument("--venue", action="append", help="venue filter; repeat to select several")
    search.add_argument("--year", action="append", type=int, help="year filter; repeat to select several")
    search.add_argument("--limit", type=int, default=10)
    compare = subparsers.add_parser("compare", help="compare a local draft with indexed titles and abstracts")
    compare.add_argument("--draft", required=True, type=Path)
    compare.add_argument("--index-dir", type=Path, default=default_index_dir())
    compare.add_argument("--limit", type=int, default=10)
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            return _build_command(args)
        embedder = _runtime_embedder(args.index_dir)
        if args.command == "search":
            results = search_index(args.index_dir, args.query, args.venue, args.year, args.limit, embedder)
            _display_search(results)
        else:
            text = extract_draft_text(args.draft)
            results = compare_draft(args.index_dir, text, embedder, args.limit)
            _display_compare(results)
    except (OSError, ValueError, sqlite3.Error, RuntimeError) as exc:
        print("semantic_retrieval: {}".format(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
