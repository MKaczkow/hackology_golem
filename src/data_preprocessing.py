import pandas as pd
import numpy as np
import swifter
from sklearn.preprocessing import LabelEncoder
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler


COVARIATE_COLUMNS = ["dept_id", "cat_id", "store_id", "state_id"]
DATE_COLUMN = 'date'

def load_pivoted_dataframes(sales_df):
    sales_df_melted = pd.melt(sales_df, id_vars=["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"], var_name="d", value_name="sales_qty")

    for column in COVARIATE_COLUMNS:
        sales_df_melted[column] = sales_df_melted[column].astype('category')
    # sales_train_val_melted['item_id'] = sales_train_val_melted['item_id'].astype('category')

    grouped_sales = {}
    for column in COVARIATE_COLUMNS:
        grouped_sales[column] = sales_df_melted.groupby(['d', column])['sales_qty'].sum().reset_index()
    # df_item = sales_train_val_melted.groupby(['d','item_id'])['sales_qty'].sum().reset_index()
    pivoted_sales = {}
    for column in COVARIATE_COLUMNS:
        curr_df = grouped_sales[column]
        pivoted_sales[column] = curr_df.pivot(index='d', columns=column, values='sales_qty').reset_index()
    return pivoted_sales


def preprocess_missing_data(selling_df):
    selling_df['sell_price'] = selling_df.groupby(['store_id', 'item_id'])['sell_price'].transform(lambda x: x.fillna(x.mean()))
    # create id from item_id and store_id & add sell price tag
    selling_df['id'] = selling_df['item_id'] +'_' + selling_df['store_id'] + '_Sell_Price'
    selling_df = selling_df.pivot(index='wm_yr_wk', columns='id', values='sell_price').reset_index()

    ########## check if fill na with 0 makes sense ###### 
    selling_df = selling_df.fillna(method='bfill')

    tot_sell_price = selling_df.drop(columns=['wm_yr_wk']).sum(axis=1).copy()
    selling_df['Total_Sell_Price'] = tot_sell_price
    selling_df = selling_df[['wm_yr_wk','Total_Sell_Price']]
    return selling_df

def prepare_df_with_covariates(sales_train_val, selling_prices, set_name, calendar, pivoted_dfs):
    # Transpose the df
    sales_train_val_transposed = sales_train_val.T.reset_index()
    # Exclude rows 1 to 5 that contain item_id, dept_id,cat_id,store_id,state_id
    # Use np.r_ from NumPy to concatenate index positions, and then use iloc for selection
    sales_train_val_transposed =\
        sales_train_val_transposed.iloc[np.r_[0, 6:len(sales_train_val_transposed)]].reset_index(drop=True) 

    # Assign the 1st row as column names
    col_names = sales_train_val_transposed.iloc[0]
    sales_train_val_transposed = sales_train_val_transposed.iloc[1:].reset_index(drop=True)
    sales_train_val_transposed.columns = col_names

    # Rename 'id' to 'd' as per calendar df
    sales_train_val_transposed.rename( columns={'id':'d'}, inplace=True) 

    # Merge with calendar df (date_column)
    sales_train_val_transposed1 = sales_train_val_transposed.merge(calendar, on=['d'], how='left')

    # Merge with Selling Prices df (sell_price_columns)
    sales_train_val_transposed1 = sales_train_val_transposed1.merge(selling_prices, on=['wm_yr_wk'], how='left')
    
    # Merge with dept, cat, store, state df (non_sales_columns)
    
    for column in COVARIATE_COLUMNS:
        sales_train_val_transposed1 = sales_train_val_transposed1.merge(pivoted_dfs[column], on=['d'], how='left').fillna(0)
            
    sales_train_val_transposed1['Weighted_Year'] = \
        sales_train_val_transposed1.swifter.apply(lambda x: (x['year']+ (x['month']/12) + int(x['date'].split('-')[2])/365 ), axis=1)
    
    # Separate date, sales and non-sales columns & rearrange column order
    sales_columns = [col for col in sales_train_val_transposed1.columns if set_name in col]
    sell_price_columns = [col for col in sales_train_val_transposed1.columns if 'Sell_Price' in col] # sell_price_columns = list(selling_prices.T.reset_index()['id'][1:])
    non_sales_columns = list(set(sales_train_val_transposed1.columns) - set(sales_columns + sell_price_columns + [DATE_COLUMN]))
    
    sales_train_val_transposed1 = sales_train_val_transposed1[[DATE_COLUMN] + non_sales_columns + sell_price_columns + sales_columns]
    
    return sales_train_val_transposed1, non_sales_columns, sell_price_columns, sales_columns


def darts_preprocessing(sales_train_val_transposed1, scaler_series, scaler_covariates, sales_columns, non_sales_columns, sell_price_columns, set_type, label_encoders):
    df = sales_train_val_transposed1.copy() # Full df

    # Convert the date column to datetime
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])

    # Set the date as the DataFrame's index
    df.set_index(DATE_COLUMN, inplace=True)

    # Prepare sales and covariates DataFrames for Full df
    df_sales = df[sales_columns]
    df_covariates = df[non_sales_columns + sell_price_columns]

    # df_sales = df[[col for col in df.columns if 'validation' in col]] # for Sample df
    # df_covariates =\
    #     df[[col for col in df.columns if col not in [col for col in df.columns if 'validation' in col] + [date_column]]] # for Sample df

    # Creating label encoders for categorical columns
    if set_type == 'validation':
        label_encoders = {}
    
    categorical_columns = ['d', 'weekday', 'event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']
    for col in categorical_columns:

        if set_type == 'validation':
            # Initialize a new label encoder for the column
            le = LabelEncoder()
            
        else:
            le = label_encoders[col]

        # Fit and transform the column. The transformation is stored in a temporary variable to avoid the warning.
        # Adding +1 so that NaN (encoded as -1) becomes 0
        transformed_col = le.fit_transform(df_covariates[col].astype(str)) + 1

        # Explicitly assign the transformed values back to the DataFrame using .loc to avoid the warning
        df_covariates.loc[:, col] = transformed_col

        if set_type == 'validation':
            # Store the fitted label encoder in the dictionary
            label_encoders[col] = le

    if set_type == 'validation':
        # Convert the sales and covariates DataFrames to Darts TimeSeries objects
        series = TimeSeries.from_dataframe(df_sales)
        covariates = TimeSeries.from_dataframe(df_covariates)
        
        # Split the series and covariates into training and validation sets
        train, val = series.split_before(0.8)
        train_covariates, val_covariates = covariates.split_before(0.8)

        # Scale the series and covariates (optional but recommended)
        scaler_series = Scaler()
        scaler_covariates = Scaler()

        train_scaled = scaler_series.fit_transform(train)
        val_scaled = scaler_series.transform(val)

        train_covariates_scaled = scaler_covariates.fit_transform(train_covariates)
        val_covariates_scaled = scaler_covariates.transform(val_covariates)

        
    else:
        eval_series = TimeSeries.from_dataframe(df_sales)
        eval_covariates = TimeSeries.from_dataframe(df_covariates)

        eval_scaled = scaler_series.fit_transform(eval_series)
        eval_covariates_scaled = scaler_covariates.transform(eval_covariates)        
        
    if set_type == 'validation':
        return train_scaled, val_scaled, train_covariates_scaled, val_covariates_scaled, scaler_series, scaler_covariates, df_sales, df_covariates, label_encoders
    else:
        return eval_scaled, eval_covariates_scaled, scaler_series, scaler_covariates, df_sales, df_covariates, label_encoders