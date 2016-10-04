import collections
import itertools
from collections import defaultdict

import networkx as nx


def get_stats_of_all_ego_network():
    ego_list = [0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980]
    for ego in ego_list:
        print "================Stats for ego network:{}=======================".format(ego)
        calculate_graph_parameters(ego)
        print "================Hypothesis data for ego network:{}==============".format(ego)
        compare_circle_features(ego)


def build_graph(ego_node_number):
    G = nx.Graph()
    edges_file = open('{}.edges'.format(ego_node_number), 'r')

    for edge in edges_file:
        nodes = edge.split(" ")
        G.add_edge(int(nodes[0]), int(nodes[1]))

    return G


def calculate_graph_parameters(ego_node_number):
    g = build_graph(ego_node_number)
    for node in g.nodes():
        g.add_edge(0, node)

    print "Nodes:{}".format(g.number_of_nodes())
    print "Edges:{}".format(g.number_of_edges())
    print "Average Clustering:{}".format(nx.average_clustering(g))
    print "Betweenness Centrality of ego node:{}".format(nx.betweenness_centrality(g, normalized=False)[0])


def get_edges_file(ego_node_number):
    return "{}.edges".format(ego_node_number)


def get_features_node_file(ego_node_number):
    return "{}.feat".format(ego_node_number)


def get_features_name_file(ego_node_number):
    return "{}.featnames".format(ego_node_number)


def get_circle_file(ego_node_number):
    return "{}.circles".format(ego_node_number)


def get_features_node_ego_file(ego_node_number):
    return "{}.egofeat".format(ego_node_number)


def get_feature_name_hashmap(ego_node_number):
    feature_name_file = open(get_features_name_file(ego_node_number), 'r')
    feature_number_name_hashmap = {}
    for feature in feature_name_file:
        feature_array = feature.split(" ")
        feature_number_name_hashmap[int(feature_array[0])] = feature_array[1]

    return feature_number_name_hashmap


def get_feature_node_hashmap(ego_node_number):
    feature_node_file = open(get_features_node_file(ego_node_number))
    feature_node_hashmap = defaultdict(list)
    feature_name_hashmap = get_feature_name_hashmap(ego_node_number)
    for feature_node in feature_node_file:
        count = 0
        feature_node_array = feature_node.split(" ")
        for feature in feature_node_array[1:]:
            if int(feature) == 1:
                feature_node_hashmap[int(feature_node_array[0])].append(feature_name_hashmap[count])
            count += 1
    return feature_node_hashmap


def compare_circle_features(ego_node_number):
    circle_file = open(get_circle_file(ego_node_number), 'r')
    circle_hashmap = {}
    circle_common_features_count = defaultdict(int)
    shortest_path = []
    no_path_count = 0
    features_node_hashmap = get_feature_node_hashmap(ego_node_number)
    g = build_graph(ego_node_number)
    for circle in circle_file:
        circle_array = circle.split('\t')
        circle_hashmap[circle_array[0]] = circle_array[1:]

    for key, value in circle_hashmap.iteritems():
        for node_1, node_2 in itertools.combinations(value, 2):
            # find common characterstics
            node_1_features = features_node_hashmap[int(node_1)]
            node_2_features = features_node_hashmap[int(node_2)]
            try:
                shortest_path.append(nx.shortest_path_length(g, int(node_1), int(node_2)))
            except nx.NetworkXError:
                pass
            except nx.NetworkXNoPath:
                no_path_count += 1

            for common_nodes in set(node_1_features).intersection(set(node_2_features)):
                circle_common_features_count[common_nodes] += 1

    print circle_common_features_count
    # print shortest_path

    shortest_path_length_frequency = collections.Counter(shortest_path)
    print shortest_path_length_frequency


if __name__ == "__main__":
    get_stats_of_all_ego_network()
