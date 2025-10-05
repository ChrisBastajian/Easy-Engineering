from manim import *

class ElectronFlow(Scene):
    def construct(self):
        # Example usage of the function
        conductor = Line((-10,0,0), (10,0,0), color=ORANGE)
        self.add(conductor)

        # Call reusable function
        self.animate_electron_flow(conductor,
                                   num_electrons=12,
                                   drift_speed=0.02,
                                   signal_speed=0.2)

    def animate_electron_flow(self, conductor: Line,
                              num_electrons=10,
                              drift_speed=0.2,
                              signal_speed=2.0):
        #Animates electrons moving through a conductor

        # Place electrons evenly spaced along the conductor
        electrons = VGroup(*[
            Dot(color=BLUE, radius=0.08).move_to(
                conductor.point_from_proportion(i / (num_electrons - 1))
            )
            for i in range(num_electrons)
        ])
        self.add(electrons)

        # Drift motion of electrons
        electron_anims = []
        for e in electrons:
            # Move right across the conductor very slowly
            target = e.copy().shift(RIGHT * 4)
            electron_anims.append(MoveAlongPath(e, conductor, rate_func=linear))

        # Play both animations simultaneously
        self.play(
            AnimationGroup(*electron_anims, run_time=1 / drift_speed, lag_ratio=0.3),
            run_time=1 / signal_speed
        )
        self.wait()

