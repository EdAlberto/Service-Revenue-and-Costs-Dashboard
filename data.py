import pandas as pd

# Read files revenue and costs
df_revenue = pd.read_csv('revenue_2022.csv')
df_costs = pd.read_csv('costs_2022.csv')

# Apply cleaning for Line Of Business in revenue
df_revenue['Line Of Business'] = df_revenue['Line Of Business'].str.replace(' Revenue','')

# Function to map months columns to one column. Reshape the datasets with Line Of Business, Month and value columns
def transform_data(df, value_name):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Store each transformed dataframe in a list
    transformed_dfs = []

    for month in months:
        temp_df = df[['Line Of Business', month]].copy()
        temp_df['Month'] = month
        temp_df.rename(columns={month: value_name}, inplace=True)

        # Append the temporary dataframe to the list
        transformed_dfs.append(temp_df)

    # Concatenate all dataframes in the list
    return pd.concat(transformed_dfs, ignore_index=True)


# Transform both dataframes with new structure for reporting
df_revenue_transformed = transform_data(df_revenue, 'Revenue')
df_costs_transformed = transform_data(df_costs, 'Costs')

# Cleaning revenue characters to make standard for aggregations and reporting 
df_revenue_transformed['Revenue'] = df_revenue_transformed['Revenue'].str.replace('$','').str.replace('.00','').str.replace(',','').astype(float)


# Group by Line Of Business and Month and aggregate the Revenue
df_grouped_revenue = df_revenue_transformed.groupby(['Line Of Business', 'Month']).agg({'Revenue': 'sum'}).reset_index()

# Group by Line Of Business and Month and aggregate the Costs
df_grouped_costs = df_costs_transformed.groupby(['Line Of Business', 'Month']).agg({'Costs': 'sum'}).reset_index()


# Merge the transformed data by Line Of Business and Month and generate a dataframe with revenue and costs
df_grouped = pd.merge(df_grouped_revenue, df_grouped_costs, on=['Line Of Business', 'Month'])

# Test
print (df_grouped.head())
print(df_grouped.groupby(['Month'])['Costs'].sum().sort_values(ascending=False))




