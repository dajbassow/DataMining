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
    print('Enter your desired years as an int: ')
    years = int(input())
    new_years_sale_number = 0
    for i in range(1, years):
        table_name = get_table_name()
        # Generate data for a year in a loop
        for i in range(1, 365):
            # Valentines day
            if 38 <= i <= 42:
                rand_num = random.randint(100, 120)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + new_years_sale_number + 200
            # summer sale
            elif 182 <= i <= 235:
                rand_num = random.randint(80, 85)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + new_years_sale_number + 50
            # Black Friday
            elif 300 <= i <= 307:
                rand_num = random.randint(100, 120)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + new_years_sale_number + 50
            # christmas
            elif 335 <= i <= 356:
                rand_num = random.randint(80, 90)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + new_years_sale_number + 50
            # end of the year
            elif 357 <= i <= 365:
                rand_num = round(random.uniform(0, 5), 2)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + new_years_sale_number + 50
                new_years_sale_number = int(sinus_result)           
            else:
                sinus_result = 0.1 * i + 50 * math.sin((i + 80) * 16 * math.pi / 365) + new_years_sale_number + 50
            
            # Try to insert the result into the db
            try:
                create_table = f'CREATE TABLE {table_name} (day int, sales decimal);'
                #insert_query = f'INSERT INTO {table_name} (day, sales) Values ({i}, {round(sinus_result, 2)});'
                #update_statement = f'UPDATE {table_name} SET sales = {round(sinus_result, 2)} WHERE day = {i}'
                cursor.execute(create_table)
                #cursor.execute(insert_query)
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
