import cr_db_quarry as quarry

# Default db path and Table Values
# User can change the values of these variable explicitly
db_path = 'cr_meeting_db.sqlite'
main_table_name = 'meeting_info'
__columns_to_print = ['Meeting_id','Cr_num','Date','Start_time','End_time','Users','Transcript','Word_cloud_link','Frequent_words']

def meeting_related_info_search():
    print ("Enter Below information to get meeting related information..")
    search_options_names = ['from date','to date','start time','end time','User names', 'Conference room Number', 'Topics discussed']
    for x in search_options_names:
        print (x)
    print ("\n\n")

    from_date = raw_input('From Date (in YYYY-MM-DD format):')
    to_date = raw_input('To Date (in YYYY-MM-DD format):')
    start_time = raw_input('Meetings starting time Lower limit(in HH:MM:SS format):')
    end_time = raw_input('Meeting starting time Upper Limit (in HH:MM:SS format):')
    user_name = list(raw_input('User Names (Separated by comma):').split(','))
    cr_num = list(raw_input('Conference Room Numbers (Separated by comma):').split(','))
    topics = list(raw_input('Topics discussed in meeting (Separated by coma):').split(','))
    #meeting_transcript = raw_input('Meeting Transcript Needed? (Yes/No) (Default option is No):')
    #word_cloud = raw_input('Want to see the word cloud? (Yes/no) (Default option is No):')

    output_list = quarry.quarry_search(db_path, main_table_name,from_date, to_date, start_time, end_time,user_name,cr_num,topics)
    #print (output_list)
    print ("|{:_<15} | {:_<10} | {:_<12} | {:_<12} | {:_<10} | {:_<50} | {:_<60} | {:_<60} | {:_<100}|".format('','','','','','','','','',''))

    print ("|{:^15} | {:^10} | {:^12} | {:^12} | {:^10} | {:^50} | {:^60} | {:^60} | {:^100}|".format(__columns_to_print[0],__columns_to_print[1],__columns_to_print[2], __columns_to_print[3],__columns_to_print[4], __columns_to_print[5], __columns_to_print[6], __columns_to_print[7], __columns_to_print[8]))
    for x in output_list:
        print ("|{:_<15} | {:_<10} | {:_<12} | {:_<12} | {:_<10} | {:_<50} | {:_<60} | {:_<60} | {:_<100}|".format('', '', '','', '', '','', '', ''))

        print ("|{:^15} | {:^10} | {:^12} | {:^12} | {:^10} | {:^50} | {:^60} | {:^60} | {:^100}|".format(x[0], x[1], x[2], x[3], x[4],x[5],x[6],x[7],x[8]))
    print ("|{:_<15} | {:_<10} | {:_<12} | {:_<12} | {:_<10} | {:_<50} | {:_<60} | {:_<60} | {:_<100}|".format('', '', '', '','', '', '', '',''))



#def transcripts_related_info_search():
