#%%
import db_utils as dbu
import data_extraction as de
from data_extraction import DataExtractor
import pandas as pd
import matplotlib.pyplot as plt 


class DataCleaning():
    
    def make_categorical(self, df, columns):
        for column in columns:
            df[column] = df[column].astype('category') 

#TODO - this should take a longer list of formats (specificallty %B %Y %d, which occurs in 4 credic card data)
    def make_datetime(self, df, columns):
        if type(columns) == str:    
            columns = [columns]
        for column in columns:
            new_dt_1 = pd.to_datetime(df[column], format='ISO8601', errors='coerce')
            new_dt_2 = pd.to_datetime(df[column], format='%Y %B %d', errors='coerce')
            df[column] = new_dt_1.combine_first(new_dt_2)

    def drop_null_rows(self, df, columns):
        df.dropna(axis=0, subset=columns, inplace=True)

    def drop_null_column(self, df, columns):
        df.drop(columns=columns, inplace=True)

    def flag_null(self, df):
        for column in df.columns:
            df[column].loc[df[column] == 'NULL'] = pd.NaT   

    def flag_strange_values(self, df):
        for column in df.columns:
            if not column == 'index':
                idx_check = (df[column].str.len() == 10) & \
                        (df[column].str.isupper()) & \
                        (df[column].str.contains('-') == False)
                print(column)
                df[column][idx_check] = pd.NaT
    
    def convert_weights(self, df):
        ikg = df['weight'].str.contains('kg')
        df['weight'].loc[ikg] = df['weight'].loc[ikg].str.replace('kg', '')

        iml = df['weight'].str.contains('ml')
        df['weight'].loc[iml] = df['weight'].loc[iml].str.replace('ml', 'g') # replace with g asuming 1ml = 1g

        ig = df['weight'].str.contains('g')
        df['weight'].loc[ig] = df['weight'].loc[ig].str.replace('g', '')

        ioz = df['weight'].str.contains('oz')
        df['weight'].loc[ioz] = df['weight'].loc[ioz].str.replace('oz', '')

        imultiply = df['weight'].loc[df['weight'].str.contains(' x ')].index 
        for ix in imultiply:
            nums = df['weight'].iloc[ix].split(' x ')
            new_weight = float(nums[0]) * float(nums[1])
            df['weight'].iloc[ix] = str(new_weight / 1000)

        df['weight'] = df['weight'].astype('float64')
        df['weight'].loc[ig] = df['weight'].loc[ig] / 1000
        df['weight'].loc[ioz] = df['weight'].loc[ioz] / 35.274




def clean_user_data():

    #%%
    connection = dbu.DatabaseConnector()
    users = DataExtractor().read_rds_table(connection.engine, 'legacy_users')
    cleaner = DataCleaning()

    # %% [markdown]
    # First, flag NULL as missing values. Then, convert to NaT.
    #%%
    print(users.info())
    for column in users.columns:
        users[column].loc[users[column] == 'NULL'] = pd.NaT   
    print(users.info())

    #msno.matrix(users)

    # %% [markdown]
    # We see that several rows (21 total) are entirely missing, so we drop these.

    #%%
    cleaner.drop_null_rows(users, ['first_name'])

    print(users.info())

    # %% [markdown] Next we convert dates to datetime objects.
    # There are 25 dob and 23 join dates that cannot be converted. On inspection, these are clearly not dates and we drop these rows too.
    # %%
    dates = ['date_of_birth','join_date']
    cleaner.make_datetime(users, dates)

    print(users[['date_of_birth','join_date']].info())

    cleaner.drop_null_rows(users, ['date_of_birth','join_date'])    

    print(users.info())

    # %% [markdown] We also make a small change to correct country codes.
    users['country_code'].loc[users['country_code'] == 'GGB'] = 'GB'

    # %% [markdown] Finally, we check that all remaining rows have a user id of 36 length and are all lowercase
    correct_uid = (users['user_uuid'].str.len() == 36) & (users['user_uuid'].str.islower())
    print(users['user_uuid'].loc[~correct_uid.values])

    # %% [markdown] Categorical are converted for categorical columns.
    categoricals = ['country','country_code']
    cleaner.make_categorical(users, categoricals)

    # %% [markdown] We are left with 15266 rows
    users.info()

    return users

