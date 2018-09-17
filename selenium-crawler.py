from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome(executable_path='./chromedriver')
browser.maximize_window()

timeout = 10

#--------------------------------------------------------------------------------------------------#

browser.get('https://pantip.com/topic/37823050')

try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.ID, 'last-pageing')))
except TimeoutException:
    print('E: get page timeout')

soup = BeautifulSoup(browser.page_source, 'html.parser')

last_page = soup.find('span', {'id': 'last-pageing'}).string
last_page = int(last_page)
pagination = Select(browser.find_element_by_class_name('dropdown-jump'))

for i in range(1, last_page):
    page = str(i + 1)

    pagination.select_by_value(page)
    print("loading page", page)
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.ID, 'pageno-title-' + page)))
    except TimeoutException:
        print('E: get page timeout')

#--------------------------------------------------------------------------------------------------#

contains = browser.find_element_by_class_name('container-inner')

sub_replies = contains.find_elements(By.CSS_SELECTOR, '.reply.see-more')
for sub_reply in sub_replies:
    browser.execute_script('arguments[0].click();', sub_reply)

sub_replies = contains.find_elements_by_class_name('load-reply-next')
while len(sub_replies) > 0:
    for sub_reply in sub_replies:
        browser.execute_script('arguments[0].click();', sub_reply)
    sub_replies = contains.find_elements_by_class_name('load-reply-next')

#--------------------------------------------------------------------------------------------------#

soup = BeautifulSoup(browser.page_source, 'html.parser')
posts = soup.find_all('div', {'class': 'display-post-wrapper-inner'})
for post in posts:
    try:
        comment = post.find('div', {'class': 'display-post-story'}).string
    except:
        print('E: get post error', post)
    comment_id = post.find('span', {'class': 'display-post-number'})
    if comment_id:
        comment_id = comment_id['id']
    print(comment_id, comment)
