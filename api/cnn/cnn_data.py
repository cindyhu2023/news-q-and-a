import pandas as pd
import os

# dataset source: https://www.kaggle.com/datasets/hadasu92/cnn-articles-after-basic-cleaning
# below is the code to filter the articles published in 2022 and output CNN_Articles_2022.csv

df1 = pd.read_csv('CNN_Articels_clean.csv')
df2 = pd.read_csv('CNN_Articels_clean2.csv')
df = pd.concat([df1, df2])

# Filter articles published in 2022
df_2022 = df[df['Date published'].str.startswith('2022')]
df_2022['Date published'] = pd.to_datetime(df_2022['Date published'])

# Write the filtered articles to a new CSV file
df_2022.to_csv('CNN_Articles_2022.csv', index=False)


