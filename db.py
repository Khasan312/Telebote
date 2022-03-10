from datetime import date
import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,)
            )

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?",
                (
                    nickname,
                    user_id,
                ),
            )

    def get_signup(self, user_id):
        with self.connection:
            # result = self.cursor.execute("SELECT 'signup' FROM 'users' WHERE 'user_id' = ? ", (user_id,)) #.fetchall()
            result = self.cursor.execute(
                "SELECT `signup` FROM `users` WHERE user_id = ? ", (user_id,)
            ).fetchall()
            # print("➡️ result :", result)
            # result = self.cursor.execute("SELECT 'signup' FROM 'users'").fetchall()

            for row in result:
                signup = str(row[0])
            # print("➡️ signup :", signup)
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `signup` = ? WHERE `user_id` = ?",
                (
                    signup,
                    user_id,
                ),
            )

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `nickname` FROM `users` WHERE `user_id` = ?",
                (user_id,),
            ).fetchall()
            # print("➡️ result :", result)
            for row in result:
                nickname = str(row[0])
            return nickname

    def set_date_of_birth(self, user_id, date_of_birth):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `date_of_birth` = ? WHERE `user_id` = ?",
                (
                    date_of_birth,
                    user_id,
                ),
            )

    def get_date_of_birth(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `date_of_birth` FROM `users` WHERE `user_id` = ?",
                (user_id,),
            ).fetchall()
            for row in result:
                date_of_birth = str(row[0])
            return date_of_birth
    
    def get_position(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `position` FROM `users` WHERE `user_id` = ?",
                (user_id,),
            ).fetchall()
            for row in result:
                position = str(row[0])
            return position

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add(self, position, user_id):
        self.cursor.execute("INSERT INTO users (position, user_id) VALUES (?, ?)", (position, user_id,))
        self.connection.commit()

    def set_position(self, user_id, position):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `position` = ? WHERE `user_id` = ?",
                (
                    position,
                    user_id,
                ),
            )