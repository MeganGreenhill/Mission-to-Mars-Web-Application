from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.nhl_db
    collection = db.articles

    # Set up Splinter browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ### NASA Mars News - Scrape the [Mars News Site](https://redplanetscience.com/) and collect the latest News Title and Paragraph Text.
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    # Define HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the article summary text
    news_results_soup = news_soup.find('div', class_='article_teaser_body')
    news_results = news_results_soup.text

    # Retrieve the article title
    news_title_soup = news_soup.find('div', class_='content_title')
    news_title = news_title_soup.text

    ### JPL Mars Space Images - Featured Image
    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)

    # Define HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html, 'html.parser')

    # Find the src for the image
    relative_image_path = image_soup.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url = image_url + '/' + relative_image_path

    ### Mars Facts - Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # URL of page to be scraped
    facts_url = 'https://galaxyfacts-mars.com'

    # Retrieve page with the requests module
    facts_response = requests.get(facts_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    facts_soup = BeautifulSoup(facts_response.text, 'html.parser')

    # Retrieve the parent divs for all articles
    facts_results = facts_soup.find_all('table', class_='table table-striped')

    # Use Pandas to convert the data to a HTML table string.
    mars_facts_df = pd.read_html(str(facts_results))[0]
    mars_facts_df = mars_facts_df.rename(columns={0:"",1:"Mars"})
    mars_facts_df = mars_facts_df.set_index("")
    mars_facts_df.to_html("mars_facts.html")

    ### Mars Hemispheres - Obtain high resolution images for each of Mar's hemispheres.
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

    # Define list for iterating through images
    hemi_image_urls = []

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    hemisphere_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain image pages
    images = hemisphere_soup.find_all('a', class_='itemLink product-item')

    # Iterate through each image and obtain url for full image
    for x in range(4):
        href = images[(2*x)]['href']
        click_image_url = hemisphere_url + href
        browser.visit(click_image_url)
        html = browser.html
        individual_image_soup = BeautifulSoup(html, 'html.parser')
        full_image_path = individual_image_soup.find_all('img', class_='wide-image')[0]["src"]
        full_image_url = hemisphere_url + full_image_path
        hemi_image_urls.append(full_image_url)
    
    # Construct dictionary
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": hemi_image_urls[0]},
        {"title": "Schiaparelli Hemisphere", "img_url": hemi_image_urls[1]},
        {"title": "Syrtis Major Hemisphere", "img_url": hemi_image_urls[2]},
        {"title": "Valles Marineris Hemisphere", "img_url": hemi_image_urls[3]}
    ]

    # Define HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    hemisphere_soup = BeautifulSoup(html, 'html.parser')

    # Store data in a dictionary
    mars_data = {
        "news_results": news_results,
        "news_title": news_title,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
