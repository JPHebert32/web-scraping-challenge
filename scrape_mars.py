import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser

#Browser
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News
    
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape the 1st Title & text for the 1st article
    news_title = soup.find('ul', class_="item_list").find("div", class_="content_title").get_text()   
    news_p = soup.find('ul', class_= "item_list").find("div", class_="article_teaser_body").get_text()


    # JPL Mars Space Images - Featured Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')

    # click the button for image url to the full size .jpg image.
    image_url = browser.find_by_id('full_image')
    image_url.click()
    # click more info url to the full size .jpg image.
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find('figure', class_="lede").find("a").get('href')

    url = 'https://www.jpl.nasa.gov'
    featured_image_url = url + featured_image_url

    # Mars Weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html = browser.html
    soup = bs(html,'html.parser')

    # Scrape Weather Tweet
    mars_weather = soup.find("div",{"lang": "en", "dir": "auto"}).text.replace("\n"," ").strip()

    # Mars Facts    