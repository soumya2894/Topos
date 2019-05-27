from bs4 import BeautifulSoup
import pandas as pd
import requests

# The web scrapper link
WIKI_PAGE = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'

# Grab the page HTML and get the list of rows for the table
req = requests.get(WIKI_PAGE)
page_html = BeautifulSoup(req.text)
wiki_table = page_html.find('table', attrs = {'class':'wikitable sortable'})
row_list = wiki_table.find_all('tr')

# First row in the table is the header, so extract that separately
header_row = row_list.pop(0)
header_th = header_row.find_all('th')
header = [el.text for el in header_th]

table_dict = {x:[] for x in header}

# Now for the rest of the table...
for row in row_list:
 row_td = row.find_all('td')
 for el,td in zip(header,row_td):
  table_dict[el].append(td.text.replace("Â ",''))

# Writing to a csv file
dataFromWikiPage = pd.DataFrame(table_dict)
export_csv = dataFromWikiPage.to_csv (r'D:\export_dataframe.csv',encoding='utf-8-sig', index = None, header=True)
print(dataFromWikiPage)

# writing to an excel file
writer = pd.ExcelWriter(r'D:\pandas_conditional.xlsx', engine='xlsxwriter')
dataFromWikiPage.to_excel(writer, sheet_name='Sheet1')
workbook  = writer.book
worksheet = writer.sheets['Sheet1']
red_format = workbook.add_format({'bg_color':'red'})
writer.save()
