
class sudoku:
    def __init__(self, sudoku_string):
        """ Where
            sudoku_string: Is the parameter initializer of the 4x4 sudoku
            change: a boolean that will determine if, after an iteration, the sudoku changed
            solvable: a boolean that will determine if the sudoku is solvable
            probability: dictionary which will hold the probable numbers of 2 or more squares 
                in the case that there is not only one solution to the problem
            record: list of  steps that the sudoku took to be solved. 
            columns: list that holds the 4 columns with their actual values
            rows: list that holds the 4 rows with their actual values
            squares: list that holds the 4 squares with their actual values
        """""
        self.sudoku_string = list(sudoku_string)
        self.change = False
        self.solvable = True
        self.probability = {}
        self.sectors = {
            "0": 0,
            "1": 0,
            "2": 1,
            "3": 1,
            "4": 0,
            "5": 0,
            "6": 1,
            "7": 1,
            "8": 2,
            "9": 2,
            "10": 3,
            "11": 3,
            "12": 2,
            "13": 2,
            "14": 3,
            "15": 3
        }
        self.record = []
        self.columns = []
        self.rows = []
        self.squares = []

    def actions(self):
        self.record.append(self.sudoku_string)

        if self.record.count('.') > 12:
            print("Not solvable sudoku. There are less than 4 clues in a 4 x 4 sudoku. \n")
            print("Check: http://pi.math.cornell.edu/~mec/Summer2009/Mahmood/More.html for explanation")
            return

        if self.contradiction():
            print("Not solvable sudoku. There is a contradiction on the sudoku itself.")
            return

        #aqui tiene que ir la calculada del rompecabezas, antes de ver si es solvable o no

        if not self.solvable:
            print("Not solvable sudoku. There are more than one answer to it \n")
            print(self.sudoku_string)
            print(self.probability)
            return

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


    def update_data(self, string_state):
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
            if sector == 1:
                sector1.append(string_state[i])
            elif sector == 2:
                sector2.append(string_state[i])
            elif sector == 3:
                sector3.append(string_state[i])
            elif sector == 4:
                sector4.append(string_state[i])
            else:
                print("Something went wrong: Not identifying secotr correctly")
        self.squares.append(sector1, sector2, sector3, sector4)


    def result(self):
        return

