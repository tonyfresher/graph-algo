class Graph:

    @classmethod
    def from_adjacency_matrix(self, matrix):
        graph = self()
        graph.topology = self._convert_adjacency_matrix_to_topology(matrix)

        return graph
    
    @staticmethod
    def _convert_adjacency_matrix_to_topology(matrix):
        node_count = len(matrix)
        topology = {n: [] for n in range(1, node_count + 1)}

        for v_from in range(node_count):
            for v_to in range(node_count):
                if matrix[v_from][v_to] == 1:
                    topology[v_from + 1].append(v_to + 1)

        return topology

    def find_connected_components(self):
        components = []
        nodes = {n for n in range(1, len(self.topology) + 1)}
        while nodes != set():
            c = self._dfs(self.topology, next(iter(nodes)))
            components.append(sorted(list(c)))
            nodes = nodes - c

        return sorted(components, key=lambda c: c[0])

    @staticmethod
    def _dfs(graph, start):
        visited, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend([item for item in graph[node] if item not in visited])
        return visited


def main(args=None):
    matrix = [
        [0, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ]

    graph = Graph.from_adjacency_matrix(matrix)
    components = graph.find_connected_components()

    print(components)

if __name__ == '__main__':
    main()
