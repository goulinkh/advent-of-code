def sum_of_unmarked_numbers(board):
    unmarked_numbers_sum = 0
    for line in board:
        for n in line:
            if not n["is-drawn"]:
                unmarked_numbers_sum += n["value"]
    return unmarked_numbers_sum


def find_index(line, number):
    for i in range(len(line)):
        if line[i]["value"] == number:
            return i
    return None


def play_step(boards, drawn_number):
    for board in boards:
        if not board:
            continue
        for line in board:
            idx = find_index(line, drawn_number)
            if idx != None:
                line[idx]["is-drawn"] = True
                break
    return boards


def check_for_winner(boards, draw_series):
    for board_idx in range(len(boards)):
        board = boards[board_idx]
        if not board:
            continue
        # Check horizontal
        for line in board:
            win = True
            for e in line:
                try:
                    draw_series.index(e["value"])
                except ValueError:
                    win = False
            if win:
                return board_idx
        # Check vertical
        for i in range(len(board)):
            temp_list = []
            for line in board:
                temp_list.append(line[i])

            win = True
            for e in temp_list:
                try:
                    draw_series.index(e["value"])
                except ValueError:
                    win = False
            if win:
                return board_idx
    return None


lines = open("./input.txt", "r").read().split("\n")

# Parse input data
numbers_to_draw = list(map(int, lines.pop(0).split(",")))
lines = "\n".join(lines)
boards = lines.split("\n\n")
for i in range(len(boards)):
    board = boards[i]
    board = board.split("\n")
    # First line is empty
    board = [line.split() for line in board if line]
    for y in range(len(board)):
        board[y] = [{"value": int(element), "is-drawn": False}
                    for element in board[y]]
    boards[i] = board

drawn_numbers = []
fst_winner, lst_winner = None, None
scores = []

# Run the game
for n in numbers_to_draw:
    drawn_numbers.append(n)
    boards = play_step(boards, n)
    winner_board_idx = check_for_winner(boards, drawn_numbers)
    while winner_board_idx != None:
        score = sum_of_unmarked_numbers(
            boards[winner_board_idx]) * n
        if score:
            boards[winner_board_idx] = None
            if not fst_winner:
                fst_winner = ("score=", score, ", board n°=", winner_board_idx)
            lst_winner = ("score=", score, ", board n°=", winner_board_idx)
        winner_board_idx = check_for_winner(boards, drawn_numbers)

print("part1:", fst_winner, "part2:", lst_winner)
