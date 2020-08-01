from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request

# Linux 서버에서는 GUI Browser를 구동할 수 없기 때문에 Headless Mode로 사용해야 한다.
chrome_options = webdriver.ChromeOptions()
# 크롬 헤드리스 모드 사용 위해 disable-gpu setting
chrome_options.add_argument('--disable-gpu')
# 크롬 헤드리스 모드 사용 위해 headless setting
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get('https://www.naver.com')

search_input = driver.find_element_by_id('query')
search_input.send_keys('권나라')
search_input.send_keys(Keys.RETURN)

# '이미지' 라는 텍스트를 가진 링크를 찾기
button = driver.find_element_by_link_text('이미지')
button.click()
time.sleep(2)

# 이미지 링크 수집
images = driver.find_elements_by_css_selector(
    'div.photowall a.thumb._thumb > img')

# 이미지를 저장할 images 폴더 생성
if not os.path.exists('./images'):
    os.mkdir('./images')

for index, image in enumerate(images):
    image_src = image.get_attribute('src')

    # gif / base64 가 아닌 jpg 이미지만 다운로드
    if 'https' in image_src and '.jpg' in image_src:
        extension = image_src.split('.')[-1]
        print(f'{index}: {image_src}')
        urllib.request.urlretrieve(image_src, f'./images/nara-{index}.jpg')

# 코드 실행을 잠시 멈춘다.
time.sleep(2)

# 사용을 마치면 드라이버를 종료시킨다.
driver.quit()