import networkx as nx


class BipartiteGraph:

    @classmethod
    def from_adjacency_matrix(self, matrix):
        bigraph = self()
        bigraph.topology = self._convert_adjacency_matrix_to_topology(matrix)

        return bigraph

    @staticmethod
    def _convert_adjacency_matrix_to_topology(matrix):
        topology = nx.DiGraph()

        x_len, y_len = len(matrix), len(matrix[0])

        topology.add_nodes_from([f'X{x}' for x in range(x_len)])
        topology.add_nodes_from([f'Y{y}' for y in range(y_len)])
        
        for x in range(x_len):
            for y in range(y_len):
                if matrix[x][y] == 1:
                    topology.add_edge(f'X{x}', f'Y{y}', capacity=1, flow=0)

        for x in range(x_len):
            topology.add_edge('S', f'X{x}', capacity=1, flow=0)

        for y in range(y_len):
            topology.add_edge(f'Y{y}', 'T', capacity=1, flow=0)

        return topology

    def find_max_weight_matching(self):
        matching =  {}
        flow, path = 0, True

        while path:
            path, reserve = self._depth_first_search(self.topology, 'S', 'T')

            if path == []:
                return {int(key[1:]): int(matching[key][1:]) for key in matching}

            matching[path[1]] = path[2]

            flow += reserve

            for v, u in zip(path, path[1:]):
                if v.startswith('X') and u.startswith('Y'):
                    matching[v] = u

                if self.topology.has_edge(v, u):
                    self.topology[v][u]['flow'] += reserve
                else:
                    self.topology[u][v]['flow'] -= reserve

    @staticmethod
    def _depth_first_search(topology, source, sink):
        undirected = topology.to_undirected()
        explored = {source}
        stack = [(source, 0, dict(undirected[source]))]

        while stack:
            v, _, neighbours = stack[-1]
            if v == sink:
                break

            while neighbours:
                u, e = neighbours.popitem()
                if u not in explored:
                    break
            else:
                stack.pop()
                continue

            in_direction = topology.has_edge(v, u)
            capacity, flow = e['capacity'], e['flow']

            if in_direction and flow < capacity:
                stack.append((u, capacity - flow, dict(undirected[u])))
                explored.add(u)
            elif not in_direction and flow:
                stack.append((u, flow, dict(undirected[u])))
                explored.add(u)

        reserve = min((f for _, f, _ in stack[1:]), default=0)
        path = [v for v, _, _ in stack]

        return path, reserve

def main(args=None):
    matrix = [
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ]

    bigraph = BipartiteGraph.from_adjacency_matrix(matrix)
    matching = bigraph.find_max_weight_matching()

    print(matching)

if __name__ == '__main__':
    main()
