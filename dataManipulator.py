import sqlite3

# try: 
#     dbConnection = sqlite3.connect('Verkaufsdaten.db')
#     cursor = dbConnection.cursor()

#     sql_select = 'SELECT * FROM Zahlen2021;'
#     cursor.execute(sql_select)
#     record = cursor.fetchall()
#     print('My data: ', record)
#     cursor.close()

# except sqlite3.Error as error:
#     print('Error while connecting to your sqlite database.', error)
# finally:
#     if dbConnection:
#         dbConnection.close()
#         print('The connection to your database was closed.')


def add_data():
    try: 
        db_connection = sqlite3.connect('Verkaufsdaten.db')
        cursor = db_connection.cursor()

        # Sin Formel einfügen mit Trend 
        # Für jeden neuen Datensatz ein INSERT ausfühern
        # for start ...
        for i in range(1, 365):
           #assd 
       
        # for end
    except sqlite3.Error as error:
        print('Error while connecting to your sqlite database.', error)
    finally:
        if db_connection:
            db_connection.close()
            print('The connection to your database was closed.')
