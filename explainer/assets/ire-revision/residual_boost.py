from manim import *

class ResidualBoost(Scene):
    def construct(self):
        self.camera.background_color = "#101827"
        title = Text("Boosting: fit the errors left over",font_size=46,weight=BOLD).to_edge(UP)
        self.add(title)
        labels = ("x","Target","Prediction","Residual")
        pos = (-4.8,-2.4,.3,3.95)
        hdr = VGroup(*[Text(s,font_size=25,weight=BOLD,color=BLUE_A).move_to([p,2,0]) for s,p in zip(labels,pos)])
        bar = Line([-5.25,1.66,0],[5.25,1.66,0],stroke_width=2,color=GRAY)
        def rows(pred,res):
            return VGroup(*[Text(f"{v:g}".replace("-","−"),font_size=34,color=c).move_to([p,yp,0])
               for i,yp in enumerate((1.13,.25,-.63))
               for v,p,c in zip((i,2*i,pred[i],res[i]),pos,(WHITE,WHITE,TEAL_A,GOLD_A))])
        def foot(title, detail, sse):
            heading=Text(title,font_size=31).move_to([0,-1.55,0])
            detail=Text(detail,font_size=24,color="#B5C2D4").move_to([0,-2.24,0])
            score=Text("Sum of squared errors: "+sse,font_size=29,color=TEAL_A).move_to([0,-3.0,0])
            return VGroup(heading,detail,score)
        data=[
          ((2,2,2),(-2,0,2), ("Start at the mean target: 2","Residual = target − current prediction","8")),
          ((1,2.5,2.5),(-1,-.5,1.5), ("Tree 1: split at x < 1","Add half the leaf output:  (−1, +0.5, +0.5)","3.5")),
          ((.625,2.125,3.25),(-.625,-.125,.75), ("Tree 2: split at x < 2","Fit the new residuals, then add  (−0.375, −0.375, +0.75)","0.96875")),
        ]
        prev_rows,prev_foot=rows(*data[0][:2]),foot(*data[0][2])
        self.play(FadeIn(hdr,bar,prev_rows,prev_foot),run_time=.8)
        self.wait(2.4)
        for pred,res,msg in data[1:]:
            new_rows,new_foot=rows(pred,res),foot(*msg)
            self.play(ReplacementTransform(prev_rows,new_rows),ReplacementTransform(prev_foot,new_foot),run_time=1.05)
            self.wait(2.6)
            prev_rows,prev_foot=new_rows,new_foot
        final=Text("This is training error on three rows, not a test result.",font_size=25,color=GOLD_A).move_to([0,-2.24,0])
        self.play(ReplacementTransform(prev_foot[1],final),run_time=.45)
        self.wait(2)
