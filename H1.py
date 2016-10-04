import collections
import itertools
from collections import defaultdict

import networkx as nx


def write_edges():
    edges_file = open('H1.edges', 'w')
    for i in range(1, 15):
        string_to_write = "{} {}\n".format(i, i + 1)
        edges_file.write(string_to_write)
    for i in range(1, 12):
        string_to_write = "{} {}\n".format(i, i + 4)
        edges_file.write(string_to_write)


def create_graph():
    G = nx.Graph()
    edges_file = open('H1.edges', 'r')

    for edge in edges_file:
        nodes = edge.split(" ")
        G.add_edge(int(nodes[0]), int(nodes[1]))

    return G


def get_all_number_shortest_path():
    value = list(range(1, 17))
    for node_1, node_2 in itertools.combinations(value, 2):
        print "Shortest path for {}, {} -->{}".format(node_1, node_2, len(
            [p for p in nx.all_shortest_paths(create_graph(), node_1, node_2) if 7 in p]))

    print nx.betweenness_centrality(create_graph(),normalized=False)
