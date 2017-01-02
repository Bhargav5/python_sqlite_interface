import sqlite3
date_column = 2
time_column = 3

def __printlist(lt1):
    for x in lt1:
        print (x)

def __preparestr(lt1):
    str1 = lt1[0]
    if (len(lt1) == 1):
        return str1
    else:
        for i in range(1,len(lt1)):
            str1 = str1 + '|' + lt1[i]
    return str1


def __prepare_user_string(lt1):
    temp_string = "{{col_user}} LIKE '%{}%'"
    str3 = temp_string.format(lt1[0])
    if (len(lt1) == 1):
        return str3
    else:
        for i in range(len(lt1)):
            xy = temp_string.format(lt1[i])
            str3 = str3 + ' OR ' + xy + ' '
    return str3

def __prepare_conf_room_string(lt1):
    temp_string = "{{col_conf}} LIKE '%{}%'"
    str3 = temp_string.format(lt1[0])
    if (len(lt1) == 1):
        return str3
    else:
        for i in range(len(lt1)):
            xy = temp_string.format(lt1[i])
            str3 = str3 + ' OR ' + xy + ' '
    return str3

def __prepare_topics_string(lt1):
    temp_string = "{{col_topics}} LIKE '%{}%'"
    str3 = temp_string.format(lt1[0])
    if (len(lt1) == 1):
        return str3
    else:
        for i in range(len(lt1)):
            xy = temp_string.format(lt1[i])
            str3 = str3 + ' OR ' + xy + ' '
    return str3




def quarry_search(db_path,table_name,from_date=None, to_date=None, start_time=None, end_time = None, user_name =1, cr_num = 1, topics = 1):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {tn}".format(tn = table_name))
    whole_table = cursor.fetchall()

    #Basic initialization
    if (from_date == None or from_date == ''):
        from_date = whole_table[0][date_column]
        print (from_date)
    if (to_date == None or to_date == ''):
        to_date = whole_table[len(whole_table)-1][date_column]
        print (to_date)
    if (start_time == None or start_time == ''):
        start_time = '00:00:00'
    if (end_time == None or end_time == ''):
        end_time = '23:59:59'
    if (user_name != 1 and user_name != ''):
        user_name = __prepare_user_string(user_name).format(col_user = 'Users')
    elif(user_name == ''):
        user_name = 1
    if (cr_num != 1 and cr_num != ''):
        cr_num = __prepare_conf_room_string(cr_num).format(col_conf = 'Cr_num')
    elif(cr_num == ''):
        cr_num = 1
    if (topics != 1 and topics != ''):

        topics = __prepare_topics_string(topics).format(col_topics = 'Frequent_words')
    elif (topics == ''):
        topics = 1

    str_input = "SELECT * FROM {tn} WHERE ({d_col} BETWEEN '{f_date}' AND '{e_date}') AND ({t_col} BETWEEN '{s_time}' AND '{e_time}') AND ({user_st}) AND ({cr_st}) AND ({topic_st})"\
        .format(tn = table_name, user_st = user_name, cr_st = cr_num, topic_st = topics,d_col='Date',f_date = from_date, e_date = to_date,t_col='Start_time',s_time = start_time,e_time=end_time )
    cursor.execute(str_input)
    lt_op = cursor.fetchall()
    #__printlist(lt_op)
    return (lt_op)


    connection.commit()
    connection.close()

def __prepare_user_name_string(lt1):
    str1 =  lt1[0]
    if (len(lt1) == 1):
        return  str1
    else:
        for i in range(1,len(lt1)):
            str1 = str1 + ',' + lt1[i]
    return str1

def virtual_table_quarry_search(db_path, table_name, meeting_id, users):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    #user_string = __prepare_user_name_string(users)

    str_input = "SELECT {str_user} FROM {tn} WHERE {m_id_col} = '{m_id}'".format(tn = table_name, m_id = meeting_id, m_id_col = 'Meeting_id',str_user = __prepare_user_name_string(users))
    cursor.execute(str_input)
    lt_op = cursor.fetchall()
    __printlist(lt_op)

    connection.commit()
    connection.close()

