import math
import copy
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
        keys = self.backtrack.keys()
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index - 4]
        base[index - 4] = '.'

        string_result = ''.join(base)
        if string_result not in keys:
            self.backtrack[string_result] = state
        return string_result

    def move_down(self, state):
        keys = self.backtrack.keys()
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index + 4]
        base[index + 4] = '.'

        string_result = ''.join(base)
        if string_result not in keys:
            self.backtrack[string_result] = state
        return string_result

    def move_left(self, state):
        keys = self.backtrack.keys()
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index - 1]
        base[index - 1] = '.'

        string_result = ''.join(base)
        if string_result not in keys:
            self.backtrack[string_result] = state
        return string_result

    def move_right(self, state):
        keys = self.backtrack.keys()
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index + 1]
        base[index + 1] = '.'

        string_result = ''.join(base)
        if string_result not in keys:
            self.backtrack[string_result] = state
        return string_result

    def distance(self, index_a, index_b):
        # Section A
        floor_a = math.floor(index_a / 4)
        module_a = index_a % 4

        #Section B
        floor_b = math.floor(index_b / 4)
        module_b = index_b % 4
        return abs(floor_a - floor_b) + abs(module_a - module_b)

    def weight(self, state):
        """"Where
        out_a_place: gets +1 whenever a square its out of its place
        reach: gets +x where x is the distance of a square to its rightfull place"""
        out_a_place = 0
        reach = 0
        string_array = list(state)
        for i in string_array:
            value = self.sectors[i]
            index = string_array.index(i)

            if (value -1) != index:
                out_a_place = out_a_place + 1
                reach = reach + self.distance(value - 1, index)
        return out_a_place + reach

    def queue_positioner(self, next_state, state_price):
        if len(self.state_cost) < 1 and len(self.frontiers) < 1:
            self.frontiers.append(next_state)
            self.state_cost.append(state_price)

        else:
            length = len(self.state_cost)
            index = 0
            for x in self.state_cost:
                if state_price < x:
                    self.state_cost.insert(index, state_price)
                    self.frontiers.insert(index, next_state)
                    break

                index = index + 1

            if length == len(self.state_cost):
                self.state_cost.append(state_price)
                self.frontiers.append(next_state)

    def backtrack_record(self, start):
        end = False
        value = start
        while not end:
            self.record.insert(0, value)
            value = self.backtrack[value]

            if value == 'END':
                end = True

    def print_nicely(self, string):
        elements = list(string)
        print("+---+---+---+---+")
        print("| " + elements[0] + " | " + elements[1] + " | " + elements[2] + " | " + elements[3] + " |")
        print("+---+---+---+---+")
        print("| " + elements[4] + " | " + elements[5] + " | " + elements[6] + " | " + elements[7] + " |")
        print("+---+---+---+---+")
        print("| " + elements[8] + " | " + elements[9] + " | " + elements[10] + " | " + elements[11] + " |")
        print("+---+---+---+---+")
        print("| " + elements[12] + " | " + elements[13] + " | " + elements[14] + " | " + elements[15] + " |")
        print("+---+---+---+---+")


    def solve_puzzle(self):
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
            self.fifteen_string = list(self.actual_string)
            if self.goal_test():
                self.backtrack_record(self.actual_string)
                break
            else:
                del self.frontiers[0]
                del self.state_cost[0]
                self.explored.append(self.actual_string)
                action_list = self.actions(self.actual_string)
                for i in action_list:
                    copy_string = self.actual_string[:]
                    next_state = self.result(copy_string, i)
                    if next_state not in self.explored:
                        state_price = self.weight(next_state)
                        self.queue_positioner(next_state, state_price)

        print("--------------------------------------------------------------------")
        print("Fastest Steps to solution: \n")
        number = 1
        for i in self.record:
            print("Step: " + str(number))
            self.print_nicely(i)
            print("")
            number = number + 1
        print("--------------------------------------------------------------------")


fifteen = Fifteen('6D7A89B.F2C5E314')
fifteen.solve_puzzle()
