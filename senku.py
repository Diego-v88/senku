from typing import List
from simpleai.search import SearchProblem, astar
import timeit


def string_to_list(state_list: str) -> List:
    list_int: List = []
    for row in state_list.split(";"):
        list_int.append(list(map(int, row.split(","))))

    return list_int


def list_to_string(rows: List) -> str:
    list_str = ""
    for row in rows:
        row_str = str(row)
        list_str = list_str + ";" + row_str[1:len(row_str)-1]

    return list_str[1:]


class PuzzleSolver(SearchProblem):
    def __init__(self, european=False):
        self.x_board = 7
        self.y_board = 7
        self.empty_x, self.empty_y = 3, 3
        if european:
            self.no_board = [(0, 0), (0, 1), (1, 0), (5, 6), (6, 5), (6, 6),
                             (0, 5), (0, 6), (1, 6), (5, 0), (6, 0), (6, 1)]
        else:
            self.no_board = [(0, 0), (0, 1), (1, 0), (1, 1), (5, 5), (5, 6), (6, 5), (6, 6),
                             (0, 5), (0, 6), (1, 5), (1, 6), (5, 0), (5, 1), (6, 0), (6, 1)]

        initial = list_to_string(self.generate_board())
        super(PuzzleSolver, self).__init__(initial_state=initial)

    def generate_board(self):
        matrix = []
        for x in range(self.x_board):
            f = []
            for y in range(self.x_board):
                if (x, y) in self.no_board:
                    f.append(-2)
                else:
                    f.append(1)
            matrix.append(f)
        matrix[self.empty_x][self.empty_y] = 0
        return matrix

    def move_right(self, state_: List, x: int, y: int):
        state_copy = [n[:] for n in state_]
        if x < self.x_board - 2:
            if state_copy[x][y] == 1 and state_copy[x + 1][y] == 1 and state_copy[x + 2][y] == 0:
                state_copy[x][y] = 0
                state_copy[x + 1][y] = 0
                state_copy[x + 2][y] = 1
                return state_copy
        return -1

    @staticmethod
    def move_left(state_: List, x: int, y: int):
        state_copy = [n[:] for n in state_]
        if x > 1:
            if state_copy[x][y] == 1 and state_copy[x - 1][y] == 1 and state_copy[x - 2][y] == 0:
                state_copy[x][y] = 0
                state_copy[x - 1][y] = 0
                state_copy[x - 2][y] = 1
                return state_copy
        return -1

    def move_down(self, state_: List, x: int, y: int):
        state_copy = [n[:] for n in state_]
        if y < self.y_board - 2:
            if state_copy[x][y] == 1 and state_copy[x][y + 1] == 1 and state_copy[x][y + 2] == 0:
                state_copy[x][y] = 0
                state_copy[x][y + 1] = 0
                state_copy[x][y + 2] = 1
                return state_copy
        return -1

    @staticmethod
    def move_up(state_: List, x: int, y: int):
        state_copy = [n[:] for n in state_]
        if y > 1:
            if state_copy[x][y] == 1 and state_copy[x][y - 1] == 1 and state_copy[x][y - 2] == 0:
                state_copy[x][y] = 0
                state_copy[x][y - 1] = 0
                state_copy[x][y - 2] = 1
                return state_copy
        return -1

    def actions(self, cur_state):
        cur_state_int = string_to_list(cur_state)
        actions = []
        for x in range(self.x_board):
            for y in range(self.y_board):
                ri = self.move_right(cur_state_int.copy(), x, y)
                le = self.move_left(cur_state_int.copy(), x, y)
                do = self.move_down(cur_state_int.copy(), x, y)
                up = self.move_up(cur_state_int.copy(), x, y)
                if ri != -1:
                    actions.append({"state": ri, "x": x, "y": y, "move": "derecha"})
                if le != -1:
                    actions.append({"state": le, "x": x, "y": y, "move": "izquierda"})
                if do != -1:
                    actions.append({"state": do, "x": x, "y": y, "move": "abajo"})
                if up != -1:
                    actions.append({"state": up, "x": x, "y": y, "move": "arriba"})

        return actions

    def result(self, state: str, action: dict):
        return list_to_string(action.get("state"))

    def is_goal(self, state):
        count: int = state.count("1")
        if count.__eq__(1):
            return True
        else:
            return False

    def cost(self, state, action, state2):
        cost_1: int = state.count("1")
        cost_2: int = state2.count("1")
        if cost_1 > cost_2:
            return 1
        else:
            return 2

    def heuristic(self, state):
        distance: int = state.count("1")
        return distance


problem = PuzzleSolver(european=False)
start = timeit.default_timer()
result = astar(problem, graph_search=True)
end = timeit.default_timer()

if result is not None:
    for i, (action, state) in enumerate(result.path()):
        print()
        if action is None:
            print('Duración total: ', end - start)
        elif i == len(result.path()) - 1:
            print('Por ultimo, mover en x:', action.get("x"), ', en y: ', action.get("y"), ' con dirección: ', action.get("move"))
        else:
            print('Mover en x:', action.get("x"), ', en y: ', action.get("y"), ' con dirección: ', action.get("move"))
