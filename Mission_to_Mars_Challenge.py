#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


executable_path = {'executable_path': "C:\Program Files\chromedriver_win32\chromedriver.exe"}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[13]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[15]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[16]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[17]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# In[18]:


# Scrape High Resolution Mars Hemisphere Images
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[19]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemisphere_img_loc = []
img_url =[]
title = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')
hemisphere_img = img_soup.find('div', class_="collapsible results")
hemisphere_imgs = hemisphere_img.find_all('div', class_="item")
for img in hemisphere_imgs:
    loc = img.find('a').get('href')
    img_title = img.find('h3').text
    # Visit URL
    url = f'https://astrogeology.usgs.gov{loc}'
    browser.visit(url)
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img = img_soup.find('img', class_="wide-image").get('src')
    img_link = f'https://astrogeology.usgs.gov{img}'
    img_url.append(img_link)
    title.append(img_title)
    img_dict = {'img_url':img_link, 'title':img_title}
    hemisphere_image_urls.append(img_dict)
    

hemisphere_image_urls


# In[20]:


browser.quit()

