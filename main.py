import os
import sys
import time
import random


colors = {
    'R': '\033[31m',
    'G': '\033[32m',
    'Y': '\033[33m',
    'B': '\033[34m',
    'M': '\033[35m',
    'C': '\033[36m',
}
BROWN = "\033[38;5;94m"
RESET = '\033[0m'

tree = [
    "        *        ",
    "       ***       ",
    "      *****      ",
    "     *******     ",
    "    *********    ",
    "   ***********   ",
    "  *************  ",
    " *************** ",
    "       |||",
    "       |||"
]

MAX_TREE_WIDTH = max(len(line) for line in tree)
TREE_LEFT_COL = 2
TREE_TOP_ROW = 2
LYRIC_BASE_COL = TREE_LEFT_COL + MAX_TREE_WIDTH + 4
PARK_ROW = TREE_TOP_ROW + len(tree) + 6

# Tempo
TEXT_DELAY = 0.08
TREE_BLINK_INTERVAL = 0.15
last_tree_blink = 0.0


lyrics = [
    "My God, I thought you were someone to rely on",
    "Me? I guess I was a shoulder to cry on",
    "A face on a lover with a fire in his heart",
    "A man under cover, but you tore me apart",
    "Oh, oh now I've found a real love",
    "You'll never fool me again"
]


def draw_tree_at_position():
    for row_index, line in enumerate(tree):
        row = TREE_TOP_ROW + row_index
        col = TREE_LEFT_COL
        print(f'\033[{row};{col}H', end='')

        colored_line = ""
        for char in line:
            if char == '*':
                color = random.choice(list(colors.values()))
                colored_line += f'{color}{char}{RESET}'
            elif char == '|':
                colored_line += f'{BROWN}{char}{RESET}'
            else:
                colored_line += char

        print(colored_line.ljust(MAX_TREE_WIDTH), end='')

    print(f'\033[{PARK_ROW};1H', end='')

    sys.stdout.flush()


def blink_tree():
    global last_tree_blink
    now = time.time()
    if now - last_tree_blink >= TREE_BLINK_INTERVAL:
        draw_tree_at_position()
        last_tree_blink = now

def blink_for(duration):
    end = time.time() + duration
    while time.time() < end:
        draw_tree_at_position()
        time.sleep(TREE_BLINK_INTERVAL)


def show_lyrics_with_tree():
    base_row = TREE_TOP_ROW + 1

    for i, line in enumerate(lyrics):
        row = base_row + i
        col = LYRIC_BASE_COL + i

        current = ""
        for ch in line:
            current += ch

            blink_tree()

            # Skriv teksten så langt
            print(f'\033[{row};{col}H', end='')
            print(f'{colors['G']}{current}{RESET}', end='')

            print(f'\033[{PARK_ROW};1H', end='')

            sys.stdout.flush()

            time.sleep(TEXT_DELAY)  # hastighet på tekst

        blink_for(1.0)


def wait_with_blink():
    try:
        while True:
            draw_tree_at_position()
            time.sleep(0.15)
    except KeyboardInterrupt:
        pass


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[?25l', end='')
    sys.stdout.flush()

    try:
        # 1) Treet blinker og teksten kommer opp
        show_lyrics_with_tree()

        # 2) Treet blinker videre til vi trykker ctrl+C
        wait_with_blink()
    finally:
        print('\033[?25h', end='')
        print(RESET)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
