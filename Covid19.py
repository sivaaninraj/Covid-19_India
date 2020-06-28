# importing required libraries
import pandas as pd
from datetime import datetime
import os
import re
import glob
import requests 
from bs4 import BeautifulSoup
# Visualisation libraries
import matplotlib.pyplot as plt


# Manipulating the default plot size
plt.rcParams['figure.figsize'] = 10, 12



# get data

# link at which web data recides
link = 'https://www.mohfw.gov.in/'
# get web data
req = requests.get(link)
# parse web data
soup = BeautifulSoup(req.content, "html.parser")


# get the table head
# table head may contain the column names, titles, subtitles
thead = soup.find_all('thead')[-1]
# print(thead)

# get all the rows in table head
# it usually have only one row, which has the column names
head = thead.find_all('tr')
# print(head)

# get the table tbody
# it contains the contents
tbody = soup.find_all('tbody')[-1]
# print(tbody)

# get all the rows in table body
# each row is each state's entry
body = tbody.find_all('tr')
# print(body)


# container for header rows / column title
head_rows = []
# container for table body / contents
body_rows = []

# loop through the head and append each row to head
for tr in head:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    head_rows.append(row)
# print(head_rows)

# loop through the body and append each row to body
for tr in body:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    body_rows.append(row)
# print(head_rows)

# save contents in a dataframe
    
# skip last 3 rows, it contains unwanted info
# head_rows contains column title
df_bs = pd.DataFrame(body_rows[:len(body_rows)-6],columns=head_rows[0])       

# Drop 'S. No.' column
df_bs.drop('S. No.', axis=1, inplace=True)
print('Original Data')
print(df_bs)


#rename column
df_name = df_bs.copy()
new_name = 'State/UnionTerritory'
df_name = df_name.rename(columns={'Name of State / UT': new_name})
#df_name = df_name.rename(columns={'Name of State / UT':'State/UnionTerritory'})
print('After Renaming')
print(df_name)

#Sorting by name of states in desc order
#sort_by_confirmed = df_name.sort_values('State/UnionTerritory' , ascending = False)
sort_by_confirmed = df_name.sort_values(new_name , ascending = False)
print('After Sorting using name')
print(sort_by_confirmed)

#Pie chart
x = df_bs['Name of State / UT']
y = df_bs['Total Confirmed cases*']
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.pie(y,labels=x)
plt.show()    
