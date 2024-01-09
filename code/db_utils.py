import pandas as pd
import yaml
import sqlalchemy as sqla

#import data_cleaning as dcn


class DatabaseConnector():
    def __init__(self, credentials='db_credentials'):
        try:
            filename = '../setup/' + credentials + '.yaml'
        except:
            filename = 'setup/' + credentials + '.yaml'
        self.credentials = self.read_credentials(filename)
        self.engine = self.start_sqla_engine()
        self.tables = self.list_db_tables()
        
    
    def read_credentials(self, filename):
        with open(filename, 'r') as fn:
            yaml_as_dict = yaml.safe_load(fn)
        return yaml_as_dict
    
    def start_sqla_engine(self):
        '''
        Creates engine to connect to RDS.
        '''
        url = sqla.engine.url.URL.create(**self.credentials) # converts credentials into url
        return sqla.create_engine(url)
    
    def list_db_tables(self):
        '''
        Lists all tables in the database.
        '''
        inspector = sqla.inspect(self.engine)
        return inspector.get_table_names()
    
    def upload_table(self, df, table_name):
        '''
        Uploads a table to the database.
        '''
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)

if __name__ == '__main__':
    pass
    #connection = DatabaseConnector('local_credentials')
    #print(connection.list_db_tables())

    #users = dcn.clean_user_data()
    #connection.upload_table(users, 'dim_users')



