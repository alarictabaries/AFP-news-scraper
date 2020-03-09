from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import datetime

from lib import misc

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

# Scrape posts from Mediapart
url = 'https://www.mediapart.fr/journal/type-darticles/breve?page='

# Scraping interval (the interval includes the limits)
before_date = '03/05/2020'
after_date = '03/03/2020'

news = []

driver = webdriver.Chrome(options=chrome_options)

scrape = True
page = 0

while scrape:
    page += 1
    driver.implicitly_wait(1)
    driver.get(url + str(page))

    # Loop in the posts
    try:
        for post in driver.find_elements_by_css_selector('.post-list>li'):

            append = True

            # Scrape elements of a post (title, asbtract, journalist, date)
            title = post.find_element_by_class_name('title').text
            journalist = post.find_element_by_class_name('journalist').text
            textual_date = post.find_element_by_css_selector('time').text
            abstract = post.find_element_by_css_selector('p').text

            d = textual_date.split()[0]
            m = misc.monthToNum(textual_date.split()[1])
            y = textual_date.split()[2]
            date = m + '/' + "{:02d}".format(int(d)) + '/' + y



            # Check if the post is in the specified interval
            before_date_arr = before_date.split('/')
            after_date_arr = after_date.split('/')
            date_arr = date.split('/')
            if datetime.date(int(date_arr[2]), int(date_arr[1]), int(date_arr[0])) > datetime.date(int(before_date_arr[2]), int(before_date_arr[1]), int(before_date_arr[0])):
                append = False
            elif datetime.date(int(date_arr[2]), int(date_arr[1]), int(date_arr[0])) < datetime.date(int(after_date_arr[2]), int(after_date_arr[1]), int(after_date_arr[0])):
                append = False
                scrape = False

            # Append to a dict.
            if append:
                news.append({'title': title, 'date': date, 'journalist': journalist, 'abstract': abstract})
    except NoSuchElementException:
        print('Error : can\'t find posts on the page.')

driver.close()