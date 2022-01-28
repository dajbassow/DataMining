import sqlite3
import math
import random
import matplotlib.pyplot as plt

# Connect to db
def get_db_connection():
    try:
        db_connection = sqlite3.connect('Verkaufsdaten.db')
        cursor = db_connection.cursor()
        print("Connected to database!")
        return cursor,db_connection
    # Error handling
    except sqlite3.Error as error:
        print('Error while connecting to your sqlite database.', error)


# Close db connection
def close_db_connection():
    if db_connection:
        cursor.close()
        db_connection.close()
        print("The db connection was closed.")


# Get table name from user
def get_table_name():
    print('Enter your desired table: ')
    return str(input())


# generate_data generates sales data for a year
def generate_data(cursor, db_connection):
    # Get table name as input from user
    table_name = get_table_name()

    # Generate data for a year in a loop
    for i in range(1, 365):
        # Valentines day
        if 40 <= i <= 45:
            rand_int = random.randint(100, 150)
            sinus_result = rand_int * math.sin((i + 80) * 8 * math.pi / 365) + 30
        # Black Friday
        if 300 <= i <= 307:
            rand_int = random.randint(100, 150)
            sinus_result = rand_int * math.sin((i + 80) * 8 * math.pi / 365) + 30
        # Pre-Christmas-Time
        if 335 <= i <= 356:
            rand_int = random.randint(100, 150)
            sinus_result = rand_int * math.sin((i + 80) * 8 * math.pi / 365) + 30
        # Christmas (Holidays, DROP)
        if 357 <= i <= 361:
            rand_int = round(random.uniform(30, 20), 2)
            print(rand_int)
            sinus_result = rand_int * math.sin((i + 80) * 8 * math.pi / 365) + 30
        # Every other day of  the year
        else:
            sinus_result = 10 * math.sin((i + 80) * 8 * math.pi / 365) + 30

        # Try to insert the result into the db
        try:
            # insert_query = f'INSERT INTO {tablename} (day, sales) Values ({i}, {round(sinus_result, 2)})'
            update_statement = f'UPDATE {table_name} SET sales = {round(sinus_result, 2)} WHERE day = {i}'
            cursor.execute(update_statement)
            db_connection.commit()
        # Error handling
        except sqlite3.Error as error:
            print('Error while inserting to your sqlite database.', error)


# SELECT QUERY
def fetch_data(cursor):
    table_name = get_table_name()
    select_query = f'SELECT * FROM {table_name}'
    cursor.execute(select_query)
    record = cursor.fetchall()
    return record


def draw_plot_data(cursor):
    table_name = get_table_name()
    sqlite_select_query = f'SELECT day FROM {table_name}'
    cursor.execute(sqlite_select_query)
    recordX = cursor.fetchall()
    sqlite_select_query = f'SELECT sales FROM {table_name}'
    cursor.execute(sqlite_select_query)
    recordY = cursor.fetchall()

    plt.plot(recordX, recordY)
    plt.show()


cursor, db_connection = get_db_connection()
generate_data(cursor, db_connection)
record = fetch_data(cursor)
draw_plot_data(cursor)
close_db_connection(cursor, db_connection)

print(record[0])
