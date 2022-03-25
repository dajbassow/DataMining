import sqlite3
import math
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

    return cursor, sqliteConnection

# Close db connection
def close_db_connection(cursor, db_connection):
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
    for i in range(0, years):
        table_name = get_table_name()
        rand_increas_number = round(random.uniform(0.1, 0.5), 2)
        try:
            drop_table = f'DROP TABLE IF EXISTS {table_name};'
            cursor.execute(drop_table)
            create_table = f'CREATE TABLE {table_name} (day int, sales decimal);'
            cursor.execute(create_table)
        except sqlite3.Error as error:
                print('Error while creating your tables.', error)
        # Generate data for a year in a loop
        for i in range(1, 366):
            # Valentines day
            if 38 <= i <= 42:
                rand_num = random.randint(100, 120)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + 200
            # summer sale
            elif 182 <= i <= 235:
                rand_num = random.randint(80, 85)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + 50
            # Black Friday
            elif 300 <= i <= 307:
                rand_num = random.randint(100, 120)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + 50
            # christmas
            elif 335 <= i <= 356:
                rand_num = random.randint(80, 90)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + 50
            # end of the year
            elif 357 <= i <= 365:
                rand_num = round(random.uniform(0, 5), 2)
                sinus_result = 0.1 * i + rand_num * math.sin((i + 80) * 16 * math.pi / 365) + 50          
            else:
                sinus_result = 0.1 * i + 50 * math.sin((i + 80) * 16 * math.pi / 365) + 50
            
            # Try to insert the result into the db
            try:
                insert_query = f'INSERT INTO {table_name} (day, sales) Values ({i}, {round(sinus_result, 2)});'
                cursor.execute(insert_query)
                db_connection.commit()
            # Error handling
            except sqlite3.Error as error:
                print('Error while inserting to your sqlite database.', error)
        
        record = fetch_last_sale(cursor, table_name)
        new_years_sale_number = int(record[0][1])


# SELECT QUERY
def fetch_data(cursor):
    table_name = get_table_name()
    select_query = f'SELECT * FROM {table_name}'
    cursor.execute(select_query)
    record = cursor.fetchall()
    print(record)
    print(record[1][1])
    return record

def fetch_last_sale(cursor, table_name):
    select_query = f'SELECT * FROM {table_name} WHERE day=365;'
    cursor.execute(select_query)
    record = cursor.fetchall()
    print(record)
    return record

def plot_single_data(cursor, sqliteConnection):
    table_name = get_table_name()
    sqlite_select_query = f'SELECT day FROM {table_name}'
    cursor.execute(sqlite_select_query)
    recordX = cursor.fetchall()
    sqlite_select_query = f'SELECT sales FROM {table_name}'
    cursor.execute(sqlite_select_query)
    recordY = cursor.fetchall()

    plt.plot(recordX, recordY)
    plt.show()

# plot all 3 tables
def plot_all_tables(cursor, sqliteConnection):
    print("Plot data from sales 2019-2021...")

    select_query = 'SELECT day FROM verkauf2019;'
    cursor.execute(select_query)
    sales19_x = cursor.fetchall()
    select_query = 'SELECT sales FROM verkauf2019;'
    cursor.execute(select_query)
    sales19_y = cursor.fetchall()

    select_query = 'SELECT day FROM verkauf2020;'
    cursor.execute(select_query)
    sales20_x = cursor.fetchall()
    select_query = 'SELECT sales FROM verkauf2020;'
    cursor.execute(select_query)
    sales20_y = cursor.fetchall()

    select_query = 'SELECT day FROM verkauf2021;'
    cursor.execute(select_query)
    sales21_x = cursor.fetchall()
    select_query = 'SELECT sales FROM verkauf2021;'
    cursor.execute(select_query)
    sales21_y = cursor.fetchall()

    plt.plot(sales19_x, sales19_y, label='sales2019')
    plt.plot(sales20_x, sales20_y, label='sales2020')
    plt.plot(sales21_x, sales21_y, label='sales2021')
    plt.xlabel('day')
    plt.ylabel('sales')
    plt.title('Sales from 2019 - 2021')
    plt.legend()
    plt.show()

# plots a sales table and their mean
def plot_table_mean(cursor, sqliteConnection, table_name):
    select_query = f'Select day from {table_name};'
    cursor.execute(select_query)
    sales_x = cursor.fetchall()
    select_query = f'Select sales from {table_name};'
    cursor.execute(select_query)
    sales_y = cursor.fetchall()
    sales_x_array = np.array(sales_x)
    mean = get_mean(sqliteConnection, table_name)
    std = get_standard_deviation(sqliteConnection, table_name)

    plt.plot(sales_x, sales_y, label=f'{table_name}')
    plt.plot(sales_x, sales_x_array * 0.1 + 75, label='linear gradient')
    plt.axhline(mean, label='mean', color='r')
    plt.axhline(std + mean, label='standard deviation', color='g')
    plt.axhline(mean - std, color='g')
    plt.xlabel('day')
    plt.ylabel('sales')
    plt.title('Sales from 2020 with mean and standard deviation')
    plt.legend()
    plt.show()

# get mean from sales table
def get_mean(sqliteConnection, table_name):
    data = pd.read_sql(f"Select sales From {table_name}", con=sqliteConnection)
    mean = data["sales"].mean()
    print("mean: ", mean)
    return mean

# calculate standard deviation
def get_standard_deviation (sqliteConnection, table_name):
    data = pd.read_sql(f"Select sales From {table_name}", con=sqliteConnection)
    st = data["sales"].std()
    print("standard deviation: ", st)
    return st

# find sth unusual
def get_peaks(sqlliteConnection, cursor):
    print("looking for peaks in ... ")
    table_name = get_table_name()
    mean = get_mean(sqliteConnection, table_name)
    std = get_standard_deviation(sqliteConnection, table_name)
    sales_record = fetch_data(cursor, table_name)
    print("mean + std: ", mean+std)
    print("mean - std: ", mean-std)
    upper_limit = mean + std
    lower_limit = mean - std

    for data in sales_record:
        if data[1] > upper_limit or data[1] < lower_limit:
            print("Peak found at day: ", data[0], " with a sale number of: ", data[1])


cursor, sqliteConnection = get_db_connection()
fetch_data(cursor, "Verkauf2020")
# get_peaks(sqliteConnection, cursor)
# generate_data(cursor, sqliteConnection)
# table_name = get_table_name()
# record = fetch_data(cursor, sqliteConnection, table_name)
# plot_single_table(cursor, sqliteConnection)
# plot_all_tables(cursor, sqliteConnection)
# get_mean(sqliteConnection, 'verkauf2020')
# get_standard_deviation(sqliteConnection, "verkauf2020")
plot_table_mean(cursor, sqliteConnection, 'verkauf2020')
close_db_connection(cursor, sqliteConnection)
