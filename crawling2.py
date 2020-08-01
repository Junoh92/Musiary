from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Linux 서버에서는 GUI Browser를 구동할 수 없기 때문에 Headless Mode로 사용해야 한다.
chrome_options = webdriver.ChromeOptions()
# 크롬 헤드리스 모드 사용 위해 disable-gpu setting
chrome_options.add_argument('--disable-gpu')
# 크롬 헤드리스 모드 사용 위해 headless setting
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get('https://www.naver.com')
print('네이버접속성공')
# 검색창에 코로나 입력 후 엔터
search_input = driver.find_element_by_id('query')
search_input.send_keys('코로나')
search_input.send_keys(Keys.RETURN)
print('코로나 검색성공')
# 실시간검색 버튼을 CSS Selector 기반으로 찾기
button = driver.find_element_by_css_selector(
    '#lnb > div > div.lnb_menu > ul > li.lnb7 > a')
button.click()
print('실시간 검색성공')
# 더보기 버튼을 N번 눌러서 여러 개의 리뷰 얻어내기
for _ in range(3):
    more_button = driver.find_element_by_css_selector(
        '#realTimeSearchBody > div.rt_wrap.rt_typ2 > div.bt_more > a')
    more_button.click()
    # 더보기 버튼을 누른 후 로딩을 위해 잠시 대기
    time.sleep(1)

    # 스크롤 맨 아래로 내리기
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
print('더보기성공')
# 리뷰를 전부 찾은 뒤, 링크 주소와 텍스트를 출력
links = driver.find_elements_by_css_selector('ul.type01 a.txt_link')
for link in links:
    review_link = link.get_attribute('href')
    review_text = link.text
    print(review_link)
    print(review_text)

# 코드 실행을 잠시 멈춘다.
time.sleep(2)

# 사용을 마치면 드라이버를 종료시킨다.
driver.quit()