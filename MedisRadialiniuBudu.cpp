#include <iostream>
#include <fstream>
#include <vector>
#include <string>
using namespace std;

void prufer_to_tree(const std::vector<int>& prufer_code, std::vector<std::pair<int, int>>& tree_edges) {
    int VerticalesNum = prufer_code.size() + 2;
    std::vector<int> vertices(VerticalesNum);
    for (int i = 0; i < VerticalesNum; ++i)
        vertices[i] = i + 1;

    std::vector<int> degree(VerticalesNum, 1);

    for (int v : prufer_code)
        degree[v - 1]++;

    for (int v : prufer_code) {
        int u = vertices.front();
        for (int vertex : vertices) {
            if (degree[vertex - 1] == 1) {
                u = vertex;
                break;
            }
        }
        tree_edges.emplace_back(u, v);
        degree[u - 1]--;
        degree[v - 1]--;
    }

    int u = vertices.front();
    int v = vertices.back();
    tree_edges.emplace_back(u, v);
}

void draw_radial_tree(const std::vector<int>& prufer_code) {
    std::vector<std::pair<int, int>> tree_edges;
    prufer_to_tree(prufer_code, tree_edges);

    std::ofstream dotFile("tree.dot");
    dotFile << "graph G {\n";
    for (auto edge : tree_edges)
        dotFile << "    " << edge.first << " -- " << edge.second << ";\n";
    dotFile << "    graph [layout=neato, mode=hier];\n";  // Specify layout as 'neato' and mode as 'hierarchical'
    dotFile << "}\n";
    dotFile.close();

    system("dot -Tpng tree.dot -o tree.png");

    std::cout << "Radial tree graph image generated: tree.png" << std::endl;
}

int main() {
    std::vector<int> prufer_code;
    std::string input;
    std::cout << "Enter Prufer code (comma separated): ";
    getline(std::cin, input);
    size_t pos = 0;
    while ((pos = input.find(',')) != std::string::npos) {
        prufer_code.push_back(stoi(input.substr(0, pos)));
        input.erase(0, pos + 1);
    }
    if (!input.empty())
        prufer_code.push_back(stoi(input));

    draw_radial_tree(prufer_code);

    return 0;
}
