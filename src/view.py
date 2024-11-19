# view.py
#https://pl.rakko.tools/tools/68/ ascii art

import curses

class View:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)

    def display_start_screen(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        title = [
            r",------.  ,------.  ,----.    ,--. ,--. ,--.      ,---.   ,------.  ,--.  ,--. ,--. ,--. ,--. ",
            r"|  .--. ' |  .---' '  .-./    |  | |  | |  |     /  O  \  |  .--. ' |  ,'.|  | |  | |  .'   / ",
            r"|  '--'.' |  `--,  |  | .---. |  | |  | |  |    |  .-.  | |  '--'.' |  |' '  | |  | |  .   ' ",
            r"|  |\  \  |  `---. '  '--'  | '  '-'  ' |  '--. |  | |  | |  |\  \  |  | `   | |  | |  |\   \ ",
            r"`--' '--' `------'  `------'   `-----'  `-----' `--' `--' `--' '--' `--'  `--' `--' `--' '--' ",
        ]
        total_height = len(title)
        start_y = (height - total_height) // 2
        for i, line in enumerate(title):
            if len(line) > width:
                line = line[:width]
            self.stdscr.addstr(start_y + i, max(0, (width - len(line)) // 2), line)
        message = "Naciśnij dowolny klawisz, aby kontynuować"
        self.stdscr.addstr(height - 2, max(0, (width - len(message)) // 2), message)
        self.stdscr.refresh()
        self.stdscr.getch()

    def display_menu(self, options, selected_index):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        title = [
            r",------.  ,------.  ,----.    ,--. ,--. ,--.      ,---.   ,------.  ,--.  ,--. ,--. ,--. ,--. ",
            r"|  .--. ' |  .---' '  .-./    |  | |  | |  |     /  O  \  |  .--. ' |  ,'.|  | |  | |  .'   / ",
            r"|  '--'.' |  `--,  |  | .---. |  | |  | |  |    |  .-.  | |  '--'.' |  |' '  | |  | |  .   ' ",
            r"|  |\  \  |  `---. '  '--'  | '  '-'  ' |  '--. |  | |  | |  |\  \  |  | `   | |  | |  |\   \ ",
            r"`--' '--' `------'  `------'   `-----'  `-----' `--' `--' `--' '--' `--'  `--' `--' `--' '--' ",
        ]

        total_height = len(title)
        start_y = 2
        for i, line in enumerate(title):
            if len(line) > width:
                line = line[:width]
            self.stdscr.addstr(start_y + i, max(0, (width - len(line)) // 2), line)
        # Opcje menu
        menu_start_y = start_y + total_height + 1
        for idx, option in enumerate(options):
            x = max(0, (width - len(option)) // 2)
            y = menu_start_y + idx
            if idx == selected_index:
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(y, x, option)
                self.stdscr.attroff(curses.A_REVERSE)
            else:
                self.stdscr.addstr(y, x, option)
        self.stdscr.refresh()

    def display_courses(self, courses, selected_index):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        title = "Dostępne kursy:"
        self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.A_BOLD)
        for idx, course in enumerate([course['name'] for course in courses]):
            x = width // 2 - len(course) // 2
            y = 4 + idx
            if idx == selected_index:
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(y, x, course)
                self.stdscr.attroff(curses.A_REVERSE)
            else:
                self.stdscr.addstr(y, x, course)
        exit_message = "Naciśnij SPACJĘ, aby wrócić do menu głównego"
        self.stdscr.addstr(height - 2, (width - len(exit_message)) // 2, exit_message)
        self.stdscr.refresh()

    def display_learning_screen(self, course_name, categories, selected_category_index, word_counts):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        # nazwa kursu
        self.stdscr.addstr(0, (width - len(course_name)) // 2, course_name, curses.A_BOLD)
        # kategorie
        category_line = ""
        for idx, category in enumerate(categories):
            count = word_counts.get(category, 0)
            category_text = f"{category} ({count})"
            if idx == selected_category_index:
                category_line += f" [{category_text}] "
            else:
                category_line += f"  {category_text}  "
        self.stdscr.addstr(2, (width - len(category_line)) // 2, category_line)
        exit_message = "Naciśnij SPACJE, aby wrócić do wyboru kursu"
        self.stdscr.addstr(height - 2, (width - len(exit_message)) // 2, exit_message)
        self.stdscr.refresh()

    def display_word(self, word_pl, example_en):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(4, (width - len(word_pl))//2, word_pl, curses.A_BOLD)
        self.stdscr.addstr(7, (width - len(example_en))//2, example_en)

        self.stdscr.addstr(10, (width - len("Sprawdź"))//2, "Sprawdź", curses.A_REVERSE)
        self.stdscr.refresh()
        while True:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER, ord('\n')]:
                break

    def display_word_with_translation(self, word_pl, word_en, example_en, example_pl):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(4, (width - len(word_pl))//2, word_pl, curses.A_BOLD)
        self.stdscr.addstr(5, (width - len(word_en))//2, word_en)
        self.stdscr.addstr(7, (width - len(example_en))//2, example_en)
        self.stdscr.addstr(8, (width - len(example_pl))//2, example_pl)
        self.stdscr.refresh()

    def display_choices(self, choices, selected_choice_index):
        height, width = self.stdscr.getmaxyx()
        choices_line = ""
        for idx, choice in enumerate(choices):
            if idx == selected_choice_index:
                choices_line += f"[{choice}] "
            else:
                choices_line += f" {choice}  "
        self.stdscr.addstr(10, (width - len(choices_line))//2, choices_line)
        self.stdscr.refresh()

    def display_message(self, message):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(height//2, (width - len(message))//2, message)
        self.stdscr.refresh()
        self.stdscr.getch()

    def display_statistics(self, statistics):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        title = "Statystyki Praktyki (Ostatnie 7 dni)"
        self.stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)
        self.stdscr.addstr(1, 0, "-" * width)
        for idx, stat in enumerate(statistics):
            line = f"{stat['date']} - Przerobione słówka: {stat['word_count']}"
            self.stdscr.addstr(2 + idx, 2, line)
        exit_message = "Naciśnij SPACJĘ, aby wrócić"
        self.stdscr.addstr(height - 2, (width - len(exit_message)) // 2, exit_message)
        self.stdscr.refresh()
        while True:
            key = self.stdscr.getch()
            if key == ord(' '):
                break

    def display_course_words(self, course_name, words):
        height, width = self.stdscr.getmaxyx()
        max_lines = height - 4  # Ilość linii dostępnych na słówka
        total_pages = (len(words) + max_lines - 1) // max_lines
        page = 0
        while True:
            self.stdscr.clear()
            title = f"Kurs: {course_name} (Strona {page + 1}/{total_pages})"
            self.stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)
            self.stdscr.addstr(1, 0, "-" * width)
            start_idx = page * max_lines
            end_idx = min(start_idx + max_lines, len(words))
            for idx, word in enumerate(words[start_idx:end_idx]):
                word_line = f"{word['word_pl']} - {word['word_en']}"
                self.stdscr.addstr(2 + idx, 2, word_line)
            exit_message = "Naciśnij SPACJĘ, aby wrócić | Strzałki LEWO/PRAWO, aby zmienić stronę"
            self.stdscr.addstr(height - 2, (width - len(exit_message)) // 2, exit_message)
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key == ord(' '):
                break
            elif key == curses.KEY_RIGHT and page < total_pages - 1:
                page += 1
            elif key == curses.KEY_LEFT and page > 0:
                page -= 1
