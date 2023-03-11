"""
For a given network, we calculate 2 things
1.
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

N = 1000
p = 0.02
erdos = nx.fast_gnp_random_graph(N, p)
erdos_deg_dist = np.array(nx.degree_histogram(erdos))
print(f"Erdos: {erdos_deg_dist @ np.arange(len(erdos_deg_dist))/N}")
print(f"Erdos: {nx.diameter(erdos)}")
# fig, (ax1, ax2) = plt.subplots(2, 1)
# ax1.bar(range(len(erdos_deg_dist)), erdos_deg_dist)

m0 = 10
scale_free = nx.barabasi_albert_graph(N, m0)
sf_deg_dist = nx.degree_histogram(scale_free)
print(f"Scale Free: {sf_deg_dist @ np.arange(len(sf_deg_dist))/N}")
print(f"Scale Free: {nx.diameter(scale_free)}")
# ax2.bar(range(len(sf_deg_dist)), sf_deg_dist)
# plt.show()


def disturb_network(G, nodes_to_remove):

    newG = G.copy()
    newG.remove_nodes_from(nodes_to_remove) 
    print(newG)
    return nx.average_shortest_path_length(newG)

err_erdos_dia = []
err_sf_dia = []
# Error tolerance
for f in np.linspace(0, 0.04, 20):
    print(f"Removing {f*100}% of nodes uniformly")
    num_nodes_remove = int(f * N)
    # sample num_nodes_remove from the graph
    nodes_to_remove = np.random.choice(np.arange(N), size=num_nodes_remove, replace=False)
    print(f"Removing {nodes_to_remove}")
    # Remove those nodes
    new_diameter = disturb_network(erdos, nodes_to_remove)
    print(f"The new diameter for erdos is {new_diameter}")
    err_erdos_dia.append(new_diameter)
    new_diameter = disturb_network(scale_free, nodes_to_remove)
    print(f"The new diameter for scale-free is {new_diameter}")
    err_sf_dia.append(new_diameter)

print(err_erdos_dia)
print(err_sf_dia)

# Attack tolerance
att_erdos_dia = []
att_sf_dia = []

for f in np.linspace(0, 0.04, 20):
    print(f"Attacking {f*100}% of nodes uniformly")
    num_connected_nodes_remove = int(f * N)

    # Attack nodes of the erdos graph
    erdos_degrees = np.array([deg for _, deg in erdos.degree(range(N))])
    erdos_probs = erdos_degrees/erdos_degrees.sum()
    nodes_to_remove_erdos = np.random.choice(np.arange(N), size=num_connected_nodes_remove, replace=False, p=erdos_probs)
    new_diameter = disturb_network(erdos, nodes_to_remove_erdos)
    print(f"The new diameter for erdos is {new_diameter}")
    att_erdos_dia.append(new_diameter)

    # Attack nodes of the scale free graph
    sf_degrees = list(scale_free.degree(range(N)))
    sf_degrees.sort(key=lambda a: a[1], reverse=True)
    # sf_probs = sf_degrees/sf_degrees.sum()
    # nodes_to_remove_sf = np.random.choice(np.arange(N), size=num_connected_nodes_remove, replace=False, p=sf_probs)
    nodes_to_remove_sf = [x for x,_ in sf_degrees[:num_connected_nodes_remove]]
    new_diameter = disturb_network(scale_free, nodes_to_remove_sf)
    print(f"The new diameter for scale-free is {new_diameter}")
    att_sf_dia.append(new_diameter)


fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.scatter(np.linspace(0, 0.04, 20), err_erdos_dia, color="orange", label="erdos", marker = "^")
ax1.scatter(np.linspace(0, 0.04, 20), err_sf_dia, color="blue", label="scale-free", marker="o")
ax1.set_title("Error tolerance")
ax1.set_ylabel("Diameter")
ax1.legend()
ax1.grid()
ax1.set_xlabel("f")

ax2.scatter(np.linspace(0, 0.04, 20), att_erdos_dia, color="orange", label="erdos", marker = "^")
ax2.scatter(np.linspace(0, 0.04, 20), att_sf_dia, color="blue", label="scale-free", marker="o")
ax2.set_title("Attack tolerance")
ax2.set_ylabel("Diameter")
ax2.legend()
ax2.grid()
ax2.set_xlabel("f")

plt.show()