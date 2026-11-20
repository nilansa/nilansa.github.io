from manim import *

config.background_color = "#10131c"

class LoggedFeedback(Scene):
    def construct(self):
        title=Text("One log. Two policies.",font_size=48).to_edge(UP,buff=.48)
        subtitle=Text("Only the shown result can get a click.",font_size=29,color=BLUE_B).next_to(title,DOWN,buff=.25)
        self.play(Write(title),FadeIn(subtitle))
        cols=[-4.5,-1.5,1.5,4.5]
        cards=VGroup()
        for j,(doc,click) in enumerate([("A","click"),("A","no click"),("B","click"),("B","no click")]):
            rect=RoundedRectangle(width=2.45,height=1.45,corner_radius=.12,stroke_color=GRAY_C if doc=="A" else BLUE_B,fill_color="#222b45",fill_opacity=1).move_to([cols[j],.45,0])
            txt=VGroup(Text(doc,font_size=37),Text(click,font_size=23)).arrange(DOWN,buff=.08).move_to(rect)
            cards.add(VGroup(rect,txt))
        self.play(LaggedStart(*[FadeIn(c,shift=.2*UP) for c in cards],lag_ratio=.18))
        label=Text("The new policy always shows B.",font_size=32).move_to([0,-.85,0])
        self.play(Write(label),cards[0].animate.set_opacity(.22),cards[1].animate.set_opacity(.22))
        self.wait(.8)
        weights=VGroup(*[Text(t,font_size=30,color=BLUE_B if j>=2 else GRAY_C).move_to([cols[j],-1.65,0]) for j,t in enumerate(["weight 0","weight 0","weight 4","weight 4"])])
        self.play(LaggedStart(*[FadeIn(x) for x in weights],lag_ratio=.15))
        why=Text("Old policy shows B one time in four: 1 / ¼ = 4.",font_size=27).move_to([0,-2.45,0])
        self.play(FadeIn(why))
        self.wait(1.2)
        result=Text("Same weighted clicks. Different denominators.",font_size=30,color=BLUE_B).move_to([0,-3.25,0])
        self.play(Write(result))
        self.wait(1.8)
