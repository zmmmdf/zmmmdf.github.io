import curses
import subprocess
import time

def execute_script(script):
    command = ["python3.12", "-u", "./funcs/" + script]
    print(command)
    subprocess.run(command)

def intro_animation(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    time.sleep(1)

    # Color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Intro text
    intro_text = [
        " ________  ___      ___    ___ ________  _____ ______      ",
        "|\\_____  \\|\\  \\    |\\  \\  /  /|\\   __  \\|\\   _ \\  _   \\    ",
        "\\|___/  / /\\  \\   \\ \\  \\/  / | \\  \\|\\  \\ \\  \\\\\\__\\ \\  \\   ",
        "    /  /_/__\\  \\   \\ \\    / / \\ \\   __  \\ \\  \\|__| \\  \\  ",
        "   /  /________\\  \\   \\/  /  /   \\ \\  \\ \\  \\ \\  \\    \\  \\ ",
        "  |\__________\\ \\__\\__/  / /      \\ \\__\\ \\__\\ \\__\\    \\__\\",
        "   \\|________|\\|__|\\___/ /        \\|__|\\|__|\\|__|     \\|__|",
        "                 \\|___|/                                    ",
        "                                                            ",
        "                                                            "
    ]

    # Display intro text with colors
    for row, line in enumerate(intro_text):
        for col, char in enumerate(line):
            if char != ' ':
                if col % 2 == 0:
                    stdscr.addstr(row + 2, col + 2, char, curses.color_pair((row + col) % 4 + 1))
                else:
                    stdscr.addstr(row + 2, col + 2, char, curses.color_pair((row + col) % 4 + 1) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.0005)

    stdscr.getch()

def main(stdscr):
    intro_animation(stdscr)

    options = [
        "build_cards.py",
        "extract_cses.py",
        "extract_eolymp.py",
        "import_cses.py",
        "import_eolymp.py"
    ]

    while True:
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_row_idx = 0

        options_menu = ["Build Cards", "Extract CSES", "Extract Eolymp", "Import CSES", "Import Eolymp", "Exit"]

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            title = "Menu"
            stdscr.addstr(0, w//2 - len(title)//2, title)

            for idx, option in enumerate(options_menu):
                x = w//2 - len(option)//2
                y = h//2 - len(options_menu)//2 + idx
                if idx == current_row_idx:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, option)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, option)

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_DOWN and current_row_idx < len(options_menu) - 1:
                current_row_idx += 1
            elif key == curses.KEY_UP and current_row_idx > 0:
                current_row_idx -= 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row_idx == len(options_menu) - 1:
                    return
                else:
                    execute_script(options[current_row_idx])
                    break

if __name__ == "__main__":
    curses.wrapper(main)
