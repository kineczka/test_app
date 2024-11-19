# model.py
import sqlite3
from datetime import datetime, timedelta

class Model:
    def __init__(self):
        self.connection = sqlite3.connect('app.db')
        self.connection.row_factory = sqlite3.Row  # Umożliwia dostęp do kolumn po nazwie
        self.cursor = self.connection.cursor()

    def get_courses(self):
        query = "SELECT id, name FROM courses"
        self.cursor.execute(query)
        courses = self.cursor.fetchall()
        return [{'id': course['id'], 'name': course['name']} for course in courses]

    def get_statistics(self):
        # Pobieramy historię przerobionych słówek
        query = """
            SELECT practice_date, COUNT(DISTINCT word_id) as word_count
            FROM word_practice_log
            GROUP BY practice_date
            ORDER BY practice_date DESC
            LIMIT 7  -- Ograniczamy do ostatnich 7 dni
        """
        self.cursor.execute(query)
        stats = self.cursor.fetchall()
        history = [{'date': row['practice_date'], 'word_count': row['word_count']} for row in stats]
        return history

    def get_word_counts(self, course_id):
        counts = {}
        today = datetime.now().strftime('%Y-%m-%d')

        # Liczba słówek w kategorii NOWE
        query = """
            SELECT COUNT(*) FROM words
            WHERE course_id = ? AND category = 'NOWE'
        """
        self.cursor.execute(query, (course_id,))
        counts['NOWE'] = self.cursor.fetchone()[0]

        # Liczba słówek w kategorii POWTÓRKI
        query = """
            SELECT COUNT(*) FROM words
            WHERE course_id = ? AND category = 'POWTÓRKI' AND date(next_review_date) <= date(?)
        """
        self.cursor.execute(query, (course_id, today))
        counts['POWTÓRKI'] = self.cursor.fetchone()[0]

        # Liczba słówek w kategorii UTRWAL
        query = """
            SELECT COUNT(*) FROM words
            WHERE course_id = ? AND category = 'UTRWAL'
        """
        self.cursor.execute(query, (course_id,))
        counts['UTRWAL'] = self.cursor.fetchone()[0]

        return counts

    def get_next_words(self, course_id, category):
        today = datetime.now().strftime('%Y-%m-%d')
        if category == 'NOWE':
            # Pobierz 10 losowych słówek z kategorii NOWE
            query = """
                SELECT * FROM words
                WHERE course_id = ? AND category = 'NOWE'
                ORDER BY RANDOM()
                LIMIT 10
            """
            self.cursor.execute(query, (course_id,))
            words = self.cursor.fetchall()
        elif category == 'POWTÓRKI':
            # Pobierz słówka z kategorii POWTÓRKI, których data powtórki jest dzisiaj lub wcześniej
            query = """
                SELECT * FROM words
                WHERE course_id = ? AND category = 'POWTÓRKI' AND date(next_review_date) <= date(?)
                ORDER BY next_review_date ASC
            """
            self.cursor.execute(query, (course_id, today))
            words = self.cursor.fetchall()
        elif category == 'UTRWAL':
            # Pobierz wszystkie słówka z UTRWAL
            query = """
                SELECT * FROM words
                WHERE course_id = ? AND category = 'UTRWAL'
                ORDER BY RANDOM()
            """
            self.cursor.execute(query, (course_id,))
            words = self.cursor.fetchall()
        else:
            words = []
        return words

    def update_word_status(self, word_id, user_choice, current_category):
        # Pobierz aktualne dane słówka
        query = "SELECT * FROM words WHERE id = ?"
        self.cursor.execute(query, (word_id,))
        word = self.cursor.fetchone()
        n = word['correct_count'] or 0  # Ilość razy z rzędu zaznaczone WIEM

        # Zapisywanie logu praktyki słówka
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
            INSERT INTO word_practice_log (word_id, practice_date)
            VALUES (?, ?)
        """
        self.cursor.execute(query, (word_id, today))

        if current_category in ['NOWE', 'POWTÓRKI']:
            if user_choice == 'WIEM':
                n += 1
                # Oblicz kiedy następna powtórka
                days = 3 * n
                next_review_date = datetime.now() + timedelta(days=days)
                # Uaktualniamy kategorię na POWTÓRKI i ustawiamy next_review_date
                query = """
                    UPDATE words
                    SET category = 'POWTÓRKI', correct_count = ?, next_review_date = ?
                    WHERE id = ?
                """
                self.cursor.execute(query, (n, next_review_date.strftime('%Y-%m-%d'), word_id))
            elif user_choice == 'PRAWIE':
                n = max(n, 1)  # Jeśli n jest 0, ustaw na 1
                # Oblicz kiedy następna powtórka
                days = 2 * n
                next_review_date = datetime.now() + timedelta(days=days)
                # Dodajemy do UTRWAL
                query = """
                    UPDATE words
                    SET category = 'UTRWAL', correct_count = ?, next_review_date = ?
                    WHERE id = ?
                """
                self.cursor.execute(query, (0, next_review_date.strftime('%Y-%m-%d'), word_id))
            elif user_choice == 'NIE WIEM':
                n = 0  # Resetujemy licznik poprawnych odpowiedzi
                next_review_date = datetime.now() + timedelta(days=1)
                # Dodajemy do UTRWAL
                query = """
                    UPDATE words
                    SET category = 'UTRWAL', correct_count = ?, next_review_date = ?
                    WHERE id = ?
                """
                self.cursor.execute(query, (n, next_review_date.strftime('%Y-%m-%d'), word_id))
        elif current_category == 'UTRWAL':
            if user_choice == 'WIEM':
                # Przenosimy słówko z powrotem do POWTÓRKI
                query = """
                    UPDATE words
                    SET category = 'POWTÓRKI'
                    WHERE id = ?
                """
                self.cursor.execute(query, (word_id,))
            elif user_choice == 'NIE WIEM':
                # Nic nie zmieniamy, słówko pozostaje w UTRWAL
                pass

        self.connection.commit()

    def get_all_words_for_course(self, course_id):
        query = """
            SELECT word_pl, word_en FROM words
            WHERE course_id = ?
            ORDER BY word_pl
        """
        self.cursor.execute(query, (course_id,))
        words = self.cursor.fetchall()
        return words

    def close_connection(self):
        self.connection.close()
