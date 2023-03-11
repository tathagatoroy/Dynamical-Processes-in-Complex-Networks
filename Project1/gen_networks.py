import numpy as np

def gen_erdos_network(N, p):
    """
    Generates a Erdos Renyi Network and returns an adjacency matrix of size NxN wherein it assigns a value of 1 to the matrix with probability p
    """
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            if np.random.random() < p:
                A[i, j] = 1

    return A

def gen_scale_free_network(N, m0):
    """
    Generates a scale free network based on the Barabasi model
    We start off with m0 nodes in the network and create arbitrary links between these m0 nodes
    Then we keep adding N - m0 nodes one by one
    Each time we add a node, we randomly create an edge with all the current nodes based on a certain probability distribution
    """
    A = np.zeros((N, N))
    degrees = np.zeros(N)

    # Creating arbitrary links between the m0 nodes
    # We will follow a Erdos Renyi model and create these arbitrary links
    p = 0.4
    for i in range(m0):
        for j in range(i + 1, m0):
            if np.random.random() < p:
                A[i, j] = 1
                degrees[i] += 1
                degrees[j] += 1

    # Now we create links from the remaining m0 nodes
    for i in range(m0, N):
        for j in range(i):
            if np.random.random() < (degrees[j]/degrees.sum()):
                A[i, j] = 1
                degrees[i] += 1
                degrees[j] += 1

    return A
