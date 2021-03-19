
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time





def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('ul', class_='item_list')
    results

    results = results.find('div', class_='content_title').text
    news_title=results.strip()
    news_title

    results_2=soup.find_all('div', class_='article_teaser_body')[0].text
    news_p=results_2.strip()
    print(news_p)


    image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    # Retrieve page with the requests module
    browser.visit(image_url)

    time.sleep(1)
    short_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    html = browser.html
        # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    target=soup.find_all('a', class_='showimg fancybox-thumbs')[0]
    target=target['href']
    target

    featured_image_url=short_image_url+target
    featured_image_url

    table_url='https://space-facts.com/mars/'


    tables=pd.read_html(table_url)
    tables

    df=tables[0]
    df.rename(columns = {0:'Label',  
                        1:'Facts'},  
                inplace = True) 
    df.set_index('Label')


    html_table = df.to_html()
    html_table
    df.to_html('table.html')
    # # Mars Hemispheres

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url="https://astrogeology.usgs.gov/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
        # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # %%
    #Finding Titles 
    image_titles=[]
    titles=soup.find_all('div', class_='description')
    for title in titles: 
            h3=title.find('h3').text
            image_titles.append(h3)
            

    image_titles

    partial_url=[]
    items=soup.find_all('div', class_='item')

    for item in items: 
            url=item.find('a')
            href=base_url+url['href']
            partial_url.append(href)
            print(base_url+url['href'])
    partial_url

    browser.visit(partial_url[0])
    time.sleep(1)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    full_image=soup.find('img', class_='wide-image')
    full_image=full_image['src']
    full_image_url=base_url+full_image

    full_image_url

    full_image_url_final=[]

    for url in partial_url: 
            browser.visit(url)
            html=browser.html
            soup = BeautifulSoup(html, 'html.parser')
            full_image=soup.find('img', class_='wide-image')
            full_image_url_final.append(base_url+full_image['src'])
            
    full_image_url_final

    image_dict=[]
    full_image_url_final


    for i in range(len(image_titles)):
        image_dict.append({'title':image_titles[i],'img_url':full_image_url_final[i]})

    len(image_titles)



    image_dict


    browser.quit()


    
    scraped_data = {}
    scraped_data["news_title"] = news_title
    scraped_data["news_p"] = news_p
    scraped_data["featured_image_url"] = featured_image_url
    scraped_data["marsfacts_html"] = html_table
    scraped_data["hemisphere_image_urls"] = image_dict

    return scraped_data

scrape_info()


