# import dependencies

from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    
    #Create dictionary with data to be imported into Mongo
    mars_data = {}

    browser = init_browser()
    
    
    #NASA Mars News
    
    #Define url
    marsnews_url = "https://mars.nasa.gov/news/"
    browser.visit(marsnews_url)
    
    #HTML object
    html = browser.html

    #Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    
    #Find first article title
    marsnews_url_title = soup.find('div', class_='list_text').find('div', class_='content_title').text

    #Find first article paragraph
    marsnews_url_paragraph = soup.find('div', class_='article_teaser_body').text
    
    #Add to dictionary
    mars_data['marsnews_url_title'] = marsnews_url_title
    mars_data['marsnews_url_paragraph'] = marsnews_url_paragraph
    
    
    
    #JPL Mars Space Images - Featured Image    
    
    #Define url
    marsimage_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(marsimage_url)
    
    #Click full image and more info buttons
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    
    #HTML object
    html = browser.html

    #Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    
    #Scrape Featured Image URL
    image_url = soup.body.find('figure', class_='lede').find('a')['href']

    homepageurl = "https://www.jpl.nasa.gov"

    featuredimage_url = homepageurl + image_url
    
    #Add to dictionary
    mars_data['featuredimage_url'] = featuredimage_url
    
    
    
    ##Mars Facts
    
    #define url
    url = 'https://space-facts.com/mars/'
    
    #read and output table
    marstable = pd.read_html(url)[0]
    marstable.columns = ["Description", "Mars"]
    marstable = marstable.set_index(["Description"])
    
    #Add to dictionary
    mars_data['marstable'] = marstable
    
    
    
    #Mars Hemispheres
    
    #define url
    url = 'https://space-facts.com/mars/'
    
    #HTML object
    html = browser.html

    #Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    
    # Retrieve all items related to mars hemispheres
    results = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    #Loop through to get title and image urls
    for result in results:

        #Find titles and append to titles list
        title = result.find('h3').text

        #Find link for page with image and open in browser
        part_imageurl = result.find('div', class_='description').find('a')['href']
        homeurl = 'https://astrogeology.usgs.gov'
        url = homeurl + part_imageurl  
        browser.visit(url)

        #Scrape full image url and append to list
        html = browser.html
        soup = bs(html, 'html.parser')
        imageurl = soup.find('div', class_='downloads').find('a')['href']

        #Create dictionary with titles and image url
        hemisphere_image_urls.append({"title" : title, "img_url": imageurl})

    #Add to dictionary
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()
    
    return mars_data

    
    