from collections import deque


class Net:

    @classmethod
    def from_lists(self, lists):
        net = self()
        net.topology, net.weights = self._convert_lists_to_topology(lists)

        return net

    @staticmethod
    def _convert_lists_to_topology(lists):
        vertex_count = len(lists)
        topology = {n: [] for n in range(1, vertex_count + 1)}
        weights = {}

        for v_from in range(vertex_count):
            for i in range(0, len(lists[v_from]), 2):
                v_to = lists[v_from][i]
                topology[v_from + 1].append(v_to)
                weights[(v_from + 1, v_to)] = int(lists[v_from][i + 1])

        return topology, weights

    def find_shortest_path(self, old_start, old_goal):
        vertex_count = len(self.topology)

        self.topology, self.weights, index = self._topsort(self.topology, self.weights)
        reversed_index = {index[i]: i for i in index}
        start, goal = index[old_start], index[old_goal]
        distance, previous = {}, {}

        distance[start] = 0
        previous[start] = 0

        for k in range(start + 1, vertex_count + 1):
            distance[k] = float('inf')
            previous[k] = start

        for k in range(start, vertex_count + 1):
            for v in self.topology[k]:
                if distance[k] + self.weights[(k, v)] < distance[v]:
                    distance[v] = distance[k] + self.weights[(k, v)]
                    previous[v] = k

        path = [goal]
        node = goal
        while (node != start):
            node = previous[node]
            path.append(node)

        return [reversed_index[i] for i in path[::-1]], distance[goal]

    @staticmethod
    def _topsort(topology, weights):
        stack = deque()
        deg_in = {v: 0 for v in topology}
        index = {}

        for v in topology:
            for w in topology[v]:
                deg_in[w] += 1
                
        for v in topology:
            if deg_in[v] == 0:
                    stack.append(v)

        number = 1

        while stack:
            node = stack.popleft()
            index[node] = number
            number += 1
            for w in topology[node]:
                deg_in[w] -= 1
                if deg_in[w] == 0:
                    stack.append(w)

        sorted_topology = {}
        for v in topology:
            sorted_topology[index[v]] = {index[w] for w in topology[v]}

        topology = sorted_topology
        weights = {(index[v], index[w]): weights[v, w] for v, w in weights}

        return topology, weights, index


def main(args=None):
    lists = [
        [2,  1,  3,  5,  4,  3],
        [3,  2,  5,  2,  6, 10],
        [4, 10,  6, 10],
        [6,  1,  7,  2],
        [6, 15,  8, 12],
        [7, 10,  8,  2],
        [8, 15],
        [],
        []
    ]

    start, goal = 1, 8

    net = Net.from_lists(lists)

    path, weight = net.find_shortest_path(start, goal)

    if weight != float('inf'):
        print(path)
        print(weight)
    else:
        print('There is no path between current start and goal')

if __name__ == '__main__':
    main()
