"""Manim scenes for IRE final presentation, task ire-final-v2-20261117.

Render, from this directory:
    python -m manim -qm --fps 30 --resolution 1280,720 scenes.py FrozenFeedback CollectiveCoverage QueryResidual

The matrix and geometry are illustrative. They do not encode measured results.
"""

from manim import *
import numpy as np
from pathlib import Path
import hashlib
import json

PAPER = "#FAFAF7"
INK = "#141414"
BLUE = "#1E3AF5"
GREY = "#666666"
LIGHT = "#D8D8D4"
PALE = "#E8EBFF"
FONT = "Arial"

config.background_color = PAPER
config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 30


def label(s, size=26, colour=INK, **kwargs):
    return Text(s, font=FONT, font_size=size, color=colour, **kwargs)


def formula(s, size=29, colour=INK):
    # The shipped vector formula cache avoids requiring a system TeX install.
    # Manim still creates, positions and animates every diagram object.
    cache = Path(__file__).parent / "math-svg"
    key = hashlib.sha256(s.encode()).hexdigest()[:16]
    svg = cache / (key + ".svg")
    if svg.exists():
        dimensions = json.loads((cache / "dimensions.json").read_text())
        result = SVGMobject(str(svg), height=None, width=None, color=colour)
        result.scale_to_fit_width(dimensions[key]["width_pt"] * size * 0.001)
        result.set_color(colour)
        return result
    return MathTex(s, font_size=size, color=colour)


def header(title, subtitle=None):
    main = label(title, 37).to_edge(UP, buff=0.42).to_edge(LEFT, buff=0.6)
    if subtitle is None:
        return VGroup(main)
    sub = label(subtitle, 18, GREY).next_to(main, DOWN, buff=0.19).align_to(main, LEFT)
    return VGroup(main, sub)


def panel(title, equation, centre, width=3.6, height=1.5, eq_size=29):
    box = Rectangle(width=width, height=height, stroke_color=LIGHT, stroke_width=1.3,
                    fill_color=PAPER, fill_opacity=1).move_to(centre)
    name = label(title, 25).move_to(centre + UP * 0.4)
    eq = formula(equation, eq_size).move_to(centre + DOWN * 0.21)
    if eq.width > width - 0.3:
        eq.scale_to_fit_width(width - 0.3)
    return VGroup(box, name, eq)


def arrow(a, b, **kwargs):
    return Arrow(a, b, buff=0.12, color=BLUE, stroke_width=2.6,
                 max_tip_length_to_length_ratio=0.10, **kwargs)


class FrozenFeedback(Scene):
    """The data flow of query-wise feedback fitting, with no teacher gradient."""

    def construct(self):
        title = header("Query-wise retrieval with fixed models")
        dense = panel("Initial dense search", r"C_{50}(q)=\operatorname{Top}_{50,d\in\mathcal{D}}\ x_q^\top z_d",
                      np.array([-4.65, 1.45, 0]), width=3.8, eq_size=25)
        selection = panel("Feedback selection", r"S_\pi(q)\subset C_{50}(q),\quad |S_\pi|=10",
                          np.array([0, 1.45, 0]), width=3.8, eq_size=26)
        teacher = panel("Black-box reranker", r"r_d=R(q,d),\quad d\in S_\pi(q)",
                        np.array([4.65, 1.45, 0]), width=3.8, eq_size=28)
        fit = panel("Query residual fit", r"\widehat{v}_q=v_q^{(300)}",
                    np.array([3.25, -1.3, 0]), width=5.2, eq_size=31)
        search = panel("Second full-corpus search", r"\operatorname{Top}_{K,d\in\mathcal{D}}\ \operatorname{unit}(x_q+\alpha\widehat{v}_q)^\top z_d",
                       np.array([-3.25, -1.3, 0]), width=5.2, eq_size=27)
        a1 = arrow(dense.get_right(), selection.get_left())
        a2 = arrow(selection.get_right(), teacher.get_left())
        a3 = arrow(teacher.get_bottom(), np.array([4.65, -0.5, 0]))
        a4 = arrow(fit.get_left(), search.get_right())
        scalar = label("fixed scalar targets", 19, BLUE).next_to(a3, LEFT, buff=0.16)
        local = label("Local gradients use the fixed document vectors.", 20, GREY).move_to([1.8, -2.43, 0])
        frozen = label("Encoder weights and the corpus vectors remain fixed.", 22, INK).to_edge(DOWN, buff=0.42)

        self.play(FadeIn(title), run_time=0.7)
        self.play(FadeIn(dense), run_time=0.9)
        self.play(GrowArrow(a1), FadeIn(selection), run_time=1.1)
        self.play(GrowArrow(a2), FadeIn(teacher), run_time=1.1)
        self.wait(0.5)
        self.play(GrowArrow(a3), FadeIn(scalar), FadeIn(fit), run_time=1.3)
        self.play(FadeIn(local), run_time=0.8)
        self.play(GrowArrow(a4), FadeIn(search), run_time=1.3)
        self.play(FadeIn(frozen), run_time=0.8)
        self.wait(3.0)


