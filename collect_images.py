from bs4 import BeautifulSoup as bs
from selenium import webdriver
from urllib import request
import base64
import re
import time


def scroll_down():
    global driver
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")

            try:
                driver.find_element_by_class_name("mye4qd").click()
            except:

                if new_height == last_height:
                    break

        last_height = new_height


if __name__ == '__main__':
    target_keyward = 'credit cards'
    num_crawl = 1500
    target_url = f'https://www.google.co.kr/search?q={target_keyward}&tbm=isch'
    target_url = target_url.replace(' ', '+')
    print(f'Target url :  {target_url}')

    # need absolute path.
    driver = webdriver.Chrome('/Users/jonghyeok/Desktop/workspace/card_number_masking/chromedriver')
    # for using this, Chrome browser and Chrome web driver should be installed on your system.
    # and both should be same version.
    # https://chromedriver.chromium.org/downloads
    driver.get(target_url)

    time.sleep(1)

    scroll_down()

    # Add user agent prevent bot security.
    request_html = driver.page_source
    parser = bs(request_html, 'html.parser')

    # find image has class 'rg_i Q4LuWd'. check 'parser.find_all()'
    results = parser.find_all('img', attrs={'class': 'rg_i Q4LuWd'})
    print('len(results): ', len(results))
    for dat in results:
        print(dat)
        try:
            base64encoded = dat['src']
        except:
            base64encoded = dat['data-src']

        # set file name.
        file_name = re.sub(r"[^a-zA-Z0-9]", "", dat['alt'])

        if base64encoded.split(',')[0] == 'data:image/jpeg;base64':
            encoded_img = base64encoded.split(',')[1]

            with open(f"data/{file_name}.jpg", "wb") as img:
                decoded_img = base64.b64decode(encoded_img)
                img.write(decoded_img)
                print(f'{file_name}.jpg saved.')
        else:
            try:
                request.urlretrieve(base64encoded, f'data/{file_name}.jpg')
                print(f'{file_name}.jpg saved.')
            except:
                print('Can not find image data.')


