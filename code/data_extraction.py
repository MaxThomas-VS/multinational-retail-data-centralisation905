import pandas as pd
import db_utils as dbu

class DataExtractor():
    
    def print_table_names(self, engine):
        '''
        Prints all tables in the database.
        '''
        print(engine.tables)

    def read_rds_table(self, engine, table_name):
        '''
        Reads a table from the database.
        '''
        return pd.read_sql_table(table_name, engine)
    


if __name__ == '__main__':
    connection = dbu.DatabaseConnector()
    extractor = DataExtractor()
    users = extractor.read_rds_table(connection.engine, 'legacy_users')
    print(users.info())