def clean_credit_card_data():

    extractor = de.DataExtractor()
    pdf_data = extractor.retrieve_pdf_data()
    cleaner = DataCleaning()

    # %%
    pdf_data.reset_index(inplace=True, drop=True)


    pdf_data['card_number'] = pdf_data['card_number'].astype('str')
    pdf_data['card_number'] = pdf_data['card_number'].str.replace('?', '')
    
    print(pdf_data.info())
    for column in pdf_data.columns:
        pdf_data[column].loc[pdf_data[column] == 'NULL'] = pd.NaT   
    print(pdf_data.info())

    # %%
    for column in pdf_data.columns:
        idx_check = (pdf_data[column].str.len() == 10) & \
                    (pdf_data[column].str.isupper())
        print(pdf_data[column][idx_check])
        pdf_data[column][idx_check] = pd.NaT

    cleaner.make_datetime(pdf_data, 'date_payment_confirmed')

    pdf_data.info()
    pdf_data.dropna(axis=0, subset=pdf_data.columns, inplace=True)
    pdf_data.info()

    return pdf_data

def clean_stores_data():
    extractor = de.DataExtractor()
    cleaner = DataCleaning()
    
    stores_data = extractor.retrieve_stores_data()

    stores_data.reset_index(inplace=True, drop=True)
    stores_data.info()

    #%%
    stores = stores_data.copy()
    stores.drop(columns=['lat'], inplace=True)
    stores.info()


    # %%
    cleaner.flag_null(stores)
    stores.info()

    #%%
    cleaner.flag_strange_values(stores)
    stores.info()

    #%%

    # %%
    cleaner.make_datetime(stores, 'opening_date')
    stores.info()

    # %%
    stores.dropna(axis=0, subset=['locality'], inplace=True)
    stores.info()

    #%%
    stores['staff_numbers'].loc[~stores['staff_numbers'].str.isdigit()] = pd.NaT

    return stores

def clean_product_data():
    extractor = DataExtractor()
    cleaner = DataCleaning()

    products_raw = extractor.extract_from_s3()

    #%%
    products = products_raw.copy()
    products.reset_index(inplace=True, drop=True)
    products.drop( columns='Unnamed: 0', inplace=True)

    # %%
    cleaner.flag_null(products)
    #%%
    cleaner.flag_strange_values(products)

    # %%
    cleaner.make_datetime(products, 'date_added')

    # %%
    products.dropna(axis=0, subset=['product_name'], inplace=True)
    products.reset_index(inplace=True, drop=True)

    # %%
    products['product_price'] = products['product_price'].str.replace('£', '')
    products['product_price'] = products['product_price'].astype('float64')
    products.rename(columns={'product_price':'price_gbp'}, inplace=True)

    # %%
    SA = products['removed']=='Still_avaliable'
    products['removed'].loc[~SA] = False
    products['removed'].loc[SA] = True
    products.rename(columns={'removed':'still_available'}, inplace=True)
    # %%
    products['weight'].iloc[1772] = '77g' # manually reformat one edge case
    cleaner.convert_weights(products)
    products.rename(columns={'weight':'weight_kg', 'EAN': 'ean'}, inplace=True)


    return products

def clean_order_data():
    extractor = DataExtractor()
    connection = dbu.DatabaseConnector()
    cleaner = DataCleaning()

    #%%
    connection.list_db_tables()
    # %%
    orders_raw = extractor.read_rds_table(connection.engine, 'orders_table')
    orders = orders_raw.copy()

    # %%
    orders.drop(columns=['level_0', 'first_name', 'last_name', '1'], inplace=True)
    orders.reset_index(inplace=True, drop=True)

    # %%
    cleaner.flag_null(orders)

    return orders

def clean_dates():
    #%%
    connection = dbu.DatabaseConnector()
    extractor = DataExtractor()
    cleaner = DataCleaning()

    # %%
    dates_raw = extractor.extract_from_s3(key='date_details.json')
    dates = dates_raw.copy()

    # %%
    cleaner.flag_null(dates)

    #%%
    cleaner.flag_strange_values(dates)
    # %%
    dates.dropna(axis=0, subset=dates.columns, inplace=True)
    dates.reset_index(inplace=True, drop=True)
    
    return dates

if __name__ == '__main__':
    #users = clean_user_data()
    #credit_card = clean_credit_card_data()

    connection = dbu.DatabaseConnector('local_credentials')
    print(connection.list_db_tables())

    #connection.upload_table(users, 'dim_users')
    
    cards = clean_credit_card_data()
    connection.upload_table(cards, 'dim_card_details')

    #stores = clean_stores_data()
   # print(stores.info())
    #connection.upload_table(stores, 'dim_store_details')

    #products = clean_product_data()
   # print(products.info())
    #connection.upload_table(products, 'dim_products')

    #orders = clean_order_data()
    #print(orders.info())
    #connection.upload_table(orders, 'orders_table')

    #dates = clean_dates()
    #print(dates.info())
    #connection.upload_table(dates, 'dim_date_times')

# %%
