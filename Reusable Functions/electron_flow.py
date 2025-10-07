from manim import *

class ElectronFlow(Scene):
    def construct(self):
        # Example usage of the function
        conductor = Line((-10,0,0), (10,0,0), color=ORANGE)
        self.add(conductor)

        # Call reusable function
        electron_flow = self.animate_electron_flow(conductor,
                                   num_electrons=12,
                                   drift_speed=0.02,
                                   signal_speed=0.2)

        self.play(electron_flow) #play the animation

    def animate_electron_flow(self, conductor,
                              num_electrons=10,
                              drift_speed=0.2,
                              signal_speed=2.0):
        # Create electrons
        electrons = VGroup(*[
            Dot(color=BLUE, radius=0.08).move_to(
                conductor.point_from_proportion(i / (num_electrons - 1))
            )
            for i in range(num_electrons)
        ])
        self.add(electrons)

        # Define drift animation along the conductor
        electron_anims = [
            MoveAlongPath(e, conductor, rate_func=linear)
            for e in electrons
        ]

        # Return a combined animation instead of playing it here
        return AnimationGroup(*electron_anims, run_time=1 / drift_speed, lag_ratio=0.3)

