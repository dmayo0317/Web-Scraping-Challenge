from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    #point to the directory where chromedriver exists
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create Mars_dict that we can insert into mongo
    mars_facts = {} 

    #Vist page
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
    #Using bs to write into html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #scrape site to collect latest News Titles and Paragraph Text
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")

    # URL of Mars Image to be scraped
    website_image_url='https://spaceimages-mars.com/'
    browser.visit(website_image_url)
    
    #Using bs to write into html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
   
    obtain_photo = soup.find_all('img')
    choosen_photo = soup.find_all('img')[1]["src"]
    featured_image_url = website_image_url + choosen_photo

    # URL of Mars Table to be scraped
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    type(tables)
    mars_tables_df = tables[0]
    mars_tables_df .columns = ["Properties","Mars","Earth"]
    mars_tables_df = mars_tables_df.iloc[1:]
    mars_table = mars_tables_df.to_html()
    mars_table.replace('\n','')

     
    mars_facts = {
        "news_title": news_title,
        "news_par": news_paragraph,
        "mars_Table": mars_table,
        "featured_image_url": featured_image_url,
    }
  

    browser.quit()

    return mars_facts