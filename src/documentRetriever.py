from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import os

resume = input('Resume ?')
if resume != 'n':
    start = input('Where to start ?')
    start = int(start)
else:
    start = 1

os.makedirs(os.path.dirname('../errors.log'), exist_ok=True)
browser = webdriver.Chrome(executable_path='./chromedriver')
timeout = 15

with open('../posts.csv') as post_list:
    lst = post_list.readlines()
    for num, line in enumerate(lst[start - 1:], start):
        #--------------------------------------OpenPost--------------------------------------------#

        url = line.split(' ')[0]
        browser.get(url)

        print(str(num) + ': getting', url)
        try:
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.ID, 'last-pageing')))
        except TimeoutException:
            print('E: get page timeout')
            with open('../errors.log', 'a') as log_file:
                log_file.write('E: get page timeout ' + url + '\n')
            continue

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        last_page = soup.find('span', {'id': 'last-pageing'}).string
        last_page = int(last_page)
        pagination = Select(browser.find_element_by_class_name('dropdown-jump'))

        for i in range(1, last_page):
            page = str(i + 1)

            pagination.select_by_value(page)
            print("loading page", page)
            try:
                locator = 'comment' + str(i) + '01'
                WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, locator)))
            except TimeoutException:
                print('E: get page timeout')
                with open('../errors.log', 'a') as log_file:
                    log_file.write('E: get page timeout ' + url + '\n')
                continue
            browser.implicitly_wait(3)

        #---------------------------------------OpenReplies----------------------------------------#

        contains = browser.find_element_by_class_name('container-inner')

        sub_replies = contains.find_elements(By.CSS_SELECTOR, '.reply.see-more')
        for sub_reply in sub_replies:
            browser.execute_script('arguments[0].click();', sub_reply)

        sub_replies = contains.find_elements_by_class_name('load-reply-next')
        while len(sub_replies) > 0:
            for sub_reply in sub_replies:
                browser.execute_script('arguments[0].click();', sub_reply)
            sub_replies = contains.find_elements_by_class_name('load-reply-next')

        #------------------------------------StoreReplyText----------------------------------------#

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        path_name = '../data/' + url.split('/')[-1] + '.txt'
        os.makedirs(os.path.dirname(path_name), exist_ok=True)

        with open(path_name, 'w') as f:
            main_post = soup.find('div', {'class': 'main-post-inner'})
            title = main_post.find(class_='display-post-title').text
            comment = main_post.find('div', {'class': 'display-post-story'}).text
            comment = comment.lstrip().rstrip()

            f.write('title:' + title + '\n')
            f.write('comment:' + comment + '\n')

            posts = soup.find_all('div', {'class': 'display-post-wrapper-inner'})
            for post in posts:
                comment_id = post.find('span', {'class': 'display-post-number'})
                if comment_id:
                    comment_id = comment_id['id']
                    if not comment_id.startswith('comment'):
                        continue
                else:
                    continue

                try:
                    comment = post.find('div', {'class': 'display-post-story'}).text
                    i = comment.find("แก้ไขข้อความเมื่อ")
                    if i != -1:
                        comment = comment[:i]
                    comment = comment.lstrip().rstrip()
                except:
                    print('E: get post error', post)
                    with open('../errors.log', 'a') as log_file:
                        log_file.write('E: get post error ' + url + '\n')
                    continue

                f.write(comment_id + ':' + comment + '\n')
