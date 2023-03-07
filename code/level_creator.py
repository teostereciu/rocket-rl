import matplotlib.pyplot as plt
import re
import numpy as np
from PIL import Image
import sys

# Run this with argument 'tracks' to draw the map or
# with argument 'goals' to draw the goals.
#


def draw_lines(n, fig_name):
    # create a figure where you can trace the track lines with points
    # each n points will make a line
    ax = plt.gca()
    xy = plt.ginput(n)
    x = [p[0] for p in xy]
    y = [p[1] for p in xy]
    plt.plot(x, y)
    ax.figure.canvas.draw()
    # write line coordinates to a string
    global f_coords
    f_coords += ' '.join(map(str, xy)) + '\n'
    plt.savefig(fig_name)


def on_close(event):
    global close_flag, f_coords
    close_flag = 1
    # write all line coordinates to a file (only the numbers)
    f_coords = re.sub("\(", "", f_coords)
    f_coords = re.sub("\)", "", f_coords)
    f_coords = re.sub(",", "", f_coords)
    # print(f_coords)
    if sys.argv[1] == "tracks":
        filename = "coords.txt"
    else:
        filename = "goals.txt"
    with open(filename, 'w') as f:
        f.write(f_coords)
    exit()


f_coords = ''
close_flag = 0

if len(sys.argv) == 1:
    print("Missing argument. Please choose from 'tracks' and 'goals'.")
    exit()
elif sys.argv[1] == "tracks":
    # Draw tracks
    fig = plt.figure(figsize=(10, 6))
    plt.xlim(0, 1600)
    plt.ylim(0, 1000)
    fig.canvas.mpl_connect('close_event', lambda event: on_close(event))

    for _ in range(10):
        if close_flag == 0:
            draw_lines(10, "map.png")
        else:
            break
elif sys.argv[1] == "goals":
    # Draw goals
    # crop tracks map
    uncropped = Image.open(r"map.png")
    left = 130
    top = 80
    right = 860
    bottom = 530
    cropped = uncropped.crop((left, top, right, bottom))
    cropped.save("map_cropped.png")
    tracks = plt.imread("map_cropped.png")
    fig = plt.figure(figsize=(10, 6))
    plt.xlim(0, 1600)
    plt.ylim(0, 1000)
    plt.imshow(tracks, extent=[0, 1600, 0, 1000])
    fig.canvas.mpl_connect('close_event', lambda event: on_close(event))
    for _ in range(15):
        if close_flag == 0:
            draw_lines(2, "map_with_goals.png")
        else:
            break

else:
    print("Invalid argument. Please choose from 'tracks' and 'goals'.")
    exit()
