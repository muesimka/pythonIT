import pymysql
import pymysql.cursors


class Database:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )

    def insert_users(self, email, password):
        sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (email, password))
        self.connection.commit()

    def insert_classes(self, places1, places2):
        sql = "INSERT INTO classes (class_name, places) VALUES (%s, %s)"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (places1, places2))
        self.connection.commit()

    def select_classes(self):
        sql = "SELECT * FROM classes"
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def select_users(self, email):
        sql = "SELECT * FROM users WHERE email = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (email,))
            return cursor.fetchone()
