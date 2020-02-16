import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from datetime import datetime

url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"

#Do not display browser
#chrome_options = Options()  
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
print("Browser Invoked")
driver.get(url)
time.sleep(5)

commandFind = "//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']"
driver.find_element_by_xpath(commandFind).click()

element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')
#print(html_content)

# 2 - Parse HTML - BeaultifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

driver.quit()

# 3- Data Frame Structure Conversion - Pandas
df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['ranking', 'player', 'team', 'total']
#print(df)

# 4 - Convert data to dictionary
top10ranking = {}
top10ranking['points'] = df.to_dict('records')

# 5 - [Dump] Convert data and save to json
json = json.dumps(top10ranking)
file_name = 'ranking-top-10-' + str(datetime.now().date()) + '.json'
fp = open(file_name, 'w')
fp.write(json)
fp.close()

print('Saved JSON.')