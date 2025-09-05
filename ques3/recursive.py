# Import required libraries
import turtle as T
import math

# Recursive edge: inward indentation rule
def inward_koch_edge(t, length, depth):
    if depth == 0:
        t.forward(length)
        return

    seg = length / 3.0
    inward_koch_edge(t, seg, depth - 1)
    t.right(60)      # turn inside
    inward_koch_edge(t, seg, depth - 1)
    t.left(120)      # make the indentation peak
    inward_koch_edge(t, seg, depth - 1)
    t.right(60)      # realign direction
    inward_koch_edge(t, seg, depth - 1)

# Draw full polygon with recursive edges
def draw_inward_koch_polygon(n_sides, side_len, depth):
    t = T.Turtle(visible=False)
    t.speed(0)
    t.pensize(2)

    # Calculate exterior angle
    exterior = 360.0 / n_sides

    # Scale view so drawing fits in the window
    R = side_len / (2.0 * math.sin(math.pi / n_sides))
    pad = (4.0 / 3.0) ** depth
    T.setworldcoordinates(-1.2*R*pad, -1.2*R*pad, 1.2*R*pad, 1.2*R*pad)

    # Position turtle at a neat start point
    t.penup()
    t.goto(-R * 0.8, 0)
    t.setheading(0)
    t.pendown()
    t.showturtle()

    # Draw all sides with recursive edges
    for _ in range(n_sides):
        inward_koch_edge(t, side_len, depth)
        t.right(exterior)

# Main program: get input and run
def main():
    try:
        n = int(input("Enter the number of sides: ").strip())
        L = float(input("Enter the side length: ").strip())
        d = int(input("Enter the recursion depth: ").strip())
        if n < 3 or d < 0 or L <= 0:
            raise ValueError
    except ValueError:
        print("Please enter: sides >= 3, length > 0, depth >= 0.")
        return

    # Create screen
    screen = T.Screen()
    screen.title("Recursive Inward-Indentation Pattern")

    # Draw polygon
    draw_inward_koch_polygon(n, L, d)

    print("Drawing complete successfully. Close the window to exit.")
    T.done()

# Run the program
if __name__ == "__main__":
    main()