class CollectiveCoverage(Scene):
    """An invented matrix demonstrates positive marginal token coverage."""

    def construct(self):
        title = header("Collective contextual-token coverage", "Illustrative similarities for three documents in a fixed candidate pool")
        # h_j(d) = max token similarity for query token j and document d.
        values = np.array([[0.9, 0.8, 0.1], [0.8, 0.7, 0.1], [0.2, 0.2, 0.9]])
        cols = [-3.65, -2.35, -1.05]
        rows = [1.35, 0.25, -0.85]
        row_labels = VGroup(*[formula(fr"d_{i+1}", 30).move_to([-5.0, y, 0]) for i, y in enumerate(rows)])
        col_labels = VGroup(*[formula(fr"u_{j+1}", 30).move_to([x, 2.22, 0]) for j, x in enumerate(cols)])
        cells, numbers = VGroup(), VGroup()
        for i, y in enumerate(rows):
            for j, x in enumerate(cols):
                cells.add(Rectangle(width=1.13, height=0.88, stroke_width=0,
                                    fill_color=PALE, fill_opacity=0.22+0.60*values[i, j]).move_to([x, y, 0]))
                numbers.add(label(f"{values[i,j]:.1f}", 29).move_to([x, y, 0]))
        h = formula(r"h_j(d)=\max_t\cos(u_j,t_{d,t})", 31).move_to([3.3, 2.0, 0])
        cov = formula(r"F_q(S)=\sum_j\max\!\left(0,\max_{d\in S}h_j(d)\right)", 27).move_to([3.3, 1.05, 0])
        first = formula(r"S_1=\{d_1\},\qquad F_q(S_1)=1.8", 29).move_to([3.3, -0.05, 0])
        marginal = VGroup(
            formula(r"\Delta(d_2\mid S_1)=0.0", 28),
            formula(r"\Delta(d_3\mid S_1)=0.8", 28, BLUE),
        ).arrange(DOWN, buff=0.25).move_to([3.3, -1.1, 0])
        selected1 = Rectangle(width=4.0, height=0.92, stroke_color=BLUE, stroke_width=2.3).move_to([-2.35, rows[0], 0])
        selected3 = Rectangle(width=4.0, height=0.92, stroke_color=BLUE, stroke_width=2.3).move_to([-2.35, rows[2], 0])
        result = formula(r"S_2=\{d_1,d_3\},\qquad F_q(S_2)=2.6", 33, BLUE).move_to([0, -2.35, 0])
        foot = label("Selection returns document IDs; TTT-Embed uses the dense document vectors.", 20, GREY).to_edge(DOWN, buff=0.40)

        self.play(FadeIn(title), run_time=0.7)
        self.play(FadeIn(row_labels), FadeIn(col_labels), FadeIn(cells), FadeIn(numbers), run_time=1.2)
        self.play(FadeIn(h), FadeIn(cov), run_time=1.2)
        self.play(Create(selected1), FadeIn(first), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(marginal), run_time=1.1)
        self.play(Create(selected3), FadeIn(result), run_time=1.3)
        self.play(FadeIn(foot), run_time=0.7)
        self.wait(3.0)


