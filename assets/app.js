"use strict";

const searchInput = document.querySelector("#search-input");
const clearButton = document.querySelector("#clear-button");
const filtersElement = document.querySelector("#category-filters");
const resultsElement = document.querySelector("#results");
const resultCount = document.querySelector("#result-count");
const introCount = document.querySelector("#intro-count");
const sidebarCount = document.querySelector("#sidebar-count");
const loadError = document.querySelector("#load-error");
let entries = [];
let activeCategory = "all";

function make(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function searchableText(entry) {
  return [entry.title, entry.description, entry.project, entry.category, ...entry.tags]
    .join(" ")
    .toLocaleLowerCase();
}

function updateLibraryCounts() {
  const count = entries.length;
  introCount.textContent = String(count);
  sidebarCount.textContent = `${count} ${count === 1 ? "item" : "items"}`;
}

function renderFilters() {
  filtersElement.replaceChildren();
  const categories = ["all", ...new Set(entries.map((entry) => entry.category))];
  for (const category of categories) {
    const button = make("button", "category-button", category === "all" ? "All topics" : category);
    button.type = "button";
    button.dataset.category = category;
    button.setAttribute("aria-pressed", String(category === activeCategory));
    button.addEventListener("click", () => {
      activeCategory = category;
      render();
    });
    filtersElement.append(button);
  }
}

function makeCard(entry) {
  const article = make("article", "entry-card");
  const top = make("div", "entry-topline");
  top.append(make("span", "project-label", entry.project));
  top.append(make("span", "entry-arrow", "↗"));

  const link = make("a", "entry-link", entry.title);
  link.href = entry.url;
  if (entry.url.startsWith("https://")) {
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", `${entry.title} (opens in a new tab)`);
  }

  const description = make("p", "entry-description", entry.description);
  const footer = make("div", "entry-footer");
  const tags = make("ul", "tag-list");
  for (const tag of entry.tags.slice(0, 3)) tags.append(make("li", "tag", tag));
  footer.append(tags);

  article.append(top, link, description, footer);
  return article;
}

function render() {
  const query = searchInput.value.trim().toLocaleLowerCase();
  const matches = entries.filter((entry) => {
    const categoryMatches = activeCategory === "all" || entry.category === activeCategory;
    return categoryMatches && (!query || searchableText(entry).includes(query));
  });
  const grouped = new Map();
  for (const entry of matches) {
    if (!grouped.has(entry.category)) grouped.set(entry.category, []);
    grouped.get(entry.category).push(entry);
  }

  resultsElement.replaceChildren();
  for (const [category, categoryEntries] of grouped) {
    const section = make("section", "topic-section");
    const heading = make("h2", "topic-heading", category);
    heading.id = `topic-${entries.findIndex((entry) => entry.category === category)}`;
    const grid = make("div", "entry-grid");
    for (const entry of categoryEntries) grid.append(makeCard(entry));
    section.append(heading, grid);
    resultsElement.append(section);
  }

  resultCount.textContent = `${matches.length} ${matches.length === 1 ? "item" : "items"}`;
  if (matches.length === 0) {
    const empty = make("div", "empty-state");
    empty.append(make("span", "empty-mark", "⌕"), make("h2", "", "No matches yet"));
    empty.append(make("p", "", "Try another word or clear the current filters."));
    resultsElement.append(empty);
  }
  resultsElement.setAttribute("aria-busy", "false");
  for (const button of filtersElement.querySelectorAll("button")) {
    button.setAttribute("aria-pressed", String(button.dataset.category === activeCategory));
  }
}

function clearFilters() {
  searchInput.value = "";
  activeCategory = "all";
  searchInput.blur();
  render();
}

searchInput.addEventListener("input", render);
clearButton.addEventListener("click", clearFilters);
document.addEventListener("keydown", (event) => {
  const target = event.target;
  const editing = target instanceof HTMLElement &&
    (target.isContentEditable || ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName));
  if (event.key === "/" && !editing && !event.metaKey && !event.ctrlKey && !event.altKey) {
    event.preventDefault();
    searchInput.focus();
  } else if (event.key === "Escape") {
    if (searchInput.value || activeCategory !== "all") clearFilters();
  }
});

fetch("./library.json")
  .then((response) => {
    if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
    return response.json();
  })
  .then((data) => {
    if (!Array.isArray(data)) throw new TypeError("Catalog must be a list");
    entries = data;
    updateLibraryCounts();
    renderFilters();
    render();
  })
  .catch(() => {
    resultsElement.setAttribute("aria-busy", "false");
    resultCount.textContent = "Library unavailable";
    loadError.hidden = false;
  });
