from functools import reduce
from copy import deepcopy
from hopcroft_karp import BipartiteGraph
import math


class HungarianAlgorithm:

    @classmethod
    def assign(self, cost_matrix):
        # assume n is always less or equals m

        # - Step 0: pad to square matrix
        modified = self._pad_matrix(cost_matrix)

        result = None

        while not result:
            # - Step 1: reduce rows and columns
            modified = self._reduce_matrix_rows(modified)
            modified = self._reduce_matrix_columns(modified)

            # - Step 2: check for current matching
            matching = self._find_max_matching(modified)

            result = self._check_full_assignment(cost_matrix, matching)
            if result:
                return result

            # - Step 3: transform matrix
            modified = self._transform(modified, matching)

            matching = self._find_max_matching(modified)

            result = self._check_full_assignment(cost_matrix, matching)
            if result:
                return result
        

    @staticmethod
    def _reduce_matrix_rows(matrix):
        modified = deepcopy(matrix)

        m_len = len(matrix)

        for m in range(m_len):
            min_val = min(modified[m])
            modified[m] = list(map(lambda e: e - min_val, modified[m]))

        return modified

    @staticmethod
    def _reduce_matrix_columns(matrix):
        modified = deepcopy(matrix)

        m_len, n_len = len(matrix), len(matrix[0])

        for n in range(n_len):
            min_val = min([row[n] for row in modified])

            for m in range(m_len):
                modified[m][n] -= min_val

        return modified

    @classmethod
    def _find_max_matching(self, matrix):
        m_len, n_len = len(matrix), len(matrix[0])

        adjacency_matrix = self._fill_matrix(m_len, n_len)
        for m in range(m_len):
            for n in range(n_len):
                if matrix[m][n] == 0:
                    adjacency_matrix[m][n] = 1

        bigraph = BipartiteGraph.from_adjacency_matrix(adjacency_matrix)
        return bigraph.find_max_weight_matching()

    @classmethod
    def _transform(self, matrix, matching):
        modified = deepcopy(matrix)

        row_len, col_len = len(modified), len(modified[0])

        marked_rows, marked_columns = self._cover_zeros(modified)

        unmarked = []
        for m in range(row_len):
            for n in range(col_len):
                if m not in marked_rows and n not in marked_columns:
                    unmarked.append(modified[m][n])

        min_val = min(unmarked)

        for m in range(row_len):
            for n in range(col_len):
                if m in marked_rows and n in marked_columns:
                    modified[m][n] += min_val
                elif m not in marked_rows and n not in marked_columns:
                    modified[m][n] -= min_val

        return modified

    @classmethod
    def _check_full_assignment(self, matrix, matching):
        if len(matching) == len(matrix[0]):
            weight = reduce(lambda acc, key: acc + matrix[key][matching[key]],
                            matching,
                            0)
            return matching, weight

        return None

    @staticmethod
    def _cover_zeros(matrix):
        row_len, col_len = len(matrix), len(matrix[0])

        marked_rows, marked_columns = set(), set()

        for row in range(row_len):
            for col in range(col_len):
                if matrix[row][col] != 0:
                    continue

                zeros_in_row = reduce(lambda acc, weight: acc + 1 if weight == 0 else acc,
                                      matrix[row], 0)
                zeros_in_col = reduce(lambda acc, weight: acc + 1 if weight == 0 else acc,
                                      [matrix[row][col] for row in range(col_len)], 0)
                if zeros_in_col >= zeros_in_row:
                    marked_columns.add(col)
                else:
                    marked_rows.add(row)

        return marked_rows, marked_columns

    @staticmethod
    def _pad_matrix(matrix, pad_value=math.inf):
        max_len = max(len(matrix), len(matrix[0]))

        modified = deepcopy(matrix)

        for row in modified:
            if len(row) < max_len:
                row.extend([pad_value for _ in range(max_len - len(row))])
        
        if len(modified) < max_len:
            modified.extend([[pad_value for _ in range(max_len)] for _ in range(max_len - len(modified))])

        return modified

    @staticmethod
    def _fill_matrix(x_size, y_size, fill_value=0):
        return [[fill_value for _ in range(y_size)] for _ in range(x_size)]


if __name__ == '__main__':
    matrix = [
        [5, 6, 1, 5, 2, 7],
        [8, 9, 2, 4, 9, 8],
        [5, 6, 7, 6, 2, 9],
        [7, 2, 8, 1, 7, 8],
        [9, 3, 8, 9, 8, 9],
        [2, 5, 6, 5, 8, 3]
    ]

    matching, weight = HungarianAlgorithm.assign(matrix)
    
    print(matching)
    print(weight)
