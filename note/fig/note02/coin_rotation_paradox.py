import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
from matplotlib.transforms import Affine2D
import os; os.chdir(os.path.dirname(__file__))

# Set the radii
R = 1.5  # Radius of the outer (stationary) coin
r = 0.5  # Radius of the inner (rolling) coin

def create_logo(ax, x, y, radius, angle):
    # Create a simple smiley face logo
    face = Circle((0, 0), radius * 0.7, fill=True, color="cyan")
    left_eye = Circle((-radius * 0.3, radius * 0.2), radius * 0.1, fill=True, color="black")
    right_eye = Circle((radius * 0.3, radius * 0.2), radius * 0.1, fill=True, color="black")
    mouth = Wedge((0, 0), radius * 0.5, 225, 315, width=radius * 0.1, color="black")

    # Create a transformation
    t = Affine2D().rotate(-angle).translate(x, y) + ax.transData

    # Apply the transformation to all elements
    face.set_transform(t)
    left_eye.set_transform(t)
    right_eye.set_transform(t)
    mouth.set_transform(t)

    ax.add_artist(face)
    ax.add_artist(left_eye)
    ax.add_artist(right_eye)
    ax.add_artist(mouth)

def create_frame(angle):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Set limits and aspect ratio
    ax.set_xlim(-(R + r + 1), R + r + 1)
    ax.set_ylim(-(R + r + 1), R + r + 1)
    ax.set_aspect("equal")

    # Remove axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Calculate position of the rolling coin's center
    x = (R + r) * math.cos(angle)
    y = (R + r) * math.sin(angle)

    # Calculate position of the point on the edge of the moving coin
    point_x = x + r * math.cos((R + r) / r * angle)
    point_y = y + r * math.sin((R + r) / r * angle)

    # Draw stationary coin
    stationary_coin = Circle((0, 0), R, fill=False, color="blue")
    ax.add_artist(stationary_coin)

    # Draw rotating coin
    rotating_coin = Circle((x, y), r, fill=False, color="red")
    ax.add_artist(rotating_coin)

    # Add logo to the rotating coin
    create_logo(ax, x, y, r, (R + r) / r * angle)

    # Draw point on the edge of the moving coin
    ax.plot(point_x, point_y, "ro")

    # Draw cardioid path
    theta = [i * 2 * math.pi / 100 for i in range(int(100 * angle / (2 * math.pi)) + 1)]
    cardioid_x = [(R + r) * math.cos(t) + r * math.cos((R + r) / r * t) for t in theta]
    cardioid_y = [(R + r) * math.sin(t) + r * math.sin((R + r) / r * t) for t in theta]
    ax.plot(cardioid_x, cardioid_y, "g-")

    # Add title
    ax.set_title(f"Rotation: {angle/(2*math.pi)*360:.1f}°")
    
    return fig

# Generate 512 frames
num_frames = 512; tex = []
for i in range(num_frames):
    angle = i * 2 * math.pi / num_frames
    fig = create_frame(angle)
    fig.savefig(f'coin_rotation_{i}.pdf', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close(fig)
    tex.append(f'\\only<{i + 1}>{{\\includegraphics[width=.6\\textwidth]{{fig/note02/coin_rotation_{i}.pdf}}\\noindent}}')
open('../../coin.tex', 'w').write(f"\\hspace*{{\\dimexpr(\\textwidth - .6\\textwidth)/2\\relax}}\n\\begin{{overlayarea}}{{\\textwidth}}{{0.7\\textheight}}\n{'\n'.join(tex)}\n\\end{{overlayarea}}") 
