
# TODO

# Scrape from CNBC
# Setup our database
# Process info

from selenium import webdriver as web
from selenium.webdriver.support import expected_conditions as con
from selenium.webdriver.support.ui import WebDriverWait as UI
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchAttributeException, TimeoutException
import DatabaseConfig
import alertSystem

import lxml
from bs4 import BeautifulSoup
import time
driver = '/Users/loganlach/PycharmProjects/chromedriver'


#CHOSE TO DO THIS PROjECT IN SELENIUM FOR TWO REASONS
#!.) Because I already can do beautifulsoup, so i want to learn something new
#2.) Thats about it, but im thinking of adding functionallity later of checking stocktwits so stay tuned
def scrape(input, email):
    #Specs for how we are gonna run selenium
    #YAHOO Finance takes forever to load, so we are gonna wait on our own terms
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    #Also since I have ironed out most of the bugs, we are gonna run it headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    temp = web.Chrome(driver, desired_capabilities=capa, options=chrome_options)
    #3 seconds max on timeout, have to give leway for internet usage
    wait = UI(temp, 6)
    data = DatabaseConfig.Database()
    #For every single stock we want to look at
    for stock in input:
        #get the website we want
        temp.get('https://finance.yahoo.com/quote/'+stock+'/')
        #Until we are able to click on this thing
        #It kind of sucks, it compromises performance but it straight up doesn't work if you don't use this to click
        try:
            wait.until(con.element_to_be_clickable((By.LINK_TEXT, 'Options')))
        #Click it when its ready
            link = temp.find_element_by_link_text('Options')
            link.click()
        except NoSuchAttributeException:
            print('Options button doesnt exist, moving to next one\n')
            continue
        except TimeoutException:
            print('Timed out when waiting/clicking the button, moving to the next one\n')
            continue


        #WAIT UNTIL THE PUTS TABLE IS LOADED
        #Takes time with XPATH, looking to find any other tag so performance is improved
        try:
            wait.until(con.presence_of_element_located((By.XPATH, '//*[@id="Col1-1-OptionContracts-Proxy"]/ section / section[2] / div[2] / div / table ')))
        except NoSuchAttributeException:
            print('Could not find the puts table, moving to the next')
            continue
        except TimeoutException:
            print('Timed out looking for the puts table, moving to the next one\n')
            continue

        #Using beautifulsoup in order to parse the page, works like a charm
        soup = BeautifulSoup(temp.page_source, 'lxml')
        print('FOR ' + stock + '\n')
        print('CALLS FOR DECEMBER 31st')
        other = soup.find('table',class_='calls W(100%) Pos(r) Bd(0) Pt(0) list-options').find_all('tr')
        #Just pulling the first 10 for now, will eventually move into the whole stack with database implementation
        hold = stock.replace('\n', '').replace('.','')
        for x in other:
        #for i in range(0,3):

            general = x.strings
            #general = other[i].strings
            quick = list(general)
            val = ''
            if(quick[0] != 'Contract Name'):
                if (quick[8] == '-'):
                    values = (quick[0],str(0))
                    val = data.analyzeDB(hold,values)
                else:
                    values = (quick[0], str(quick[8]))
                    val = data.analyzeDB(hold, values)
            if val != '':
                email.addMessage(val)



        other = soup.find('table',class_='puts W(100%) Pos(r) list-options').find_all('tr')
        print('PUTS FOR DECEMBER 31st')
        for x in other:
        #for i in range(0,3):
            general = x.strings
            #general = other[i].strings
            quick = list(general)
            val = ''
            if (quick[0] != 'Contract Name'):
                if (quick[8] == '-'):
                    values = [quick[0],str(0)]
                    val = data.analyzeDB(hold,values)
                else:
                    values = [quick[0], str(quick[8])]
                    val = data.analyzeDB(hold, values)
            if val != '':
                email.addMessage(val)




    temp.close()
    temp.quit()
    data.connection.commit()
    data.close()



file = open('S&P500.txt', 'r')
actual = []
currStock = file.readline()
count = 0
email = alertSystem.alertSystem()
while(currStock != ''):
    actual.append(currStock)
    currStock = file.readline()
    if(count % 10 == 1 and count != 0):
        #start = time.time()
        scrape(actual,email)
        #print('This took' +str(time.time() - start))
        actual = []
        time.sleep(3)
    count += 1
email.testoutput()
