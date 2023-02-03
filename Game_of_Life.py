import matplotlib.pyplot as plt
import numpy as np

class GameOfLife:
    def __init__(self, size_of_board=100, board_start_mode=1, rules='', rle='', pattern_position=None):
        self.mode = {1: [0.5, 0.5], 2: [0.2, 0.8], 3: [0.8, 0.2], 4: (10, 10), 5: '24b1o11b1$22b1o1b1o11b1$12b2o6b2o12b2o1$11b1o3b1o4b2o12b2o1$2o8b1o5b1o3b2o14b1$2o8b1o3b1o1b2o4b1o1b1o11b1$10b1o5b1o7b1o11b1$11b1o3b1o20b1$12b2o22b1$!'}
        self.painting_rle = {'b': 0, 'o': 255}
        self.size = (size_of_board, size_of_board)
        self.pattern_position = pattern_position
        self.start_mode = board_start_mode
        self.rules = rules.split('/')                                        # separated rules
        self.born = set([int(k) for k in self.rules[0] if k.isdigit()])
        self.survive = set([int(r) for r in self.rules[1] if r.isdigit()])
        self.update_board = np.zeros(self.size).tolist()
        self.new_board = np.zeros(self.size).tolist()
        if len(rle) > 0:
            self.x, self.y = self.pattern_position
            self.transform_rle_to_matrix(rle)
        else:
            if board_start_mode not in {1, 2, 3, 4}:
                self.start_mode = 1
            self.START_MOD()

    def Check_Rules(self, row, col, neig, life_cell):                            # 'B32/S24'
        if life_cell and neig in self.survive:
            self.update_board[row][col] = 255
        if life_cell and neig not in self.survive:
            self.update_board[row][col] = 0
        elif (not life_cell) and neig in self.born:
            self.update_board[row][col] = 255

    def open_board(self):
        for w in range(0, self.size[0]):
            for t in range(0, self.size[0]):
                self.new_board[w][t] = self.update_board[w][t]
        return self.new_board

    def update(self):
        """This method updates board game by the rules of the game.
            Do single iteration.
            Input None.
            Output None."""
        new_b = self.open_board()
        for i in range(0, self.size[0]):
            for j in range(0, self.size[0]):
                neighbours = self.count_neighbours(i, j)
                life_cell = new_b[i][j] == 255
                self.Check_Rules(i, j, neighbours, life_cell)

    def count_neighbours(self, row, col):
        """this function return neighbours
           get : row (int),  col (int)"""
        dim = len(self.new_board)
        count = [self.new_board[(row - 1) % dim][col],
                 self.new_board[(row + 1) % dim][col],
                 self.new_board[row][(col - 1) % dim],
                 self.new_board[row][(col + 1) % dim],
                 self.new_board[(row - 1) % dim][(col + 1) % dim],
                 self.new_board[(row - 1) % dim][(col - 1) % dim],
                 self.new_board[(row + 1) % dim][(col + 1) % dim],
                 self.new_board[(row + 1) % dim][(col - 1) % dim]]
        return sum([1 for n in count if n == 255])

    def save_board_to_file(self, file_name):
        """ This method saves the current state of the game to a file. You should use Matplotlib for this.
        Input img_name donates the file name. Is a string, for example file_name = '1000.png'
        Output a file with the name that donates filename.
        """
        plt.imshow(self.update_board)                  # TODO: TO ADD bbox_inches='tight' ,and place i want to save the file
        plt.imsave(file_name, self.update_board)

    def START_MOD(self):
        if self.start_mode in (1, 2, 3):
            for row in range(self.size[0]):
                for col in range(self.size[0]):                   # it's change to life and depending on the mode stats
                    self.update_board[row][col] = np.random.choice([0, 255], p=self.mode[self.start_mode])

        else:                                                                             # start the game whit 10,10 position
            self.x, self.y = self.mode[4]                                                 # paint the Gosper Glider Gun
            self.transform_rle_to_matrix(self.mode[5])

    def return_board(self):
        return self.update_board

    def transform_rle_to_matrix(self, rle):
        """ This method transforms an rle coded pattern to a two dimensional list that holds the pattern,
            Dead will be donated with 0 while alive will be donated with 255.
            Input an rle coded string.
            Output a two dimensional list that holds a pattern with a size of the bounding box of the pattern."""
        index = 0
        y1 = self.y
        rle = "".join(rle.split('"'))
        while rle[index] != '!':
            if rle[index].isdigit():
                if rle[index + 1].isdigit() and self.painting_rle.get(rle[index + 2]) in (255, 0):
                    for k in range(int(rle[index] + rle[index + 1])):
                        self.update_board[self.x][y1 + k] = self.painting_rle.get(rle[index + 2])
                    y1 += int(rle[index] + rle[index + 1])
                    index += 2
                elif rle[index + 1].isdigit() and rle[index + 2] == '$':
                    self.x += int(rle[index] + rle[index + 1])
                    y1 = self.y
                    index += 2
                elif self.painting_rle.get(rle[index + 1]) in (255, 0):
                    for j in range(int(rle[index])):
                        self.update_board[self.x][y1 + j] = self.painting_rle.get(rle[index + 1])
                    y1 += int(rle[index])
                    index += 1
                elif rle[index + 1] == '$':
                    self.x += int(rle[index])
                    y1 = self.y
                    index += 1

            elif rle[index] in self.painting_rle.keys():
                self.update_board[self.x][y1] = self.painting_rle.get(rle[index])
                y1 += 1

            elif rle[index] == '$':
                self.x += 1
                y1 = self.y
            index += 1
        return self.update_board

    def display_board(self):
        """ This method displays the current state of the game to the screen. You can use Matplotlib for this.
        Input None.
        Output a figure should be opened and display the board.
        """
        plt.imshow(self.update_board)                                                          # just show the bord
        return plt.show()

if __name__ == "__main__":
    np.random.seed(seed=1)
    new = GameOfLife(size_of_board=50, rle='', pattern_position=0, board_start_mode=1, rules='B36/S23')
    # for i in range(100):
    new.update()
    new.display_board()
    # new.save_board_to_file("shahaf.png")
    # print(new.return_board)
