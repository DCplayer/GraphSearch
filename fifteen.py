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
        self.queue_list = []
        self.state_cost = []
        self.backtrack = {
            self.initial_string: 'END'
        }
        self.explored = []
        self.frontiers = []

    def organize_hex_list(self):
        for i in range(16):
            if self.fifteen_string[i] == '.':
                self.fifteen_string[i] = 16
            else:
                self.fifteen_string[i] = int(self.fifteen_string[i], 16)
        print(self.fifteen_string)

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
        return

    def result(self, state, action):
        if action == 'UP':
            return self.move_up()
        return

    def move_up(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index - 4]
        base[index - 4] = '.'
        return ''.join(base)

    def move_down(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index + 4]
        base[index + 4] = '.'
        return ''.join(base)

    def move_left(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index - 1]
        base[index - 1] = '.'
        return ''.join(base)

    def move_right(self, state):
        index = self.fifteen_string.index('.')
        base = list(state)
        base[index] = base[index + 1]
        base[index + 1] = '.'
        return ''.join(base)

    def main(self):
        if not self.solvable_puzzle():
            print("El puzzle no posee solucion. \nNúmero de inversiones: "
                  + str(self.inversiones) + "\nPosicion de X desde el fondo: " + str(self.row_number)  +
                  "\nVease: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/ para una explicación"
                  "mas completa")
            return


fifteen = Fifteen('D2A31C845.96FEB7')
print(fifteen.solvable_puzzle())
