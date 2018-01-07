from functools import reduce


class PointsSet:

    @classmethod
    def from_coordinates(self, coordinates):
        points = self()
        points.topology = self._convert_coordinates_to_topology(coordinates)

        return points

    @staticmethod
    def _convert_coordinates_to_topology(coordinates):
        metrics = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])

        edges = set()
        for i in range(len(coordinates)):
            for j in range(len(coordinates)):
                distance = metrics(coordinates[i], coordinates[j])
                if distance != 0:
                    edges.add((i, j, distance))

        topology = {
            'vertices': range(len(coordinates)),
            'edges': edges
        }

        return topology

    def find_minimum_spanning_tree(self):
        self._parent = {}
        self._rank = {}

        for vertice in self.topology['vertices']:
            self._parent[vertice] = vertice
            self._rank[vertice] = 0

        minimum_spanning_tree = set()

        edges = list(self.topology['edges'])
        edges.sort(key=lambda x: x[2])

        for edge in edges:
            v1, v2, weight = edge
            if self._find(v1) != self._find(v2):
                self._union(v1, v2)
                minimum_spanning_tree.add(edge)

        weight = reduce(lambda acc, x: acc + x[2], minimum_spanning_tree, 0)

        return minimum_spanning_tree, weight

    def _find_current_connected_component(self, vertice):
        if self._parent[vertice] != vertice:
            self._parent[vertice] = self._find(self._parent[vertice])
        return self._parent[vertice]

    def _trees_union(self, v1, v2):
        root1 = self._find(v1)
        root2 = self._find(v2)
        if root1 != root2:
            if self._rank[root1] > self._rank[root2]:
                self._parent[root2] = root1
            else:
                self._parent[root1] = root2
                if self._rank[root1] == self._rank[root2]: self._rank[root2] += 1


def main(args=None):
    coordinates = [
        [1, 6],
        [-1, 4],
        [3, 3],
        [6, 5],
        [4, 5],
        [5, 0]
    ]

    points = PointsSet.from_coordinates(coordinates)
    spanning_tree, weight = points.find_minimum_spanning_tree()

    print([edge[:2] for edge in spanning_tree])
    print(weight)

    result = []

if __name__ == '__main__':
    main()
