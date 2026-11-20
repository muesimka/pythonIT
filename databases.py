import pymysql.cursors


class Database:
    def __init__(self, host, user, password, database):

        self.connection = pymysql.connect(host=host, user=user, password=password, database=database)

    def insert_users(self, login, password):
        cursor = self.connection.cursor()
        sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (login, password))
            self.connection.commit()

    def insert_classes(self, places1, places2):
        cursor = self.connection.cursor()
        sql = "INSERT INTO classes (class_name, places) VALUES (%s, %s)"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (places1, places2))
            self.connection.commit()


    def select_classes(self):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM classes"
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            classes = cursor.fetchall()
            for row in classes:
                print(row)

    def select_users(self, login):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM users WHERE login = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, login)
            user = cursor.fetchone()
            print(user)
