from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv

chromeDriver = "cd/chromedriver"

csvFile = open('result.csv','w')
csvWrtiter = csv.writer(csvFile)
csvWrtiter.writerow(['Title','Price','Url'])

class scraper(object):
    def __init__(self,minPrice,maxPrice): 
        self.maxPrice = maxPrice
        self.minPrice = minPrice
        self.url = 'https://delhi.craigslist.org/search/sss?min_price={}&max_price={}'.format(minPrice,maxPrice)
        self.driver = webdriver.Chrome(chromeDriver)
        self.delay = 5
           

    def loadUrl(self):
        self.driver.get(self.url)

        try:
            wait = WebDriverWait(self.driver,self.delay)
            wait.until(EC.presence_of_all_elements_located((By.ID,"searchform")))
            print("Page loaded")
        except TimeoutException:
            print("Can't load / End reached")

    def getData(self):
        htmlPage = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(htmlPage,'lxml')

        for post in soup.findAll('li',class_='result-row'):
            title = post.find('a',class_="hdrlnk")
            price = post.find('span',class_="result-price")
            url = post.find('a',class_="result-title hdrlnk")
            
            if title is None:
                title = "Not Listed"
            else:
                title = title.text

            if price is None:
                price ="Not Listed"
            else:
                price = price.text 
            
            if url is None:
                url = "Not Listed"
            else:
                url =url['href']

            csvWrtiter.writerow([title,price,url])
            print(price)
            print(title)
            print(url)

            print()   
        
        nextPage = soup.find('',class_="button next")
        if nextPage is not None:
            self.url = 'https://delhi.craigslist.org'+nextPage['href']
            self.loadUrl()
            self.getData()

print("Search cragslist Delhi")
minPrice = input("Enter minimum Price ")
maxPrice = input("Enter max Price ")
obj = scraper(minPrice,maxPrice)
obj.loadUrl()
obj.getData()
csvFile.close()
obj.driver.close()