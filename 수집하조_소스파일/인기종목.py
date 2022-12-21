import csv
import requests
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='

filename = '시가총액1-100.csv'
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)

# table
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
table = soup.find('table', attrs={'class':'type_2'})

# title row 가져오기
title_rows = table.find('thead').find_all('th')
titles = [title_row.get_text() for title_row in title_rows]
# print(titles)
writer.writerow(titles)

# rows 가져오기
for page in range(1, 3):
	res = requests.get(url + str(page))
	res.raise_for_status()

	soup = BeautifulSoup(res.text, 'lxml')
	data_rows = soup.find('table', attrs={'class':'type_2'}).find('tbody').find_all('tr')
	for row in data_rows:
		columns = row.find_all('td')
		if len(columns) <= 1: # 의미 없는 데이터는 skip
			continue
		data = [column.get_text().strip() for column in columns[:-1]]
		# print(data)
		writer.writerow(data)
