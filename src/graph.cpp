#include <iostream>
#include "graph.h"
#include <random>
#include <unordered_set>

graph::graph(int nodes, int edges_probability) : nodes(nodes), edges_probability(edges_probability) {

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, nodes-1);
    node_list.resize(nodes);

    for (int i = 0; i < nodes; i++) {
        int n_neighbors = dis(gen);
        std::unordered_set<int> neighbor_set;

        std::uniform_int_distribution<> dis_values(1, n_neighbors);
        int value = dis_values(gen);
        node_list[i].value = value;

        for (int j = 0; j < n_neighbors; j++) {
            int neighbor = dis(gen);
            while (neighbor == i) {
                neighbor = dis(gen);
            }
            neighbor_set.insert(neighbor);
        }
        node_list[i].neighbors = std::vector<int>(neighbor_set.begin(), neighbor_set.end());
    }
}

void graph::list_nodes() {
     for (int i = 0; i < nodes; i++) {
        std::cout << "Node " << i << " has value " << node_list[i].value << " and neighbors: ";
        for (int neighbor : node_list[i].neighbors) {
            std::cout << neighbor << " ";
        }
        std::cout << std::endl;
    }
}
