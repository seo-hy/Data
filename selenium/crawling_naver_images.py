import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

### Set search keyword and max number of images to crawl
keyword = "keyword"
max = 10000

### Set path to save images
path = "./test/"
### Set chromedriver path
driver = webdriver.Chrome('c:/chromedriver.exe')


if not os.path.isdir(path):
    os.mkdir(path)
#URL
driver.get("https://search.naver.com/search.naver?where=image&sm=tab_jum&query=")

elem = driver.find_element_by_name("query")
elem.send_keys(keyword)
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1

## Infinite scroll

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

images = driver.find_elements_by_css_selector("._image._listImage")
count = 1
for image in images:
    try:
        image.click()
        time.sleep(2)
        # Set XPath : inspect -> copy XPath
        imgUrl = driver.find_element_by_xpath(
            '//*[@id="main_pack"]/section/div/div[1]/div[1]/div['+str(count)+']/div/div[1]/a/img').get_attribute(
            "src")
        urllib.request.urlretrieve(imgUrl, path+keyword+str(count) + ".jpg")
        count = count + 1
        if count == max:
            break
    except Exception as e:
        print(e)


driver.close()