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
search_input.send_keys('싸이 강남스타일')
search_input.send_keys(Keys.RETURN)
print('노래 검색성공')

# 뮤직검색 버튼을 CSS Selector 기반으로 찾기
button = driver.find_element_by_css_selector(
    '#lnb > div > div.lnb_menu > ul > li.lnb14 > a')
button.click()
print('음악 검색성공')
# 1위 음악클릭
button_music = driver.find_element_by_css_selector(
    '#main_pack > div.music.music_type.section._prs_mus_1st > ul > li:nth-child(1) > dl > dt > a.sh_music_title.music_tit')
button_music.click()
print('바이브 진입 성공')

#새 창 진입
driver.switch_to_window(driver.window_handles[1])
driver.get_window_position(driver.window_handles[1])
print('새 창 진입 성공')

#가사찾자 제발
paragraph = driver.find_element_by_css_selector('#content > div:nth-child(3) > p')
lyric = paragraph.text
print(lyric)

#앨범아트 따자
albumart = driver.find_element_by_css_selector('#content > div.summary_section > div.summary_thumb > img')
albumart_link = albumart.get_attribute('src')
print(albumart_link)

#앨범명도 따자
albumname = driver.find_element_by_css_selector('#content > div:nth-child(4) > div > div.text_area > div > a')
albumname_name = albumname.text
print(albumname_name)


driver.quit()