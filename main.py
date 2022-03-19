import random
import time


def computer_move(computer_moves, player_board, computer_board):
    print("computer is thinking...")
    time.sleep(3)
    while len(computer_moves) > 0:
        computer_move = computer_moves.pop()
        if not player_board & (1 << computer_move):
            return computer_board | (1 << computer_move), computer_moves
    return computer_board, computer_moves


def player_move(computer_board, player_board, player_move):
    if not computer_board & (1 << player_move) and not player_board & (
            1 << player_move):
        return player_board | (1 << player_move), True
    else:
        return None, False


def check_win(win_conditions, computer_board, player_board):
    for win_condition in win_conditions:
        if win_condition & player_board == win_condition:
            return "player"
        elif win_condition & computer_board == win_condition:
            return "computer"
        elif computer_board & player_board == 0b111111111:
            return "tie"
    return ""


def get_player_move():
    return int(validate_and_input("""Choose your move 0,1,2
                 3,4,5
                 6,7,8\n""", ['0', '1', '2', '3', '4', '5', '6', '7', '8']))


def print_board(computer_board, player_board):
    board_string = """
 {0} | {1} | {2} 
-----------      
 {3} | {4} | {5} 
-----------   
 {6} | {7} | {8} 
"""
    board_positions = []
    for element in range(0, 9):
        if computer_board & (1 << element):
            board_positions.append('o')
        elif player_board & (1 << element):
            board_positions.append('x')
        else:
            board_positions.append(' ')
    print(board_string.format(*board_positions))


def is_starting_player():
    coin_choice = validate_and_input("To decide who goes first, lets flip a coin, (h)eads or (t)ails?", ['h', 't'])
    print("flipping coin...\n")
    time.sleep(1)
    if (random.randint(0, 2) == 1 and coin_choice == 'h') or (random.randint(0, 2) == 0 and coin_choice == 't'):
        print("Good guess, you go first!\n")
        return True
    else:
        print("Better luck next time, computer goes first\n")
        return False


def sleep_input(string):
    input_str = input(string)
    time.sleep(0.5)
    return input_str


def validate_and_input(string, valid_input):
    input = '----'
    while input not in valid_input:
        input = sleep_input(string)
    return input


def get_computer_moveset():
    computer_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(computer_moves)
    return computer_moves


def get_constants():
    return 0, 0, [0b111000000,
                  0b000111000,
                  0b000000111,
                  0b100100100,
                  0b010010010,
                  0b001001001,
                  0b100010001,
                  0b001010100], get_computer_moveset()


def get_player_board_after_move(computer_board, player_board):
    success = False
    while not success:
        move = get_player_move()
        temp, success = player_move(computer_board, player_board, move)
    return temp


def check_and_act_on_end_conditions(player_board, computer_board, win_conditions):
    condition = check_win(win_conditions, computer_board, player_board)
    if condition == '':
        return False
    if condition == "tie":
        print("DRAW! Almost, but not quite 😐")
    if condition == "player":
        print("Ayyy, you won! Nice one 😊")
    if condition == "computer":
        print("You got beaten, damn 💩")
    return True


def main():
    player_board, computer_board, win_conditions, computer_moves = get_constants()

    print("----------------\nWelcome to tic-tac-toe!\n----------------\n")
    is_player_turn = is_starting_player()
    finished = False
    while not finished:
        if is_player_turn:
            player_board = get_player_board_after_move(computer_board, player_board)
        else:
            computer_board, computer_moves = computer_move(computer_moves, player_board, computer_board)
        print_board(computer_board, player_board)
        is_player_turn = not is_player_turn
        finished = check_and_act_on_end_conditions(player_board, computer_board, win_conditions)


if __name__ == '__main__':
    main()
