import sqlite3
import math
import random

# add_data generates sales data for a year
def add_data():
    try:
        # Connect to db 
        db_connection = sqlite3.connect('Verkaufsdaten.db')
        cursor = db_connection.cursor()
        print("Connected to database!")
        # Generate data for a year in a loop
        for i in range(1, 365):
            # Valentines day
            if (i >= 40 & i<=45):
                rand_int = random.randint(20, 40)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Black Friday
            if (i >= 300 & i<=307):
                rand_int = random.randint(35, 50)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Pre-Christmas-Time
            if (i >= 335 & i<=356):
                rand_int = random.randint(30, 45)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Christmas (Holidays, DROP)
            if (i >= 357 & i<=361):
                rand_int = round(random.uniform(0, 5), 2)
                sinus_result = rand_int * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Every other day of  the year
            else:
                sinus_result = 10 * math.sin((i+80) * 8 * math.pi / 365) + 30
            # Try to insert the result into the db
            try: 
                table_name = str(input())
                insert_query = f"INSERT INTO {table_name} (column1, column2) Values ({i}, {sinus_result})"
                cursor.execute(insert_query)
                db_connection.commit()
            # Error handling
            except sqlite3.Error as error:
                print('Error while inserting to your sqlite database.', error)
        # Select statement to see the results
        select_query = 'SELECT * FROM Zahlen2021'
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