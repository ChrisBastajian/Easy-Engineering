from manim import *

class ElectronFlow(Scene):
    def construct(self):
        v_source = self.construct_vsource().scale(0.5).move_to(LEFT*3)

        light_bulb = SVGMobject("light_bulb.svg").scale(0.5).move_to(RIGHT * 3)
        self.add(v_source, light_bulb)

        # Top wire
        top_wire = VMobject()
        top_wire.set_points_as_corners([
            light_bulb.get_top(),  # start on top of the bulb
            light_bulb.get_top() + UP * 2.0,
            v_source.get_top() + UP * 2.0,
            v_source.get_top() #end on top of the voltage source
        ])
        top_wire.set_color(ORANGE).set_stroke(width=5)

        # Bottom wire
        bottom_wire = VMobject()
        bottom_wire.set_points_as_corners([
            v_source.get_bottom(),  #start below source
            v_source.get_bottom() + DOWN * 2.0,
            light_bulb.get_bottom() + DOWN * 2.0,
            light_bulb.get_bottom(), #end below bulb

        ])
        bottom_wire.set_color(ORANGE).set_stroke(width=5)

        self.add(top_wire, bottom_wire)

        #Getting the animations (running top and bottom at the same time):
        e_group1 = self.animate_electron_flow(top_wire, num_electrons=30, speed=0.02, direction=1)
        e_group2 = self.animate_electron_flow(bottom_wire, num_electrons=30, speed=0.02, direction=1)

        self.wait(5)

        #Showing current:
        # Getting the animations (running top and bottom at the same time):
        i_group1 = self.animate_current(top_wire, num_arrows=5, speed=0.2, direction=-1, arrow_length=2)
        i_group2 = self.animate_current(bottom_wire, num_arrows=5, speed=0.2, direction=-1, arrow_length=2)

        # Let the updaters run
        self.wait(5)

        # Making the electrons disappear:
        for mob in (*e_group1, *e_group2):
            mob.add_updater(lambda m, dt: None)  # keeps it "live" until fade ends

        self.play(
            *[mob.animate.set_opacity(0) for mob in (*e_group1, *e_group2)],
            run_time=2.0
        )

        # Removing e_groups from scene after fade completes
        for mob in (*e_group1, *e_group2):
            mob.clear_updaters()
            self.remove(mob)

        self.wait(5)

        #Showing function i(t)
        i_ltx = MathTex("i(t)", fill_color=YELLOW).next_to(top_wire, UP * 0.2)

        # Animate arrows fading out while text appears
        self.play(
            AnimationGroup(
                *[FadeOut(a) for a in (*i_group1, *i_group2)],
                FadeIn(i_ltx),
                lag_ratio=0
            )
        )
        self.wait(3)

    def animate_electron_flow(self, conductor, num_electrons=10, speed=0.15, direction=1):
        # Local helper for this conductor only
        def point_along_wire(wire, proportion):
            pts = wire.get_points()
            seg_lengths = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
            total_length = sum(seg_lengths)
            target_length = proportion * total_length
            acc = 0
            for i, seg_len in enumerate(seg_lengths):
                if acc + seg_len >= target_length:
                    local_prop = (target_length - acc) / seg_len
                    return pts[i] * (1 - local_prop) + pts[i + 1] * local_prop
                acc += seg_len
            return pts[-1]

        # Create electrons
        electrons = VGroup()
        for i in range(num_electrons):
            e = Dot(color=BLUE, radius=0.08)
            e.proportion = i / num_electrons
            e.move_to(point_along_wire(conductor, e.proportion))
            electrons.add(e)
        self.add(electrons)

        # Define updater — bound to *this* conductor and direction
        def electron_updater(mob, dt):
            mob.proportion += direction * speed * dt
            if mob.proportion > 1:
                mob.proportion -= 1
            elif mob.proportion < 0:
                mob.proportion += 1
            mob.move_to(point_along_wire(conductor, mob.proportion))

        for e in electrons:
            e.add_updater(electron_updater)

        return electrons

    def animate_current(self, conductor, num_arrows=10, speed=0.15, direction=1, arrow_length=5.0):
        """
        Animate current along a conductor using arrows.

        Parameters:
            conductor: VMobject - the wire/path
            num_arrows: int - number of arrows along the wire
            speed: float - proportion per second (how fast the arrows move)
            direction: int - 1 for forward, -1 for backward
            arrow_length: float - length of each arrow
        """

        def point_along_wire(wire, proportion):
            pts = wire.get_points()
            seg_lengths = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
            total_length = sum(seg_lengths)
            target_length = proportion * total_length
            acc = 0
            for i, seg_len in enumerate(seg_lengths):
                if acc + seg_len >= target_length:
                    local_prop = (target_length - acc) / seg_len
                    return pts[i] * (1 - local_prop) + pts[i + 1] * local_prop
                acc += seg_len
            return pts[-1]

        # Create arrows
        arrows = VGroup()
        for i in range(num_arrows):
            arrow = Arrow(
                start=ORIGIN,
                end=RIGHT * arrow_length,
                buff=0,
                stroke_width=3,
                color=YELLOW
            )
            arrow.proportion = i / num_arrows
            arrow.move_to(point_along_wire(conductor, arrow.proportion))
            arrows.add(arrow)
        self.add(arrows)

        # Updater function for each arrow
        def arrow_updater(mob, dt):
            mob.proportion += direction * speed * dt
            if mob.proportion > 1:
                mob.proportion -= 1
            elif mob.proportion < 0:
                mob.proportion += 1

            # Move arrow to the new position
            start_point = point_along_wire(conductor, mob.proportion)

            # Determine approximate tangent direction along wire
            tangent_prop = mob.proportion + 0.01 * direction
            # Clamp to [0, 1]
            tangent_prop = min(max(tangent_prop, 0), 1)
            tangent_point = point_along_wire(conductor, tangent_prop)

            direction_vec = tangent_point - start_point
            if np.linalg.norm(direction_vec) == 0:
                direction_vec = RIGHT
            mob.put_start_and_end_on(start_point, start_point + direction_vec)

        for a in arrows:
            a.add_updater(arrow_updater)

        return arrows

    @staticmethod
    def construct_vsource():
        circle = Circle().set_stroke(width=5, color=WHITE)
        plus_sign = MathTex("+", fill_color=RED).set_stroke(width=7, color=RED)
        minus_sign = MathTex("-", fill_color=BLUE).set_stroke(width=7, color=BLUE)

        #Repositioning
        plus_sign.next_to(circle.get_top(), DOWN*1.5)
        minus_sign.next_to(circle.get_bottom(), UP*1.5)

        voltage_source = VGroup(circle, plus_sign, minus_sign)
        return voltage_source