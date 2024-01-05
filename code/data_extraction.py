import pandas as pd
import tabula as tb

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
    
    def retrieve_pdf_data(self, link='https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'):
        '''
        Retrieves data from a pdf file to a pandas dataframe.
        '''
        all_data = tb.read_pdf(link, pages='all')
        return pd.concat(all_data)
    
    


#if __name__ == '__main__':
#    connection = dbu.DatabaseConnector()
#    users = extractor.read_rds_table(connection.engine, 'legacy_users')
#    extractor = DataExtractor()
#    print(users.info())
