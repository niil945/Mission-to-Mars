# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemispheres = mars_hemispheres(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        #Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemispheres(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # Add try/except for error handling
    try:
        # 1. Use browser to visit the URL
        url = 'https://marshemispheres.com/'
        browser.visit(url)
        # 2. Create a list to hold the images and titles.
        hemisphere_image_urls = []
        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        
        #Optional delay for loading page
        browser.is_element_present_by_css('div.item', wait_time=1)
        # Parse the html for the links to the pages containing the full images
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        hemi_links = hemi_soup.findAll('div',attrs={'class':'description'})
        for div in hemi_links:
            links = div.findAll('a')
            for a in links:
                hemi_url = str("http://marshemispheres.com/" + a['href'])
                #print(hemi_url)
                browser.visit(hemi_url)
                hemi_html = browser.html
                img_hemi = soup(hemi_html, 'html.parser')
                #Find the relative image url and combine it with the base url
                img_url_rel = img_hemi.find('a', href=True, text='Sample').get('href')
                img_url = f'https://marshemispheres.com/{img_url_rel}'
                # Find the relative image title
                img_title = img_hemi.find('h2', class_='title').text
                # Add the title and full image url to the list
                image_info = {'img_url': img_url, 'title': img_title}
                hemisphere_image_urls.append(image_info)
        # 4. Print the list that holds the dictionary of each image url and title.
    except BaseException:
        return None
    
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())