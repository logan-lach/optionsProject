
# TODO

# Scrape from CNBC
# Setup our database
# Process info

from selenium import webdriver as web
from selenium.webdriver.support import expected_conditions as con
from selenium.webdriver.support.ui import WebDriverWait as UI
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

import lxml
from bs4 import BeautifulSoup
import time
driver = '/Users/loganlach/PycharmProjects/chromedriver'

def scrape():
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"


    temp = web.Chrome(driver, desired_capabilities=capa)
    wait = UI(temp, 3)

    temp.get('https://finance.yahoo.com/quote/TSLA/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAMNhvzD_Gy7KvZdz4ets6Uu8o80tElDkQ0S1pyElxmL_kUa_FvTVN4uDD3uOnfhsImvDOUPCd9_t6LK1al3AZe0KFJuJ1W0_qFIop1MmAPKMbg8JAzfLTLDaGpjfp1UiNzcK_q6fkykn4GMXXZSw5aUFz9ZAoLwRTrmLxmbS3Xjd')
    wait.until(con.element_to_be_clickable((By.LINK_TEXT, 'Options')))
    link = temp.find_element_by_link_text('Options')
    link.click()
    time.sleep(2)

    print(temp.current_url)
    soup = BeautifulSoup(temp.page_source, 'lxml')
    for i in range(0,50):
        print('CALLS FOR DECEMBER 31st')
        other = soup.find('tr',class_='data-row'+str(i)+' Bgc($hoverBgColor):h BdT Bdc($seperatorColor) H(33px) in-the-money Bgc($hoverBgColor)').strings
        t = list(other)
        print(t)
    for i in range(0,50):
        print('PUTS FOR DECEMBER 31st')
        other = soup.find()

    #t = list(other)
    #print(t)

    temp.close()
    temp.quit()




scrape()
