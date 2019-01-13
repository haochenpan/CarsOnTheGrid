import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pickle
import time
from matplotlib.widgets import Button

pause = True

idx = 0


def on_click(event):
    print("pressed")
    global pause
    pause ^= True


def gen():
    global idx
    while True:
        # time.sleep(0.1)
        yield idx
        if not pause:
            idx += 1
            idx = idx % len(offsets)


def _update(idx):
    scat.set_offsets(offsets[idx])


ls_1_x = np.linspace(0, 0, num=50)
ls_1_y = np.linspace(0, 3, num=50)
ls_2_x = np.linspace(1, 2, num=50)
ls_2_y = np.linspace(0, 2, num=50)
ls_1 = np.column_stack((ls_1_x, ls_1_y))
ls_2 = np.column_stack((ls_2_x, ls_2_y))
ls = np.stack([ls_1, ls_2, ls_1], axis=1)
offsets = ls
print(ls)
fig = plt.figure(figsize=(10, 10))
# fig.canvas.mpl_connect('button_press_event', on_click)
ax = fig.add_subplot(111, xlim=[-1, 11], ylim=[11, -1])
ax.xaxis.tick_top()
ax.set_xticks(np.arange(-1, 12, 1))
ax.set_yticks(np.arange(-1, 12, 1))

xs, ys = [0, 1], [0, 0]
# scat = plt.scatter(xs, ys, c=xs)
scat = plt.scatter(xs, ys)
scat.set_alpha(0.8)

anim = animation.FuncAnimation(fig, _update, gen, blit=False, interval=25, repeat=True)
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(on_click)
plt.show()

# if __name__ == '__main__':
#     pass

# with open('g.pickle', 'rb') as handle:
#     g, b = pickle.load(handle)
# round_ctr = 0
# for pos, cars in g.items():
#     for car in cars:
#         curr_pos = car['trace'][0]
#         print(curr_pos)
#         x.append(curr_pos[1][0])

#         y.append(curr_pos[1][1])
