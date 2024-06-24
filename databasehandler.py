import pymysql

class DatabaseHandler:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(**self.db_config)
        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            return None
