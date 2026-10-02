import mysql.connector

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""         # Isi jika MySQL Anda menggunakan password
        self.database = "perpustakaan"  # GANTI dengan nama database Anda di Laragon

    def get_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except mysql.connector.Error as err:
            print(f"\n[ERROR DATABASE]: {err}")
            return None