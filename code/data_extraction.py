import pandas as pd
import tabula as tb
import requests
import boto3
import io

class DataExtractor():

    def __init__(self):
        self.api_key = self.make_api_header()
    
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
    
    def make_api_header(self, api_key='yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'):
        return {'x-api-key': api_key}
    
    def list_number_of_stores(self, link='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'):
        response = requests.get(link, headers=self.api_key)
        if response.status_code == 200:
            data = response.json()
            return data['number_stores']
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response Text: {response.text}")
            return None
        
    def retrieve_stores_data(self, link='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'):
        n_stores = self.list_number_of_stores()
        stores_data = None
        for i_store in range(n_stores):
            response = requests.get(link + str(i_store), headers=self.api_key)
            if response.status_code == 200:
                new_data = pd.json_normalize(response.json())
                stores_data = pd.concat([stores_data, new_data])
            else:
                print(f"In retrieve_stores_data, iteration {str(i_store)}:")
                print(f"Request failed with status code: {response.status_code}")
                print(f"Response Text: {response.text}")
        return stores_data
    
    def extract_from_s3(self, bucket='data-handling-public', key='products.csv'):
        s3 = boto3.client('s3')
        s3_obj = s3.get_object(Bucket=bucket, Key=key)
        if key.endswith('.csv'):
            return pd.read_csv(s3_obj['Body'])
        elif key.endswith('.json'):
            stream_data = io.BytesIO(s3_obj['Body'].read())
            return pd.read_json(stream_data)
    


    
    


#if __name__ == '__main__':
 #   connection = dbu.DatabaseConnector()
#    users = extractor.read_rds_table(connection.engine, 'legacy_users')
###   extractor = DataExtractor()
#    print(users.info())
