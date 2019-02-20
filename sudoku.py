from copy import copy
from copy import deepcopy

class Sudoku:
    def __init__(self, sudoku_string):
        """ Where
            initial_string: the one to compare at the end. You'll understand later. 
            actual_string: String being compared and analyzed
            sudoku_string: Is the parameter initializer of the 4x4 sudoku
            change: a boolean that will determine if, after an iteration, the sudoku changed
            solvable: a boolean that will determine if the sudoku is solvable
            finish: will determine that we have found a solution for the sudoku
            probability: dictionary which will hold the probable numbers of 2 or more squares 
                in the case that there is not only one solution to the problem
            record: list of  steps that the sudoku took to be solved. 
            columns: list that holds the 4 columns with their actual values
            rows: list that holds the 4 rows with their actual values
            squares: list that holds the 4 squares with their actual values
            queue_list: list that holds the queue of the states reading right now
            state_cost: list that holds the cost of every step mentioned on queue_list to organize them
            frontiers: list that hold the string already read
        """""
        self.initial_string = sudoku_string
        self.actual_string = sudoku_string
        self.sudoku_string = list(sudoku_string)
        self.change = True
        self.solvable = True
        self.finish = False
        self.probability = {}
        self.sectors = {
            0: 0,
            1: 0,
            2: 1,
            3: 1,
            4: 0,
            5: 0,
            6: 1,
            7: 1,
            8: 2,
            9: 2,
            10: 3,
            11: 3,
            12: 2,
            13: 2,
            14: 3,
            15: 3
        }
        self.record = []
        self.columns = []
        self.rows = []
        self.squares = []
        self.queue_list = []
        self.state_cost = []
        self.backtrack = {
            self.initial_string: 'END'
        }
        self.frontiers = []

        for i in range(16):
            self.probability[i] = [1, 2, 3, 4]

    def actions(self):
        print(self.sudoku_string.count('.'))
        if self.sudoku_string.count('.') > 12:
            print("Not solvable sudoku. There are less than 4 clues in a 4 x 4 sudoku. \n")
            print("Check: http://pi.math.cornell.edu/~mec/Summer2009/Mahmood/More.html for explanation")
            return

        if self.contradiction():
            print("Not solvable sudoku. There is a contradiction on the sudoku itself.")
            return

        while not self.finish and self.change:

            compare1 = deepcopy(self.queue_list)
            self.iterate_reaction()
            if compare1 == self.queue_list:
                self.change == False
                self.solvable = False
        print("--------------------------------------------------------------------")
        if not self.solvable:
            print("Not solvable sudoku. There are more than one answer to it \n")
            print(self.sudoku_string)
            print(self.probability)
            print("--------------------------------------------------------------------")
            return
        print("Fastest stepts to solution: \n")
        print(self.record)
        print("--------------------------------------------------------------------")

    def contradiction(self):
        resolve = False

        self.update_data(self.sudoku_string)

        for row in self.rows:
            for x in row:
                if row.count(x) > 1 and x != '.':
                    resolve = True
                    break

        if not resolve:
            for column in self.columns:
                for x in column:
                    if column.count(x) > 1 and x != '.':
                        resolve = True
                        break

        if not resolve:
            for square in self.squares:
                for x in square:
                    if square.count(x) > 1 and x != '.':
                        resolve = True
                        break

        return resolve

    def iterate_reaction(self):
        # meter el primer strign en donde estara la lista de records
        if len(self.queue_list) < 1:
            self.frontiers.append(self.actual_string)
            self.update_data(self.actual_string)

            for i in range(16):
                self.solve(i)

            number = self.count_prob100()
            for x in self.probability:
                if len(self.probability[x]) < 1:
                    print("Something went terrible wrong with iterate_reaction: Size of the probability array is 0")

                elif len(self.probability[x]) == 1:
                    state_worth = number - 1

                    twin = copy(self.sudoku_string)
                    twin[x] = str(self.probability[x][0])

                    string_result = ''.join(twin)
                    state_worth = state_worth +  16 - twin.count('.') + self.expert_solve(string_result) - (number - 1)

                    self.backtrack[string_result] = self.actual_string
                    self.append_queuer(string_result, state_worth)


        else:
            for x in self.queue_list:
                if list(x).count('.') == 0:
                    self.finish = True
                    self.backtrack_record(x)


                self.actual_string = x
                self.queue_list.remove(x)
                self.frontiers.append(self.actual_string)
                self.update_data(self.actual_string)

                for i in range(16):
                    self.solve(i)

                number = self.count_prob100() - 1
                for x in self.probability:
                    if len(self.probability[x]) < 1:
                        print("Something went terrible wrong with iterate_reaction: Size of the probability array is 0")

                    elif len(self.probability[x]) == 1:
                        state_worth = number - 1

                        twin = copy(self.sudoku_string)
                        twin[x] = str(self.probability[x][0])

                        string_result = ''.join(twin)
                        state_worth = state_worth + 16 - twin.count('.') + self.expert_solve(string_result) - (
                                    number - 1)


                        #Simplemente revisar si existe una manera mas rapida de llegar al string creado ahorita, en dado
                        #caso existiera en queue_list

                        if string_result in self.queue_list:
                            index_queue = self.queue_list.index(string_result)
                            if state_worth < self.state_cost[index_queue]:
                                self.backtrack[string_result] = self.actual_string
                                self.append_queuer(string_result, state_worth)
                        else:
                            self.backtrack[string_result] = self.actual_string
                            self.append_queuer(string_result, state_worth)
                        return
                # solver para cada uno y que se coloquen los nuevos strings en el backtrack

            # Ademas debes de meter en las fronteras cada vez que se itera.
        return

    def solve(self, index):
        data = self.sudoku_string[index]

        if data != '.':
            return False

        content = self.probability[index]
        square = self.which_square(index)
        row = self.which_row(index)
        col = self.which_col(index)

        for i in range(4):
            n1 = square[i]
            if n1 != '.':
                if int(n1) in content:
                    content.remove(int(n1))
            n2 = row[i]
            if n2 != '.':
                if int(n2) in content:
                    content.remove(int(n2))
            n3 = col[i]
            if n3 != '.':
                if int(n3) in content:
                    content.remove(int(n3))
        self.probability[index] = content
        return

    def expert_solve(self, data):
        dato = list(data)
        prob = copy(self.probability)

        number = 0
        for x in dato:
            if x == '.':
                content = prob[number]
                square = self.which_square(number)
                row = self.which_row(number)
                col = self.which_col(number)

                for i in range(4):
                    n1 = square[i]
                    if n1 in content:
                        content.remove(n1)
                    n2 = row[i]
                    if n2 in content:
                        content.remove(n2)
                    n3 = col[i]
                    if n3 in content:
                        content.remove(n3)
                prob[number] = content
            number = number + 1

        number = 0
        for x in prob:
            if len(prob[x]) == 1:
                number = number + 1
        return number

    def update_data(self, string_state):
        self.sudoku_string = list(string_state)
        # Columns & Rows
        for i in range(4):
            row = [string_state[4 * i + 0], string_state[4 * i + 1], string_state[4 * i + 2],
                   string_state[4 * i + 3]]
            column = [string_state[i], string_state[i + 4], string_state[i + 8],
                      string_state[i + 12]]

            self.rows.append(row)
            self.columns.append(column)

        # Squares
        sector1 = []
        sector2 = []
        sector3 = []
        sector4 = []
        for i in range(16):
            sector = self.sectors[i]
            if sector == 0:
                sector1.append(string_state[i])
            elif sector == 1:
                sector2.append(string_state[i])
            elif sector == 2:
                sector3.append(string_state[i])
            elif sector == 3:
                sector4.append(string_state[i])
            else:
                print("Something went wrong: Not identifying secotr correctly")
        self.squares.append(sector1)
        self.squares.append(sector2)
        self.squares.append(sector3)
        self.squares.append(sector4)

        for i in range(16):
            self.probability[i] = [1, 2, 3, 4]


    '''''Returns in which square form self.square[] should you look for the numbers'''
    def which_square(self, index):
        number = self.sectors[index]
        sector1 = [self.sudoku_string[0], self.sudoku_string[1], self.sudoku_string[4], self.sudoku_string[5]]
        sector2 = [self.sudoku_string[2], self.sudoku_string[3], self.sudoku_string[6], self.sudoku_string[7]]
        sector3 = [self.sudoku_string[8], self.sudoku_string[9], self.sudoku_string[12], self.sudoku_string[13]]
        sector4 = [self.sudoku_string[10], self.sudoku_string[11], self.sudoku_string[14], self.sudoku_string[15]]

        if number == 0:
            return sector1
        elif number == 1:
            return sector2
        elif number == 2:
            return sector3
        elif number == 3:
            return sector4
        else:
            print("Something went terrible with which_square")
        return

    '''''Returns in which row form self.square[] should you look for the numbers'''
    def which_row(self, index):
        if index < 4:
            return [self.sudoku_string[0], self.sudoku_string[1], self.sudoku_string[2], self.sudoku_string[3]]
        elif 4 <= index < 8:
            return [self.sudoku_string[4], self.sudoku_string[5], self.sudoku_string[6], self.sudoku_string[7]]
        elif 8 <= index < 12:
            return [self.sudoku_string[8], self.sudoku_string[9], self.sudoku_string[10], self.sudoku_string[11]]
        elif 12 <= index < 16:
            return [self.sudoku_string[12], self.sudoku_string[13], self.sudoku_string[14], self.sudoku_string[15]]
        else:
            print("Something went wrong in which_row()")
        return

    '''''Returns in which column form self.square[] should you look for the numbers'''
    def which_col(self, index):
        module = index % 4
        if module == 0:
            return [self.sudoku_string[0], self.sudoku_string[4], self.sudoku_string[8], self.sudoku_string[12]]
        elif module == 1:
            return [self.sudoku_string[1], self.sudoku_string[5], self.sudoku_string[9], self.sudoku_string[13]]
        elif module == 2:
            return [self.sudoku_string[2], self.sudoku_string[6], self.sudoku_string[10], self.sudoku_string[14]]
        elif module == 3:
            return [self.sudoku_string[3], self.sudoku_string[7], self.sudoku_string[11], self.sudoku_string[15]]
        else:
            print("Something went wrong in which_row()")
        return

    def count_prob100(self):
        number = 0
        for x in self.probability:
            if len(self.probability[x]) == 1:
                number = number + 1

        return number

    def append_queuer(self, string_queuer, state_worth):
        if len(self.queue_list) < 1 and len(self.state_cost) < 1 :
            self.queue_list.append(string_queuer)
            self.state_cost.append(state_worth)

        else:
            if self.frontier_bool(string_queuer, state_worth):
                if string_queuer in self.frontiers:
                    index = self.frontiers.index(string_queuer)
                    self.state_cost[index] = state_worth
                    self.backtrack[string_queuer] = self.actual_string
                else:
                    length = len(self.state_cost)
                    index = 0
                    for x in self.state_cost:
                        if state_worth > x:
                            self.state_cost.insert(index, state_worth)
                            self.queue_list.insert(index, string_queuer)
                            break

                        index = index + 1

                    if length == len(self.state_cost):
                        self.state_cost.append(state_worth)
                        self.queue_list.append(string_queuer)

    '''''Return true if either, the string is not on frontiers, so it has not been analyzed or
    The state worth of the string_queuer is higher than the one listed on frontiers, which makes a better result'''
    def frontier_bool(self, string_queuer, state_worth):
        if string_queuer not in self.frontiers:
            return True
        else:
            index = self.frontiers.index(string_queuer)
            weight = self.state_cost[index]

            if weight < state_worth:
                return True
            else:
                return False

    def backtrack_record(self, start):
        end = False
        value = start
        while not end:
            self.record.insert(0, value)
            value = self.backtrack[value]

            if value == 'END':
                end = True


sudoku = Sudoku(".1..2..1...3..4.")
sudoku.actions()