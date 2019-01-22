import matplotlib.pyplot as plt
import pickle

fig, ax = plt.subplots(figsize=(12, 12))
# fig25.add_subplot(111)

with open('stats.pickle', 'rb') as handle:
    stats = pickle.load(handle)
x, y = [], []
for key in sorted(stats):
    x.append(key)
    y.append(stats[key])
ax.scatter(x, y, alpha=0.8)

for i, d in enumerate(y):
    ax.annotate(d, (x[i], y[i]), size=8)
plt.show()
# plt.savefig('30000.png')

