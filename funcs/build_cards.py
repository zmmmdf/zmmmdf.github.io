import json
import os
import curses

def print_menu(stdscr, options, current_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = "Select type of problem set:"
    stdscr.addstr(0, w//2 - len(title)//2, title)
    for idx, option in enumerate(options):
        x = w//2 - len(option)//2
        y = h//2 - len(options)//2 + idx
        if idx == current_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    options = ["CSES", "Eolymp", "CodeForces"]
    current_row_idx = 0
    print_menu(stdscr, options, current_row_idx)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_DOWN and current_row_idx < len(options) - 1:
            current_row_idx += 1
        elif key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            cata = options[current_row_idx].lower()
            break

        print_menu(stdscr, options, current_row_idx)


    with open(f'./data/{cata}.json') as json_file:
        data = json.load(json_file)

    solution_files = os.listdir(f'./solutions/{cata}')

    html_cards = ""

    for entry in data:
        problem_href = entry['problem_href']
        problem_title = entry['problem_title']
        lang = entry['lang']

        if f"{problem_title}.html" in solution_files:
            solution_file = f"./solutions/{cata}/{problem_title}.html" 
        else: continue

        html_card = f"""
        <div class="card bg-dark">
            <img src="./img/{cata}.png" style="padding: 50px;" class="card-img-top">
            <div class="card-body">
                <h5 class="card-title">{problem_title}</h5>
                <p class="card-text">
                    <a href="{problem_href}" style="text-decoration: none;">Problem link</a><br>
                    Solution in {lang}
                </p>
            </div>
            <div class="card-footer">
                <a href="./{solution_file}" class="btn">Read more</a>
            </div>
        </div>
        """

        html_cards += html_card

    with open(f'./dist/{cata}_cards.html', 'w') as html_file:
        html_file.write(html_cards)

curses.wrapper(main)
