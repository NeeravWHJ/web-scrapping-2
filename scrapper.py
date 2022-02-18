from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

start_url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(start_url)
time.sleep(10)

headers = ["name","distance","mass","radius"]
planet_data = [],
new_planet_data = []

def scrape():
    for i in range(0,185):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for th_tag in soup.find_all("ul",attrs={"class","mass"}):
            tr_tags = th_tag.find_all("li")
            temp_list = []
            for index,tr_tag in enumerate(tr_tags):
                if index == 0:
                    temp_list.append(tr_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(tr_tag.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)           
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()     

def scrape_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content,"html.parser")
    for tr_tag in soup.find_all("tr",attrs = {"class","fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div",attrs = {"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
        new_planet_data.append(temp_list)


scrape()
for data in planet_data:
    scrape_more_data(data[5])

final_planet_data = []
for index,data in enumerate(planet_data):
    final_planet_data.append(data+final_planet_data[index])
with open("final_dwarf.csv", "w") as f: 
        csvwriter = csv.writer(f) 
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)    



scrape()
