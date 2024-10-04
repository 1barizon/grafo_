#include <iostream>
#include "graph.h"


int main(){

    int nodes;

    std::cout << "Enter the number of nodes: ";
    std::cin >> nodes;
   
    graph g(nodes, 10);
    g.list_nodes();
    return 0;
}
