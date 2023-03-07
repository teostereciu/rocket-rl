import matplotlib.pyplot as plt
import re


def draw_line():
    # create a figure where you can trace the track lines with points
    # each 10 points will make a line
    ax = plt.gca()
    xy = plt.ginput(10)
    x = [p[0] for p in xy]
    y = [p[1] for p in xy]
    line = plt.plot(x, y)
    ax.figure.canvas.draw()
    # write line coordinates to a string
    global f_coords
    f_coords += ' '.join(map(str, xy)) + '\n'
    plt.savefig("map.png")


def on_close(evt):
    global close_flag, f_coords
    close_flag = 1
    # print(f_coords)
    # write all line coordinates to a file (only the numbers)
    f_coords = re.sub("\(\)", "", f_coords)
    with open('coords.txt', 'w') as f:
        f.write(f_coords)
    exit()


f_coords = ''
close_flag = 0

fig = plt.figure(figsize=(16, 10))
plt.xlim(0, 1600)
plt.ylim(0, 1000)
fig.canvas.mpl_connect('close_event', on_close)

for _ in range(10):
    if close_flag == 0:
        draw_line()
    else:
        break
