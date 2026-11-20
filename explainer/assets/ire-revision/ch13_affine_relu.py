from manim import *

class Chapter13(Scene):
    def construct(self):
        self.camera.background_color = "#101827"
        title = Text("One layer: affine map, then ReLU", font_size=47, weight=BOLD).to_edge(UP)
        self.add(title)
        plane = Axes(x_range=[-3,3,1],y_range=[-2,2,1],x_length=8,y_length=4.45,
                     tips=False, axis_config={"color":"#9EADC0"}).shift(DOWN*.15)
        self.play(Create(plane),run_time=.6)
        xy=[(-2,-1),(-1.4,.8),(-.75,-.55),(.5,1.12),(1.3,-.7),(1.9,.45)]
        colors=[TEAL_A,TEAL_A,TEAL_A,GOLD_A,GOLD_A,GOLD_A]
        points=VGroup(*[Dot(plane.c2p(x,y),color=c,radius=.115) for (x,y),c in zip(xy,colors)])
        legend=VGroup(VGroup(Dot(color=TEAL_A,radius=.075),Text("Class A",font_size=24)).arrange(RIGHT,buff=.16),
                      VGroup(Dot(color=GOLD_A,radius=.075),Text("Class B",font_size=24)).arrange(RIGHT,buff=.16)).arrange(DOWN,aligned_edge=LEFT,buff=.23).to_edge(RIGHT,buff=.48).shift(UP*.7)
        def caption(s): return Text(s,font_size=31,color="#E2E8F0").to_edge(DOWN,buff=.4)
        cap=caption("Start with six labeled inputs.")
        self.play(FadeIn(points,legend,cap))
        self.wait(1.0)
        affine=[(x+.5*y-.25,.65*y+.35*x-.12) for x,y in xy]
        next_cap=caption("Affine map: mix coordinates, then add a bias.")
        self.play(ReplacementTransform(cap,next_cap),*[p.animate.move_to(plane.c2p(*a)) for p,a in zip(points,affine)],run_time=1.55)
        self.wait(1.1)
        proj=[(max(0,x),max(0,y)) for x,y in affine]
        guides=VGroup(*[DashedLine(plane.c2p(*a),plane.c2p(*b),color="#B1BFD1",stroke_width=2) for a,b in zip(affine,proj) if a!=b])
        relu=caption("ReLU replaces each negative coordinate with zero.")
        self.play(FadeIn(guides),ReplacementTransform(next_cap,relu),run_time=.65)
        self.play(*[p.animate.move_to(plane.c2p(*b)) for p,b in zip(points,proj)],run_time=1.5)
        self.wait(1.25)
        final=caption("Labels stay fixed, even when inputs map to the same point.")
        self.play(FadeOut(guides),ReplacementTransform(relu,final))
        self.wait(2.05)
