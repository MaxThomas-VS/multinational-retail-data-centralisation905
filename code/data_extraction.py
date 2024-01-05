import yaml
import sqlalchemy as sqla
from sqlalchemy import inspect

class DataExtractor():
    
    def __init__(self, filename='../setup/db_credentials.yaml'):
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
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def print_table_names(self):
        '''
        Prints all tables in the database.
        '''
        print(self.tables)
    


if __name__ == '__main__':
    data_extractor = DataExtractor()
    data_extractor.print_table_names()
