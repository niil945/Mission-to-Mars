# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
#Optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemisphere_image_urls.clear()

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
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

