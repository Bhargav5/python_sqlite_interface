import cr_db_interface as interface
import time
import sqlite3
import os
from wordcloud import WordCloud  # To draw word cloud
import matplotlib.pyplot as plt  # For creating image used by wordcloud module
from sklearn.feature_extraction.text import CountVectorizer #To create frequently used words
import numpy as np


# Information fields used for CR
__column_name_main_table = ['Meeting_id','Cr_num','Date','Start_time','End_time','Users','Transcript','Word_cloud_link','Frequent_words']
__column_name_virtual_table=['Meeting_id','Cr_num','Date','Time']
__virtual_table_default_columns = len(__column_name_virtual_table)
__field_types = ['TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT']

# Default db path and Table
# User can change the values of these variable explicitly
db_path = 'cr_meeting_db.sqlite'
main_table_name = 'meeting_info'


## Create New Table
def create_new_table():
    interface.create_table(db_path, main_table_name, __column_name_main_table,__field_types,['Meeting_id'], True)

## Generate Meeting id based on the meeting information
# The format is YYMMDDHHMMCr#
def __generate_meeting_id(Cr_number):
    localtime = time.localtime(time.time())
    yy = str (localtime[0]%100)
    mm = "{:02d}".format(localtime[1])
    dd = "{:02d}".format(localtime[2])
    hh = "{:02d}".format(localtime[3])
    mm1 = "{:02}".format(localtime[4])
    return (mm+dd+yy+hh+mm1+Cr_number)

# Function to create new meeting
def new_meeting(Cr_number, User_names):
    # Every New Meeting has 2 tasks: 1. Create a new entry in main table and 2. Create a virtual table
    # 1. Creating new entry in main table

    localtime = time.localtime(time.time())

    date_ip = str (localtime[0]) + '-' + "{:02d}".format(localtime[1]) + '-' + "{:02d}".format(localtime[2])
    strart_time_ip = "{:02d}".format(localtime[3])+ ':' + "{:02d}".format(localtime[4]) + ':' + "{:02d}".format(localtime[5])

    meeting_id = __generate_meeting_id(Cr_number)

    user_str = str (User_names[0])

    for i in range(1,len((User_names))):
        user_str = user_str + ' ' + User_names[i]

    ip_values = [meeting_id, Cr_number, date_ip, strart_time_ip, 'None', user_str, 'None', 'None', 'None']
    interface.insert_raw(db_path,main_table_name,__column_name_main_table, ip_values)

    # 2. Create a new virtual table to store speech of each user

    __virtual_table_name = 'Table_' + meeting_id

    interface.create_virtual_table(db_path,__virtual_table_name,__column_name_virtual_table + User_names)

    return meeting_id

def store_speech_data(meeting_id, user_names, cr_num, ip_strings):


    localtime = time.localtime(time.time())
    current_date = str (localtime[0]) + '-' + "{:02d}".format(localtime[1]) + '-' + "{:02d}".format(localtime[2])
    current_time = "{:02d}".format(localtime[3])+ ':' + "{:02d}".format(localtime[4]) + ':' + "{:02d}".format(localtime[5])

    input_list = [meeting_id,cr_num, current_date, current_time] + ip_strings

    __virtual_table_name = 'Table_' + meeting_id

    #print (input_list)
    #print (__column_name_virtual_table + user_names)

    interface.insert_raw(db_path, __virtual_table_name, parameters= (__column_name_virtual_table + user_names), values= input_list)


def __create_transcript(meeting_id, user_names):

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    table_name = 'Table_' + meeting_id
    cursor.execute("SELECT * FROM {tn}".format(tn = table_name))
    table_data = cursor.fetchall()
    transcript = []

    for x in table_data:

        lt_temp = ["{}:{}".format(x1,y1) for x1,y1 in zip(user_names,x[len(__column_name_virtual_table):])]
        lt_temp1 = ["Time = {}".format(x[len(__column_name_virtual_table) -1])] + lt_temp
        #transcript.append(["Time = {}".format(x[len(__column_name_virtual_table) -1]), lt_temp])
        transcript.append(lt_temp1)

    connection.close()
    file_obj = open('{}.txt'.format(meeting_id),'w+')

    for x in transcript:
        for y in x:
            file_obj.write("{}\n".format(y))
        file_obj.write("\n")
    file_obj.close()
    file_path = os.getcwd() + '\\' + '{}.txt'.format(meeting_id)
    return file_path

def __create_word_cloud(meeting_id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    table_name = 'Table_' + meeting_id
    cursor.execute("SELECT * FROM {tn}".format(tn=table_name))
    table_data = cursor.fetchall()
    input_str1 = ""

    for raw in table_data:
        for statements in raw[len(__column_name_virtual_table):]:
            if (statements != '' or statements != None):
                input_str1 = input_str1 + ' '+statements
    #print (input_str1)
    wc =  WordCloud(max_font_size=40, relative_scaling=.5).generate(input_str1)

    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    #plt.show()
    plt.savefig('{}.png'.format(meeting_id))
    connection.close()
    image_path = os.getcwd() + '\\' + '{}.png'.format(meeting_id)
    return (image_path)

def __create_freq_words(meeting_id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    table_name = 'Table_' + meeting_id
    cursor.execute("SELECT * FROM {tn}".format(tn=table_name))
    table_data = cursor.fetchall()
    input_str1 = ""

    for raw in table_data:
        for statements in raw[len(__column_name_virtual_table):]:
            if (statements != '' or statements != None):
                input_str1 = input_str1 + ' ' + statements

    cv = CountVectorizer(min_df=0,stop_words="english", max_features=200)
    counts = cv.fit_transform([input_str1]).toarray().ravel()
    words = np.array(cv.get_feature_names())

    op_str = words[0]
    if (len(words) > 1):
        for i in range(1,len(words)):
            op_str = op_str + ',' + words[i]

    #print (op_str)
    return op_str



def end_meeting(meeting_id, user_names):
    ''' At the end of the meeting there are 4 tasks.
    1. Set the End_time
    2. Create transcript and update Transcript column
    3. Create Word cloud picture and put it's link
    4. Find most frequently used words and update Frequent_words
    '''

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    localtime = time.localtime(time.time())
    current_time = "{:02d}".format(localtime[3]) + ':' + "{:02d}".format(localtime[4]) + ':' + "{:02d}".format(localtime[5])
    transcript = __create_transcript(meeting_id, user_names)

    word_cloud = __create_word_cloud(meeting_id)

    freq_words =  __create_freq_words(meeting_id)

    cursor.execute("UPDATE {tn} SET End_time = '{c_time}', Transcript = '{tsc}', Word_cloud_link='{wc}',Frequent_words = '{freq_wd}'  WHERE Meeting_id = '{m_id}'".format(tn = main_table_name, c_time = current_time, m_id = meeting_id, tsc = transcript, freq_wd= freq_words, wc = word_cloud))

    connection.commit()
    connection.close()
