import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as soup
import pandas as pd 
import datetime as dt

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    mars_dict={}
    #visit web page 
    url = "'https://mars.nasa.gov/news/'"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #Mars scrape title and paragraph
    news_title= soup.find_all("div", class_="content_title")[0].text
    news_p= soup.find_all("div", class_="article_teaser_body")[0].text
   


    # #Image scrape 
    # def scrape_image():

    site_url='https://www.jpl.nasa.gov'
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    full_image_element= browser.find_by_id("full_image")
    full_image_element.click()
    browser.is_element_present_by_text("more info", wait_time=2)

    more_info_element=browser.links.find_by_partial_text("more info")
    more_info_element.click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    path=soup.select_one('figure.lede a img').get("src")
    featured_image_url= site_url + path

    mars_dict['featured_image_url']=featured_image_url

#  

    # #Table

    table=pd.read_html('https://space-facts.com/mars/')[0]
    table.columns=['description','mars']
    mars_table=table.to_html(index=False)
    mars_table.replace('\n', '')

    

    #hemisphere
    main_url='https://astrogeology.usgs.gov'
    hem_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    hems=soup.find('div',class_='collapsible results')
    articles = soup.find_all('div', class_='item')


    image_urls = []

    # Iterate through each hemisphere data
    for article in hems:
        hem_article = soup.find('div', class_="description")
        link=hemisphere.a['href']
        title=hem_article.h3.text
        full_link=main_url+link
        browser.visit(full_link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hem_images=soup.find('div', class_='dowloads')
        image_list=soup.find('li').a['href']
  
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_list
        
        image_urls.append(image_dict)

    # # Store data in a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_table":mars_table,
        "hem_images": image_urls
    }
    return mars_dict