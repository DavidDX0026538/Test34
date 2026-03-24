#!/usr/bin/env python3
import curses
import random
import time

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],                          # I
    [[1, 1], [1, 1]],                         # O
    [[1, 1, 1], [0, 1, 0]],                   # T
    [[1, 1, 1], [1, 0, 0]],                   # L
    [[1, 1, 1], [0, 0, 1]],                   # J
    [[0, 1, 1], [1, 1, 0]],                   # S
    [[1, 1, 0], [0, 1, 1]],                   # Z
]

COLORS = [1, 2, 3, 4, 5, 6, 7]  # curses color pairs

BOARD_W = 10
BOARD_H = 20


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def valid(board, shape, ox, oy):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx, ny = ox + x, oy + y
                if nx < 0 or nx >= BOARD_W or ny >= BOARD_H:
                    return False
                if ny >= 0 and board[ny][nx]:
                    return False
    return True


def place(board, shape, ox, oy, color):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and oy + y >= 0:
                board[oy + y][ox + x] = color


def clear_lines(board):
    full = [i for i, row in enumerate(board) if all(row)]
    for i in full:
        del board[i]
        board.insert(0, [0] * BOARD_W)
    return len(full)


def draw(stdscr, board, shape, ox, oy, color, score, next_shape, next_color, game_over):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    off_x = (w - BOARD_W * 2 - 4) // 2
    off_y = (h - BOARD_H - 2) // 2

    # Border
    stdscr.attron(curses.color_pair(8))
    stdscr.addstr(off_y, off_x, "+" + "-" * (BOARD_W * 2) + "+")
    stdscr.addstr(off_y + BOARD_H + 1, off_x, "+" + "-" * (BOARD_W * 2) + "+")
    for i in range(BOARD_H):
        stdscr.addstr(off_y + 1 + i, off_x, "|")
        stdscr.addstr(off_y + 1 + i, off_x + BOARD_W * 2 + 1, "|")
    stdscr.attroff(curses.color_pair(8))

    # Board
    for y in range(BOARD_H):
        for x in range(BOARD_W):
            c = board[y][x]
            if c:
                stdscr.attron(curses.color_pair(c))
                stdscr.addstr(off_y + 1 + y, off_x + 1 + x * 2, "[]")
                stdscr.attroff(curses.color_pair(c))

    # Current piece
    if not game_over:
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell and oy + y >= 0:
                    sy = off_y + 1 + oy + y
                    sx = off_x + 1 + (ox + x) * 2
                    if 0 <= sy < h and 0 <= sx + 1 < w:
                        stdscr.attron(curses.color_pair(color))
                        stdscr.addstr(sy, sx, "[]")
                        stdscr.attroff(curses.color_pair(color))

    # Info panel
    info_x = off_x + BOARD_W * 2 + 4
    stdscr.addstr(off_y, info_x, "TETRIS", curses.A_BOLD)
    stdscr.addstr(off_y + 2, info_x, f"Score: {score}")
    stdscr.addstr(off_y + 4, info_x, "Next:")
    for y, row in enumerate(next_shape):
        for x, cell in enumerate(row):
            if cell:
                stdscr.attron(curses.color_pair(next_color))
                stdscr.addstr(off_y + 5 + y, info_x + x * 2, "[]")
                stdscr.attroff(curses.color_pair(next_color))

    stdscr.addstr(off_y + 10, info_x, "Controls:", curses.A_BOLD)
    stdscr.addstr(off_y + 11, info_x, "← → Move")
    stdscr.addstr(off_y + 12, info_x, "↑  Rotate")
    stdscr.addstr(off_y + 13, info_x, "↓  Drop")
    stdscr.addstr(off_y + 14, info_x, "Space Hard drop")
    stdscr.addstr(off_y + 15, info_x, "Q  Quit")

    if game_over:
        msg = "GAME OVER!"
        mx = off_x + (BOARD_W * 2 - len(msg)) // 2 + 1
        my = off_y + BOARD_H // 2
        stdscr.attron(curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(my, mx, msg)
        stdscr.attroff(curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(my + 1, off_x + 2, "Press R to restart or Q to quit")

    stdscr.refresh()


def new_piece():
    idx = random.randint(0, len(SHAPES) - 1)
    return SHAPES[idx], COLORS[idx]


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    # Init colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED,     curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_GREEN,   curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_YELLOW,  curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLUE,    curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_CYAN,    curses.COLOR_CYAN)
    curses.init_pair(7, curses.COLOR_WHITE,   curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_WHITE,   curses.COLOR_BLACK)

    def start_game():
        board = [[0] * BOARD_W for _ in range(BOARD_H)]
        shape, color = new_piece()
        next_shape, next_color = new_piece()
        ox = BOARD_W // 2 - len(shape[0]) // 2
        oy = -len(shape)
        score = 0
        fall_speed = 0.5
        last_fall = time.time()
        game_over = False
        return board, shape, color, next_shape, next_color, ox, oy, score, fall_speed, last_fall, game_over

    board, shape, color, next_shape, next_color, ox, oy, score, fall_speed, last_fall, game_over = start_game()

    while True:
        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            break

        if game_over:
            if key == ord('r') or key == ord('R'):
                board, shape, color, next_shape, next_color, ox, oy, score, fall_speed, last_fall, game_over = start_game()
            draw(stdscr, board, shape, ox, oy, color, score, next_shape, next_color, game_over)
            time.sleep(0.05)
            continue

        if key == curses.KEY_LEFT and valid(board, shape, ox - 1, oy):
            ox -= 1
        elif key == curses.KEY_RIGHT and valid(board, shape, ox + 1, oy):
            ox += 1
        elif key == curses.KEY_UP:
            rotated = rotate(shape)
            if valid(board, rotated, ox, oy):
                shape = rotated
        elif key == curses.KEY_DOWN and valid(board, shape, ox, oy + 1):
            oy += 1
        elif key == ord(' '):
            while valid(board, shape, ox, oy + 1):
                oy += 1

        # Gravity
        now = time.time()
        if now - last_fall >= fall_speed:
            if valid(board, shape, ox, oy + 1):
                oy += 1
            else:
                place(board, shape, ox, oy, color)
                lines = clear_lines(board)
                score += [0, 100, 300, 500, 800][lines]
                fall_speed = max(0.05, 0.5 - score // 1000 * 0.05)
                shape, color = next_shape, next_color
                next_shape, next_color = new_piece()
                ox = BOARD_W // 2 - len(shape[0]) // 2
                oy = -len(shape)
                if not valid(board, shape, ox, oy):
                    game_over = True
            last_fall = now

        draw(stdscr, board, shape, ox, oy, color, score, next_shape, next_color, game_over)
        time.sleep(0.03)


if __name__ == "__main__":
    curses.wrapper(main)
