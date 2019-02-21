import math
class Fifteen:
    def __init__(self, fifteen_string):

        self.initial_string = fifteen_string
        self.actual_string = fifteen_string
        self.fifteen_string = list(fifteen_string)
        self.change = True
        self.solvable = True
        self.finish = False
        self.inversiones = 0
        self.row_number = 0
        self.sectors = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'A': 10,
            'B': 11,
            'C': 12,
            'D': 13,
            'E': 14,
            'F': 15,
            '.': 16
        }
        self.record = []
        self.backtrack = {
            self.initial_string: 'END'
        }
        self.state_cost = []
        self.explored = []
        self.frontiers = []

    def solvable_puzzle(self):
        inversions = 0
        index_space = self.fifteen_string.index('.')
        self.fifteen_string.remove('.')

        for i in range(14):
            x = self.sectors[self.fifteen_string[i]]
            for j in range(1, 15):
                y = self.sectors[self.fifteen_string[j]]
                if x > y and i < j:
                    inversions = inversions + 1
        self.inversiones = inversions
        self.fifteen_string.insert(index_space, '.')

        self.row_number = 4 - math.floor(index_space / 4)
        result1 = 'ODD'
        result2 = 'ODD'

        if inversions % 2 == 0:
            result1 = 'EVEN'

        if self.row_number % 2 == 0:
            result2 = 'EVEN'

        if result1 != result2:
            return True
        else:
            return False

    def goal_test(self):
        if self.fifteen_string == ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', '.']:
            self.finish = True
            return True
        else:
            return False

    def actions(self, state):
        action_list = []
        index = self.fifteen_string.index('.')
        if index > 3:
            action_list.append('U')
        if index < 12:
            action_list.append('D')
        if index % 4 > 0:
            action_list.append('L')
        if index % 4 < 3:
            action_list.append('R')
        return action_list

    def result(self, state, action):
        if action == 'U':
            return self.move_up(state)
        elif action == 'D':
            return self.move_down(state)
        elif action == 'L':
            return self.move_left(state)
        elif action == 'R':
            return self.move_right(state)
        else:
            print("Something went terrible wrong with: result(self, state, action)")
        return

    def move_up(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index - 4]
        base[index - 4] = '.'

        string_result = ''.join(base)
        self.backtrack[string_result] = state
        return string_result

    def move_down(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index + 4]
        base[index + 4] = '.'

        string_result = ''.join(base)
        self.backtrack[string_result] = state
        return string_result

    def move_left(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index - 1]
        base[index - 1] = '.'

        string_result = ''.join(base)
        self.backtrack[string_result] = state
        return string_result

    def move_right(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index + 1]
        base[index + 1] = '.'

        string_result = ''.join(base)
        self.backtrack[string_result] = state
        return string_result

    def main(self):
        if not self.solvable_puzzle():
            print("El puzzle no posee solucion. \nNúmero de inversiones: "
                  + str(self.inversiones) + "\nPosicion de X desde el fondo: " + str(self.row_number)  +
                  "\nVease: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/ para una explicación"
                  "mas completa")
            return

        self.frontiers.append(''.join(self.fifteen_string))
        self.state_cost.append(1000000000000000)
        while not self.finish and self.change:
            self.actual_string = self.frontiers[0]
            if self.goal_test(self.actual_string):
                #Funcion de backtrack con self.actual_string
                break
            else:
                self.frontiers.remove(0)
                self.state_cost.remove(0)
                self.explored.append(self.actual_string)
                action_list = self.actions(self.actual_string)
                for i in action_list:
                    next_state = self.result(self.actual_string, i)
                    self.frontiers.append(next_state)
                    #funcion de heuristica para saber cuanto pesa el next_state
                    #Funcion para posicionar un next_state basado en su peso de heuristica

fifteen = Fifteen('D2A31C845.96FEB7')
print(fifteen.solvable_puzzle())
