#%%
from data_extraction import DataExtractor
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt 


class DataCleaning():
    
    def make_categorical(self, df, columns):
        for column in columns:
            df[column] = df[column].astype('category') 

    def make_datetime(self, df, columns):
        for column in columns:
            new_dt_1 = pd.to_datetime(df[column], format='ISO8601', errors='coerce')
            new_dt_2 = pd.to_datetime(df[column], format='%Y %B %d', errors='coerce')
            df[column] = new_dt_1.combine_first(new_dt_2)

    def drop_null_rows(self, df, columns):
        df.dropna(axis=0, subset=columns, inplace=True)



            
   


#if __name__ == '__main__':
#%%
users = DataExtractor().read_table('legacy_users')
cleaner = DataCleaning()

# %% [markdown]
# First, flag NULL as missing values. Then, convert to NaT.
#%%
print(users.info())
for column in users.columns:
    users[column].loc[users[column] == 'NULL'] = pd.NaT   
print(users.info())

msno.matrix(users)

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

# %%
