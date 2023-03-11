import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.scatter([0.1,0.2, 0.3], [9,8,4], marker="o", color="orange")
ax.scatter([0.1,0.2, 0.3], [7,6,2], marker="^", color="blue")

plt.show()