#ifndef GRAPH_H
#define GRAPH_H

#include <vector>
#include <map>
#include <string> 

struct Node {
    int value;
    std::vector<int> neighbors;
};


class graph {
    private:
        int nodes ;
        int edges_probability;
        std::vector<Node> node_list;

        
    public:
        graph(int nodes, int edges_probability);
        void list_nodes(); 
};

#endif // GRAPH_H
