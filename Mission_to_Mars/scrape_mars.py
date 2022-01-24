import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
from splinter import Browser

def scrape():
    output={}

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #opening the url in chrome browser page
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    #saving html code to a variable
    html = browser.html

    soup = bs(html, 'html.parser')

    ## NASA Mars News
    #scrapping the latest news title
    news_title = soup.find("div", class_="content_title").text
    output['news_title'] = news_title
    
    #scrapping paragraph text for the latest news title
    news_p = soup.find("div", class_="article_teaser_body").text
    output['news_p'] = news_p
   
    ## JPL Mars Space Images - Featured Image
    images_url = "https://spaceimages-mars.com/"
    browser.visit(images_url)
    #saving html code to a variable
    html = browser.html
    images_soup = bs(html, 'html.parser')
    #navigating to the "full image" link through splinter
    browser.links.find_by_partial_text('FULL IMAGE').click()
    # find the relative image url
    img_url_rel = images_soup.find('img', class_='headerimage fade-in').get('src')
    print(img_url_rel)
    featured_image_url = f'https://spaceimages-mars.com/{img_url_rel}'
    output['featured_image_url'] = featured_image_url
    ## Mars Facts
    facts_url = "https://galaxyfacts-mars.com/"
    #saving html code to a variable
    facts = pd.read_html(facts_url, header=0)[0]
    facts_html = facts.to_html()
    output['facts_html'] = facts_html
    ## Mars Hemispheres
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    #saving html code to a variable
    html = browser.html
    hemispheres_soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    for x in range(0,4):
        #navigating to each link through splinter
        browser.links.find_by_partial_text('Hemisphere')[x].click()
        html = browser.html
        hemi_soup = bs(html,'html.parser')
        
        # defining variables for saving scrapped data
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')
        
        # Store findings into a dictionary and append to list
        hemispheres = {}
        hemispheres['title'] = title
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemisphere_image_urls.append(hemispheres)
        
        # Browse back to repeat
        browser.back()

    output['hemispheres'] = hemisphere_image_urls
    
    #closing the browser
    browser.quit()

    return output

# scrape()