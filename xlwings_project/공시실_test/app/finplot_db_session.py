import config

import pymysql

import pandas as pd

class mysql_session:
    def __init__(self):
        self.connection = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                                    user=config.DATABASE_CONFIG['user'],
                                    password=config.DATABASE_CONFIG['password'],
                                    database=config.DATABASE_CONFIG['dbname'],
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def select_all_from_finplot(self):
        self.cursor.execute("select * from finplot_tb;")
        rows = self.cursor.fetchall()
        return rows

    def get_header_list(self):
        self.cursor.execute("select * from finplot_tb limit 1;")
        rows = self.cursor.fetchall()
        finplot_data_columns = pd.DataFrame(rows).columns
        header_list = list()
        for column_name in finplot_data_columns:
            temp_dict = dict()
            temp_dict['title'] = column_name
            temp_dict['field'] = column_name
            header_list.append(temp_dict)
        return header_list

    def alter_table_add_column(self,column_name):
        self.cursor.execute(f"alter table `finplot_tb` add column `{column_name}` varchar(16);")
        self.connection.commit()

    def alter_table_drop_column(self,column_name):
        self.cursor.execute(f"alter table `finplot_tb` drop column `{column_name}`'")
        self.connection.commit()

    def insert_into_table_value(self,row_form):
        sql = f"insert into `finplot_tb` (`Date`,`Open`,`High`,`Low`,`Close`,`Volume`,`CHANGE`) value ('{row_form.date}',{row_form.open},{row_form.high},{row_form.low},{row_form.close},{row_form.volume},{row_form.change});"
        self.cursor.execute(sql)
        

    def db_close(self):
        self.connection.close()