class QueryResidual(Scene):
    """Illustrative 2-D geometry; no empirical relevance or gain is implied."""

    def construct(self):
        title = header("A residual changes the query representation", "Illustrative two-dimensional geometry")
        origin = np.array([-3.8, -0.65, 0])
        scale = 2.15
        # x has unit norm; x+v is deliberately not unit length.
        x = np.array([0.6, 0.8, 0])
        v = np.array([0.5, -0.2, 0])
        raw = x + v
        unit = raw / np.linalg.norm(raw)
        dot_x = origin + scale*x
        dot_raw = origin + scale*raw
        dot_unit = origin + scale*unit
        circle = Circle(radius=scale, color=LIGHT, stroke_width=1.3).move_to(origin)
        ax = VGroup(Line(origin+LEFT*2.7, origin+RIGHT*3.4, color=LIGHT, stroke_width=1.2),
                    Line(origin+DOWN*1.05, origin+UP*3.1, color=LIGHT, stroke_width=1.2))
        # Unit document vectors are fixed at three angles.
        doc_angles = [0.12, 1.46, 2.35]
        docs = VGroup()
        doc_labels = VGroup()
        for i, angle in enumerate(doc_angles):
            pos = origin+scale*np.array([np.cos(angle),np.sin(angle),0])
            docs.add(Dot(pos, radius=0.063, color=GREY))
            direction = RIGHT if i == 0 else UP if i == 1 else LEFT
            doc_labels.add(formula(fr"z_{i+1}", 25, GREY).next_to(docs[-1], direction, buff=0.14))
        original = Arrow(origin,dot_x,buff=0,color=INK,stroke_width=3)
        orig_label = formula(r"x_q", 29).next_to(dot_x, LEFT, buff=0.13)
        residual = Arrow(dot_x, dot_raw, buff=0,color=BLUE,stroke_width=3)
        residual_label = formula(r"v", 29, BLUE).next_to(residual, UP, buff=0.08)
        raw_point = Dot(dot_raw, radius=0.06, color=BLUE)
        raw_label = formula(r"x_q+v", 27, BLUE).next_to(dot_raw, RIGHT, buff=0.14)
        normalized = Arrow(origin,dot_unit,buff=0,color=BLUE,stroke_width=4)
        unit_label = formula(r"\operatorname{unit}(x_q+v)", 27, BLUE).move_to([-3.8,-3.0,0])
        projected = DashedLine(dot_raw,dot_unit,color=GREY,stroke_width=2,dash_length=0.07)
        eq1 = formula(r"\widehat{x}_q(v)=\frac{x_q+v}{\|x_q+v\|_2}", 36).move_to([3.7,1.42,0])
        eq2 = formula(r"p^S_d(v)=\operatorname{softmax}_{d}\!\left(\frac{\widehat{x}_q(v)^\top z_d}{\tau_S}\right)", 30).move_to([3.7,0.12,0])
        teacher = label("Teacher targets remain fixed.", 22, GREY).move_to([3.7,-1.1,0])
        deploy = VGroup(label("Recorded FiQA deployment",21,INK),
                        formula(r"\widetilde{x}_q=\operatorname{unit}(x_q+0.5\widehat{v}_q)",31))
        deploy.arrange(DOWN,buff=0.25).move_to([3.7,-2.23,0])
        foot = label("Document vectors and encoder weights remain fixed.",20,GREY).to_edge(DOWN,buff=0.40)

        self.play(FadeIn(title), run_time=0.7)
        self.play(Create(ax), Create(circle), FadeIn(docs), FadeIn(doc_labels), run_time=1.0)
        self.play(GrowArrow(original), FadeIn(orig_label), run_time=0.9)
        self.play(GrowArrow(residual), FadeIn(residual_label), FadeIn(raw_point), FadeIn(raw_label), run_time=1.1)
        self.play(FadeIn(eq1), run_time=0.8)
        self.play(Create(projected), GrowArrow(normalized), FadeIn(unit_label), run_time=1.2)
        self.play(FadeIn(eq2), FadeIn(teacher), run_time=1.0)
        self.play(FadeIn(deploy), FadeIn(foot), run_time=0.9)
        self.wait(3.0)

