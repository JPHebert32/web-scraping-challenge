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

    #___NASA Mars News___    
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape the 1st Title & text for the 1st article
    news_title = soup.find('ul', class_="item_list").find("div", class_="content_title").get_text()   
    news_p = soup.find('ul', class_= "item_list").find("div", class_="article_teaser_body").get_text()


    #___JPL Mars Space Images - Featured Image___
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

    #___Mars Weather___
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html = browser.html
    soup = bs(html,'html.parser')

    # Scrape Weather Tweet
    mars_weather = soup.find("div",{"lang": "en", "dir": "auto"})
    
    mars_weather = mars_weather[2].find_all("span")
    mars_weather[0].text


    #___Mars Facts___

    url4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url4)   
    facts_df = tables[0]
    facts_df.columns = ['Description', 'Value']

    # Set the index to the Description column
    facts_df = facts_df.set_index('Description', inplace=True)
    
    html_table = df.to_html()
    # Strip unwanted newlines to clean up the table.
    html_table = html_table.replace('\n', '')


    #___Mars Hemispheres___



    #___Dictionary of all Mars Info Scraped___
    mars_info_dict = {"news_title":news_title,"news_text":news_p,"featured_image":featured_image_url,
    "mars_weather":mars_weather,"facts_table":table_html} #"hemisphere_img":hemisphere_image_urls

    browser.quit()

    return  mars_info_dict