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
            0: hex(0),
            1: hex(1),
            2: hex(2),
            3: hex(3),
            4: hex(4),
            5: hex(5),
            6: hex(6),
            7: hex(7),
            8: hex(8),
            9: hex(9),
            10: hex(10),
            11: hex(11),
            12: hex(12),
            13: hex(13),
            14: hex(14),
            15: hex(15)
        }
        self.record = []
        self.queue_list = []
        self.state_cost = []
        self.backtrack = {
            self.initial_string: 'END'
        }
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
        self.organize_hex_list()
        index_space = self.fifteen_string.index(16)
        self.fifteen_string.remove(16)

        for i in range(14):
            x = self.fifteen_string[i]
            for j in range(1, 15):
                y = self.fifteen_string[j]
                if x > y and i < j:
                    inversions = inversions + 1
        self.inversiones = inversions
        self.fifteen_string.insert(index_space, 16)

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
        if self.fifteen_string == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
            return True
        else:
            return False

    def actions(self):
        return

    def result(self, state, action):
        return

    def move_up(self, state):
        return

    def move_down(self, state):
        return

    def move_left(self, state):
        return

    def move_right(self, state):
        return

    def main(self):
        if not self.solvable_puzzle():
            print("El puzzle no posee solucion. \nNúmero de inversiones: "
                  + str(self.inversiones) + "\nPosicion de X desde el fondo: " + str(self.row_number)  +
                  "\nVease: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/ para una explicación"
                  "mas completa")
            return


fifteen = Fifteen('D2A31C845.96FEB7')

