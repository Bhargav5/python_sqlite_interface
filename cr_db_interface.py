'''
Module Name: cr_db_interface
Basic Purpose: To create basic interface functions for conference room database in sqlite3
Owner : Bhargav Upadhyay
Started: 20th septmber, 2016
Basic functions: Create new table, create new virtual table using fts4, add new column, add new raw
Version: 1.0
'''
import sqlite3
# Function to create new table for a db. It also sets given fields as primary key
def create_table(db_path,table_name,column_name, field_type, primary_key,is_primary_key=False):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    l1 = ["{} {}".format(x, y) for x, y in zip(column_name, field_type)]
    if (is_primary_key == False):
        str1 = "CREATE TABLE {tn}({str_c})".format(tn=table_name,str_c = __preparestring(l1))
        cursor.execute(str1)
    else:
        str1 = "CREATE TABLE {tn}({str_c}, PRIMARY KEY({prk}))".format(tn= table_name,str_c=__preparestring(l1),prk=__preparestring(primary_key))
        cursor.execute(str1)

    connection.commit()
    connection.close()
# To create new virtual Table without attaching it to real table.
def create_virtual_table(db_path, table_name, column_name):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    str1 = "CREATE VIRTUAL TABLE {tn} USING fts4({str_c})".format(tn=table_name, str_c=__preparestring(column_name))
    cursor.execute(str1)

    connection.commit()
    connection.close()

# To delete a table.
def delete_table(db_path,table_name):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE  {tn}".format(tn=table_name))

    connection.commit()
    connection.close()
# To insert a new column in a table. User can also assign default value to new column
def insert_column(db_path,table_name, column_name, field_type, default_value=None):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ft} DEFAULT '{df}'".format(tn=table_name, cn= column_name, ft= field_type, df=default_value))

    connection.commit()
    connection.close()
# To convert list in to string seperated by semi colon, a private function to module
def __preparestring(l1):
    str1 = str(l1[0])
    if (len(l1) == 1):
        return str1
    else:
        for i in range(1,len(l1)):
            str1 = str1 + ','+ str(l1[i])
    return str1

# To insert new raw in to table
def insert_raw(db_path, table_name, parameters, values):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    str_par = __preparestring(parameters)
    str1 = "INSERT INTO {tn}({str_p}) VALUES {str_v}".format(tn=table_name, str_p = str_par, str_v = tuple(values))

    cursor.execute(str1)
    connection.commit()
    connection.close()


