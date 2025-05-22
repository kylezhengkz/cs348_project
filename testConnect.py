import psycopg2


DATABASE = "postgres"
USERNAME = "postgres"
PASSWORD = "DatabaseSpring2025#"
HOST = "cs348database.ch2a26o0uum7.us-east-2.rds.amazonaws.com"
PORT = "5432"


if __name__ == "__main__":
    conn = psycopg2.connect(database = DATABASE, user = USERNAME, password = PASSWORD, host = HOST, port = PORT)

    print(f"TYPER: {type(conn)}")
    conn.close()
    print("Successfully connected to the database")