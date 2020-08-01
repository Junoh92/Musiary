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

search_input = driver.find_element_by_id('query')
search_input.send_keys('코로나')
search_input.send_keys(Keys.RETURN)
print(driver.title)

# 코드 실행을 잠시 멈춘다.
time.sleep(1)#realTimeSearchBody > div.rt_wrap.rt_typ2 > div.bt_more > a

# 사용을 마치면 드라이버를 종료시킨다.
driver.quit()