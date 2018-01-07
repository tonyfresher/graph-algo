from collections import deque


class Labyrinth:

    @classmethod
    def from_matrix(self, matrix):
        labyrinth = self()
        labyrinth.topology = self._convert_matrix_to_topology(matrix)

        return labyrinth

    @staticmethod
    def _convert_matrix_to_topology(matrix):
        row_len, col_len = len(matrix), len(matrix[0])

        topology = {(i, j): set()
                    for i in range(1, row_len + 1)
                    for j in range(1, col_len + 1) 
                    if matrix[i - 1][j - 1] == 0}

        add_edge = lambda v1, v2: topology[v1].add(v2)

        for row, col in topology.keys():
            if row + 1 <= row_len and matrix[row][col - 1] == 0:
                add_edge((row, col), (row + 1, col))
            if col + 1 <= col_len and matrix[row - 1][col] == 0:
                add_edge((row, col), (row, col + 1))
            if row - 1 >= 1 and matrix[row - 2][col - 1] == 0:
                add_edge((row, col), (row - 1, col))
            if col - 1 >= 1 and matrix[row - 1][col - 2] == 0:
                add_edge((row, col), (row, col - 1))

        return topology

    def find_shortest_path(self, start, goal):
        try:
            return next(self._bfs_paths(self.topology, start, goal))
        except StopIteration:
            return None

    @staticmethod
    def _bfs_paths(graph, start, goal):
        queue = deque([(start, [start])])
        while queue:
            (vertex, path) = queue.popleft()
            for next in (graph[vertex] - set(path)):
                if next == goal:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))


def main(args=None):
    matrix = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]

    start, goal = (2, 2), (2, 4)

    labyrinth = Labyrinth.from_matrix(matrix)
    path = labyrinth.find_shortest_path(start, goal)

    print(path if path else 'There is no path between current start and goal')

if __name__ == '__main__':
    main()
