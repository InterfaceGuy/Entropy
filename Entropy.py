from manim import *
from manim_physics import *
import random

RED = "#FF644E"
BLUE = "#00a2ff"


class SpiritualEntropy(SpaceScene):
    GRAVITY = 0, -0  # Set gravity to 0 to create a zero-gravity environment
    
    def construct(self):
        # create two semi circles forming a circle with horizontal cut
        semi_circle1 = Arc(radius=0.5, start_angle=0, angle=PI, stroke_width=4)
        semi_circle2 = Arc(radius=0.5, start_angle=PI, angle=PI, stroke_width=4)
        # create circle
        circle = Circle(radius=1/8)
        # create square
        square = Square(side_length=1/4)
        square.rotate(PI/4)
        
        # shift the upper semi circle with circle to the right and the lower with the square to the left by half their radius
        semi_circle1.shift(0.5*RIGHT)
        circle.shift(0.5*RIGHT)
        semi_circle2.shift(0.5*LEFT)
        square.shift(0.5*LEFT+0.01*DOWN)
        # combine the two semi circles
        s_curve = VGroup(semi_circle1, semi_circle2, circle, square)
        # tilt s curve by 45 degrees
        s_curve.rotate(PI/4)
        # scale s curve
        s_curve.scale(3)

        # create a set of equidistant dots along the s curve
        upper_arc = VGroup()
        for i in range(1, 50):
            dot = Dot(point=semi_circle1.point_from_proportion(i/49))
            upper_arc.add(dot)
        lower_arc = VGroup()
        for i in range(1, 50):
            dot = Dot(point=semi_circle2.point_from_proportion(i/49))
            lower_arc.add(dot)

        # combine dots into one flat group
        full_symbol = VGroup(*[*upper_arc.submobjects, *lower_arc.submobjects, circle, square])

        # Create a grid of squares overlay
        overlay = self.create_grid_overlay(full_symbol)

        ground = Line([-3.5, -3.5, 0], [3.5, -3.5, 0])
        ceiling = Line([-3.5, 3.5, 0], [3.5, 3.5, 0])
        wall1 = Line([-3.5, -3.5, 0], [-3.5, 3.5, 0])
        wall2 = Line([3.5, -3.5, 0], [3.5, 3.5, 0])
        walls = VGroup(ground, ceiling, wall1, wall2)
        self.add(walls)

        # Add the object and its overlay to the scene
        self.play(Create(overlay, run_time=3, lag_ratio=0.0005))

        # make the squares rigid and give them a random initial velocity
        for square in overlay:
            self.make_rigid_body(square)  
            # Set a random initial velocity for the body of the square
            square.body.velocity = random.uniform(-.1, .1), random.uniform(-.1, .1)

        self.make_static_body(walls)  # Mobjects will stay in place
        self.wait(1)
        self.make_rigid_body(*overlay)
        self.wait(30)

    def create_grid_overlay(self, mobject, square_size=0.05):
        # Determine the width and height of the mobject
        width = mobject.width
        height = mobject.height

        # Calculate the number of squares in each dimension
        squares_x = int(width / square_size)
        squares_y = int(height / square_size)

        # Create a grid of squares
        squares = VGroup()
        for i in range(squares_x+1):
            for j in range(squares_y+1):
                square = Square(square_size, stroke_width=1, color=BLUE)
                square.move_to(mobject.get_center() + square_size * np.array([i - squares_x / 2, j - squares_y / 2, 0]))
                
                # check if group
                if isinstance(mobject, VGroup):
                    # loop over all submobjects
                    for submob in mobject:

                        # check if the square intersects with the object
                        intersection = Intersection(submob, square)
                        if len(intersection) > 0: # if there is an intersection
                            squares.add(square)
                else:
                    # Check if the square intersects with the object
                    intersection = Intersection(mobject, square)
                    if len(intersection) > 0:  # If there is an intersection
                        squares.add(square)

        return squares