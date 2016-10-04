from collections import defaultdict

from py2neo import Graph, Relationship, authenticate, Node, NodeSelector


def build_nodes():
    


    authenticate("localhost:7474", "neo4j", "jonty1")
    graph = Graph()
    graph.delete_all()
    tx = graph.begin()
    node_file = open('0.edges', 'r')
    node_map = defaultdict()

    feature_node_map = assign_features_to_node()
    circle_node_map = assign_circles()

    ego_features = assign_features_to_node_ego()
    ego_node = Node("ego", features=ego_features[0])
    tx.create(ego_node)
    for line in node_file:
        nodes = line.split(" ")
        try:
            first_node = node_map[nodes[0]]
        except KeyError:
            print "Creating node id:{}, circle:{}, features: {}".format(nodes[0], circle_node_map[int(nodes[0])],
                                                                        feature_node_map[int(nodes[0])])

            first_node = Node("alter", id=nodes[0], circles=circle_node_map[int(nodes[0])],
                              features=feature_node_map[int(nodes[0])])
            node_map[nodes[0]] = first_node

        try:
            second_node = node_map[nodes[1]]
        except KeyError:
            print "Creating node id:{}, features:{}, circles: {}".format(nodes[1], circle_node_map[int(nodes[1])],
                                                                         feature_node_map[int(nodes[1])])
            second_node = Node("alter", id=nodes[1], circles=circle_node_map[int(nodes[1])],
                               features=feature_node_map[int(nodes[1])])
            node_map[nodes[1]] = second_node

        tx.create(first_node)
        tx.create(second_node)
        first_node_know_second_node = Relationship(first_node, "Knows", second_node)
        tx.create(first_node_know_second_node)
    tx.commit()


def build_feature_map():
    feature_file_name = open('0.featnames', 'r')
    features_map = {}
    for line in feature_file_name:
        features_data = line.split(" ")
        features_map[int(features_data[0])] = "{}__{} {}".format(features_data[1], features_data[2], features_data[3])
    return features_map


def assign_features_to_node():
    node_feature_file = open('0.feat', 'r')
    feature_node_map = defaultdict(list)
    feature_name_map = build_feature_map()
    for line in node_feature_file:
        feature_data = line.split(" ")
        count = 0
        for feature_bool in feature_data[1:]:
            if feature_bool == '1':
                feature_node_map[int(feature_data[0])].append(feature_name_map[count])
            count += 1

    return feature_node_map


def assign_features_to_node_ego():
    node_feature_file = open('0.egofeat', 'r')
    feature_node_map = defaultdict(list)
    feature_name_map = build_feature_map()
    for line in node_feature_file:
        feature_data = line.split(" ")
        count = 0
        for feature_bool in feature_data[1:]:
            if feature_bool == '1':
                feature_node_map[int(feature_data[0])].append(feature_name_map[count])
            count += 1

    return feature_node_map


def assign_circles():
    node_circle_file = open('0.circles', 'r')
    circle_node_map = defaultdict(list)
    for line in node_circle_file:
        circle_data = line.split('\t')
        circle_name = circle_data[0]
        for node_id in circle_data[1:]:
            circle_node_map[int(node_id)].append(circle_name)

    return circle_node_map


def node_selector(id):
    graph = Graph()
    selector = NodeSelector(graph)
    selected = selector.select("alter", id=id)
    return selected.first()
