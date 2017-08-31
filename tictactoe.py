
import ai_logic

class TicTacToe:
    def __init__(self):
        self.board = [['-','-','-'],
                      ['-','-','-'],
                      ['-','-','-']]


        # row : col : correct diagonal(s) to check 
        self.diags = {0 : {0: [self._check_ul], 1:[], 2: [self._check_ur]},
                      1 : {0: [], 1: [self._check_ul, self._check_ur], 2: []},
                      2 : {0: [self._check_ur], 1:[], 2: [self._check_ul]} }


        self.row = None
        self.col = None

        self.user = 'x'
        self.bot = 'o'

        self.ai_difficulty = 0

        self.turn = self.user
        
        self.game_over = False
        self.winner = "no one - tie game"

        self.count = 0 # each move increments
                       # in order to know if game board full


    def print_board(self):
        ''' Console game view '''
        for row in self.board:
            for col in row:
                print(col, end=' ')
            print()
        print("\n")
    

    def board_update(self):
        self.board[self.row][self.col] = self.turn

        self.count += 1


    def get_user_move(self):
        ''' Prompt the user to enter ROW then COLUMN of move '''

        # need to make sure move is VALID and not taken!!!

        print("Move must be separated by a space.")
        print("format : '[row] [col]' where 0,1,2 are only acceptable")
        move = input("Enter move:").split(' ')
        
        self.row = int(move[0])
        self.col = int(move[1])

        spot = self.board[self.row][self.col]

        if spot == self.user or spot == self.bot:
            return self.get_user_move()


    def switch_turns(self):
        ''' Switch between user and bot turns for making a move '''
        if self.turn == self.user:
            self.turn = self.bot
        else:
            self.turn = self.user



    def _check_row(self):
        ''' Assures all values in row are winning or not '''
        return self.board[self.row].count(self.turn) == 3
            
    def _check_col(self):
        ''' Assures all values in col are winning or not '''
        return self.turn == self.board[0][self.col] == self.board[1][self.col] == self.board[2][self.col]
    
    def _check_ul(self):
        ''' Assures all values in upper-left diagonal are winning or not '''
        return self.turn == self.board[0][0] == self.board[1][1] == self.board[2][2]
        
    def _check_ur(self):
        ''' Assures all values in upper-right diagonal are winning or not '''
        return self.turn == self.board[0][2] == self.board[1][1] == self.board[2][0]



    def determine_if_winner(self):
        ''' Use last row & col to determine 3 in a line '''

        # either do 2, 3, or 4 checks
        #
        # 1,1 move equates to 4 checks
        # corners equate to 3 checks
        # edges equate to 2 checks

        if self._check_row() or self._check_col():
            self.game_over = True
            self.winner = self.turn

        else:
            # check the dictionary on row, col values

            for func in self.diags[self.row][self.col]:
                if func():
                    self.game_over = True
                    self.winner = self.turn
        

    def do_ai_move(self):

        # self.ai_difficulty in range(4)
        # 
        # 0 -> random_ai
        # 1 -> easy_ai
        # 2 -> normal_ai
        # 3 -> difficult_ai
        
        self.row, self.col = ai_logic.determine(self.board, self.bot, self.user, self.ai_difficulty)
    

    def start(self):

        ai_difficulty = input("Choose AI Difficulty:\n0 for Random\n1 for Easy\n2 for Hard\n:").lstrip().strip()

        try:
            self.ai_difficulty = int(ai_difficulty)
            if self.ai_difficulty not in range(3):
                self.ai_difficulty = 1
        except:
            pass
            

        while self.count < 9 and not self.game_over:
            
            self.get_user_move()
            self.board_update()

            self.print_board()
            
            self.determine_if_winner()


            if self.game_over or self.count == 9:
                break
            self.switch_turns()



            self.do_ai_move()
            self.board_update()

            self.print_board()
            
            self.determine_if_winner()

            if self.game_over or self.count == 9:
                break
            self.switch_turns()


        print("Winner is "+self.winner+'!')

if __name__ == "__main__":
    TicTacToe().start()
        
