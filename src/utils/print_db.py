import argparse
import db_guard

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_path', help='path of the database file')
    args = parser.parse_args()

    with db_guard.SqliteGuard(args.db_path) as guard:
        conn = guard.conn
        cursor = guard.cursor

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("table of database:")
        for table in tables:
            print(table[0])

            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print("column: ", [col[1] for col in columns])

            cursor.execute(f"SELECT * FROM {table[0]}")
            rows = cursor.fetchall()
            print("data of table:")
            for i, row in enumerate(rows):
                print(i, ':', row)
            print("-" * 50)
