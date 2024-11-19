#pip install freezegun
# main.py
import curses
from controller import Controller
from freezegun import freeze_time

#@freeze_time("2024-11-11")
def main(stdscr):
    controller = Controller(stdscr)
    controller.run()

if __name__ == "__main__":
    curses.wrapper(main)
