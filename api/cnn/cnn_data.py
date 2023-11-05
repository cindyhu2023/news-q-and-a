import pandas as pd
import os

# Load the first dataset
df1 = pd.read_csv('CNN_Articels_clean.csv')

# Load the second dataset
df2 = pd.read_csv('CNN_Articels_clean2.csv')

# Concatenate the two datasets
df = pd.concat([df1, df2])

# Filter articles published in 2022
# df_2022 = df[df['Date published'].str.startswith('2022') & (df['Category'] == 'news') & (df['Section'].isin(['us', 'world']))]
df_2022 = df[df['Date published'].str.startswith('2022')]
# category_counts = df_2022['Category'].value_counts()
# section_counts = df_2022['Section'].value_counts()
df_2022['Date published'] = pd.to_datetime(df_2022['Date published'])
# print(df_2022[df_2022['Url'] == 'https://www.cnn.com/2022/01/03/tech/elizabeth-holmes-verdict/index.html']['Category'])

# Write the filtered articles to a new CSV file
# df_2022.to_csv('CNN_Articles_2022.csv', index=False)

# headlines = df_2022['Headline']
# headlines.to_csv('headlines.txt', index=False, header=False)


import matplotlib.pyplot as plt

print(df_2022.describe())
df_2021 = df[df['Date published'].str.startswith('2021')]
df_2021['Date published'] = pd.to_datetime(df_2021['Date published'])
print(df_2021.describe())

plt.figure(figsize=(10, 6))
plt.hist(df_2021['Date published'], bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribution of Dates Published')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
