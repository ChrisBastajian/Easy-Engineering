from manim import *

class VoltageSource(Scene):
    def construct(self):
        source = self.construct_vsource()
        self.add(source)
    @staticmethod
    def construct_vsource():
        circle = Circle().set_stroke(width=5, color=WHITE)
        plus_sign = MathTex("+", fill_color=RED)
        minus_sign = MathTex("-", fill_color=BLUE)

        #Repositioning
        plus_sign.next_to(circle.get_top(), DOWN*1.5)
        minus_sign.next_to(circle.get_bottom(), UP*1.5)

        voltage_source = VGroup(circle, plus_sign, minus_sign)
        return voltage_source

