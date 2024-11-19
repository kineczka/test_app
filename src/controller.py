# controller.py
import curses
from model import Model
from view import View

class Controller:
    def __init__(self, stdscr):
        self.model = Model()
        self.view = View(stdscr)
        self.stdscr = stdscr

    def run(self):
        self.view.display_start_screen()
        while True:
            options = ["Kursy", "Statystyki", "Katalog Kursów", "Wyjście"]
            selected_index = 0
            while True:
                self.view.display_menu(options, selected_index)
                key = self.view.stdscr.getch()
                if key == curses.KEY_UP and selected_index > 0:
                    selected_index -= 1
                elif key == curses.KEY_DOWN and selected_index < len(options) - 1:
                    selected_index += 1
                elif key in [curses.KEY_ENTER, ord('\n')]:
                    break
            choice = options[selected_index]
            if choice == "Kursy":
                self.show_courses()
            elif choice == "Statystyki":
                self.show_statistics()
            elif choice == "Katalog Kursów":
                self.show_course_catalog()
            elif choice == "Wyjście":
                self.model.close_connection()
                break

    def show_courses(self):
        courses = self.model.get_courses()
        selected_index = 0
        while True:
            self.view.display_courses(courses, selected_index)
            key = self.view.stdscr.getch()
            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1
            elif key == curses.KEY_DOWN and selected_index < len(courses) - 1:
                selected_index += 1
            elif key in [curses.KEY_ENTER, ord('\n')]:
                selected_course = courses[selected_index]
                self.learn_course(selected_course)
            elif key == ord(' '):
                break

    def learn_course(self, course):
        course_name = course['name']
        course_id = course['id']
        categories = ["POWTÓRKI", "UTRWAL", "NOWE"]
        selected_category_index = 0
        while True:
            word_counts = self.model.get_word_counts(course_id)
            self.view.display_learning_screen(course_name, categories, selected_category_index, word_counts)
            key = self.view.stdscr.getch()
            if key == curses.KEY_LEFT and selected_category_index > 0:
                selected_category_index -= 1
            elif key == curses.KEY_RIGHT and selected_category_index < len(categories) - 1:
                selected_category_index += 1
            elif key in [curses.KEY_ENTER, ord('\n')]:
                selected_category = categories[selected_category_index]
                self.learn_words(course_id, selected_category)
                # Po nauce słówek odśwież licznik słówek
                continue
            elif key == ord(' '):
                break

    def learn_words(self, course_id, category):
        words = self.model.get_next_words(course_id, category)
        if not words:
            self.view.display_message("Brak słówek w tej kategorii.")
            return
        index = 0
        while index < len(words):
            word = words[index]
            self.view.display_word(word['word_pl'], word['example_en'])
            # Po naciśnięciu ENTER wyświetlamy tłumaczenie
            self.view.display_word_with_translation(
                word['word_pl'], word['word_en'], word['example_en'], word['example_pl']
            )
            # Użytkownik wybiera WIEM, PRAWIE, NIE WIEM
            if category == 'UTRWAL':
                choices = ["WIEM", "NIE WIEM"]
            else:
                choices = ["WIEM", "PRAWIE", "NIE WIEM"]
            selected_choice_index = 0
            while True:
                self.view.display_choices(choices, selected_choice_index)
                key = self.view.stdscr.getch()
                if key == curses.KEY_LEFT and selected_choice_index > 0:
                    selected_choice_index -= 1
                elif key == curses.KEY_RIGHT and selected_choice_index < len(choices) - 1:
                    selected_choice_index += 1
                elif key in [curses.KEY_ENTER, ord('\n')]:
                    user_choice = choices[selected_choice_index]
                    self.model.update_word_status(word['id'], user_choice, category)
                    break
            # Logika dla UTRWAL
            if category == 'UTRWAL' and user_choice == 'NIE WIEM':
                index += 1
                if index == len(words):
                    index = 0  # Wracamy do początku listy
                continue
            elif category == 'UTRWAL' and user_choice == 'WIEM':
                del words[index]
                if not words:
                    break
                continue
            else:
                index += 1

    def show_statistics(self):
        statistics = self.model.get_statistics()
        self.view.display_statistics(statistics)

    def show_course_catalog(self):
        courses = self.model.get_courses()
        selected_index = 0
        while True:
            self.view.display_courses(courses, selected_index)
            key = self.view.stdscr.getch()
            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1
            elif key == curses.KEY_DOWN and selected_index < len(courses):
                selected_index += 1
            elif key in [curses.KEY_ENTER, ord('\n')]:
                if selected_index < len(courses):
                    selected_course = courses[selected_index]
                    self.show_course_words(selected_course)
                else:
                    break
            elif key == ord(' '):
                break

    def show_course_words(self, course):
        course_id = course['id']
        course_name = course['name']
        words = self.model.get_all_words_for_course(course_id)
        self.view.display_course_words(course_name, words)

