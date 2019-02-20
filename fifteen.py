
class Fifteen:
    def __init__(self, fifteen_string):

        self.initial_string = fifteen_string
        self.actual_string = fifteen_string
        self.fifteen_string = list(fifteen_string)
        self.change = True
        self.solvable = True
        self.finish = False
        self.sectors = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
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
