import sqlite3
import math
import random

def get_tablename():
    print('Enter your desired table: ')
    return str(input())
# add_data generates sales data for a year
def add_data():
    try:
        # Connect to db 
        db_connection = sqlite3.connect('Verkaufsdaten.db')
        cursor = db_connection.cursor()
        print("Connected to database!")
        tablename = get_tablename()
        # Generate data for a year in a loop
        for i in range(1, 365):
            # Valentines day
            if (40 <= i <= 45):
                rand_int = random.randint(100, 150)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Black Friday
            if (300 <= i <= 307):
                rand_int = random.randint(100, 150)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Pre-Christmas-Time
            if (335 <= i <= 356):
                rand_int = random.randint(100, 150)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Christmas (Holidays, DROP)
            if (357 <= i <= 361):
                rand_int = round(random.uniform(30, 20), 2)
                print(rand_int)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Every other day of  the year
            else:
                sinus_result = 10 * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Try to insert the result into the db
            try: 
                #insert_query = f'INSERT INTO {tablename} (day, sales) Values ({i}, {round(sinus_result, 2)})'
                update_statement = f'UPDATE {tablename} SET sales = {round(sinus_result, 2)} WHERE day = {i}'
                cursor.execute(update_statement)
                db_connection.commit()
            # Error handling
            except sqlite3.Error as error:
                print('Error while inserting to your sqlite database.', error)
        # Select statement to see the results
        select_query = f'SELECT * FROM {tablename}'
        cursor.execute(select_query)
        record = cursor.fetchall()
        print("ma data: ", record[0])
        cursor.close()
    # Error handling
    except sqlite3.Error as error:
        print('Error while connecting to your sqlite database.', error)
    # Close db connection
    finally:
        if db_connection:
            db_connection.close()
            print('The connection to your database was closed.')

add_data()