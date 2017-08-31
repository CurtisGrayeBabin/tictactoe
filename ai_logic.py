# Curtis Babin
# curtsocal [at] gmail [dot] com

# AI module containing the logic for:
# 1. Random AI
# 2. Easy AI
# 3. Normal AI
# 4. Difficult AI


import random, collections


def random_logic(potential_moves):
    ''' AI that chooses one random open spot '''
    
    random.shuffle(potential_moves)
    return potential_moves[0][0], potential_moves[0][1]


def _is_corner(move):
    ''' Returns if move location is corner in the board '''
    row = move[0]
    col = move[1]

    return ((row == 0 or row == 2) and (col == 0 or col == 2))


def get_diag(row, col, board, checks):
    ''' Returns either the upper-left diag, upper-right diag, or both diagonals'''

    if not _is_corner( (row,col) ): # move location is NOT a corner
        
        if 1 == row == col: # center location of board includes both diagonals
            checks.append([ board[0][0], board[1][1], board[2][2] ]) # upper-left diagonal
            checks.append([ board[2][0], board[1][1], board[0][2] ]) # upper-right diagonal
            return checks
        else:
            return checks


    if (row == 0 and col == 0) or (row == 2 and col == 2): # upper-left diagonal
        checks.append([ board[0][0], board[1][1], board[2][2] ])
        return checks

        
    # else ... upper-right diagonal
    checks.append([ board[2][0], board[1][1], board[0][2] ])
    return checks


def score_moves(potential_moves, bot, user, board):
    '''
        Scores each potential move the bot may make
        where low scores =>  bad moves for ai
        where big scores => good moves for ai
    '''
    scores = collections.Counter()


    if len(potential_moves) == 9: # value corners when the board is empty
        
        for move in potential_moves:
            if _is_corner(move):
                scores[move] += 50
            elif _is_edge(move):
                scores[move] += 25
            else: # center location of board
                scores[move] += 40

    else:

        for move in potential_moves:

            # just get the list of checks that include rows, columns, and diagonals to check
            row = move[0]
            col = move[1]

            # must check the row, colum, and potential diagonal(s)
            checks = [board[row], [board[0][col], board[1][col], board[2][col]] ]
            checks = get_diag(row, col, board, checks)

            
            for line in checks:

                # where we score potential moves
                
                user_count = line.count(user)
                bot_count = line.count(bot)
                
                if bot_count == user_count:
                    scores[move] -= 5
                    
                if user_count == 1 and bot_count == 0:
                    scores[move] += 20
                    
                    if 1 == move[0] == move[1]:
                        scores[move] += 10
                        
                elif bot_count == 2 and user_count == 0:
                    scores[move] += 1000
                    
                elif user_count == 2 and bot_count == 0:
                    scores[move] += 500
                    
                elif 0 == user_count == bot_count:
                    scores[move] += 5

    return scores
    



def easy_logic(potential_moves, bot, user, board):
    '''
    find WORST possible move for the bot to make
    where the user has best chance of winning
    '''
    scores = score_moves(potential_moves, bot, user, board)

    lowest_score = scores[potential_moves[0]]
    lowest_move = potential_moves[0]

    for move in scores.keys():
        if scores[move] < lowest_score:
            
            lowest_score = scores[move]
            lowest_move = move
    
    return lowest_move[0],lowest_move[1]


def hard_logic(potential_moves, bot, user, board):
    '''
    find BEST possible move for the bot to make
    where the user has best chance of winning
    '''
 
    scores = score_moves(potential_moves, bot, user, board)

    best_score = scores[potential_moves[0]]
    best_move = potential_moves[0]


    for move in scores.keys():
        
        if scores[move] > best_score:
            
            best_score = scores[move]
            best_move = move
    
    return best_move[0],best_move[1]


def determine(board, bot_value, user_value, logic_version):

    potential_moves = []

    for x in range(3):
        for y in range(3):
            if board[x][y] == '-': # may change later to other value
                potential_moves.append((x,y))


    if logic_version == 0:
        return random_logic(potential_moves)

    elif logic_version == 1:
        return easy_logic(potential_moves, bot_value, user_value, board)
   
    elif logic_version == 2:
        return hard_logic(potential_moves, bot_value, user_value, board)

