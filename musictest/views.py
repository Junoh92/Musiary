from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
import requests


from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

from spotdl.command_line.core import Spotdl
import os
from django.core.files import File

from mutagen import File

from django.contrib.auth.models import User

def index(request):
    posts = Post.objects.all()
    context = {'posts': posts,              }
    return render (request, 'musictest/index.html', context)
    
def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'musictest/detail.html', context)
    
@login_required    
def create(request):
    user = request.user
    image = None
    if 'image' in request.FILES:
        image = request.FILES['image']
    music = request.POST['music'] #검색하고자 하는 음악 타이틀 입력
    singer = request.POST['singer'] #검색하고자 하는 가수 입력
    args = { "no_encode":False, 'output_ext': 'mp3', 'output_file': f'./songs/{singer}-{music}.mp3', 'quality': 'best',
             } #검색옵션, 다운로드 mp3형식, 다운로드 파일명은 가수 - 타이틀.mp3
    try:
        spotdl_handler = Spotdl(args) #spotdl.handler에 검색옵션 저장
        spotdl_handler.download_track(f'{singer} {music}') #'가수 타이틀' 로 노래 검색 후 다운로드
    except:
        print('노래가 검색되지 않았습니다.')
        return redirect('musictest:index')
        
###############################################정보 다 따오자 
    # Linux 서버에서는 GUI Browser를 구동할 수 없기 때문에 Headless Mode로 사용해야 한다.
    chrome_options = webdriver.ChromeOptions()
    # 크롬 헤드리스 모드 사용 위해 disable-gpu setting
    chrome_options.add_argument('--disable-gpu')
    # 크롬 헤드리스 모드 사용 위해 headless setting
    chrome_options.add_argument('--headless')
    
    
    #벅스 내에서 노래 검색
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(3)
    driver.get(f'https://music.bugs.co.kr/search/integrated?q={singer} {music}')
    print('벅스 검색 성공')

    #노래 제목 따오기 
    try: 
        music_official_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(1) > th > p > a')
        music_official = music_official_link.text
        print(music_official)
    except:
        music_official = '곡 정보가 없습니다.'
        driver.quit()
    #앨범 이름 따오기
    try:
        albumlink = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr > td:nth-child(8) > a')
        album_official = albumlink.text
        print(album_official)
    except:
        album_official = '앨범 정보가 없습니다'
        driver.quit()
    #아티스트 이름 따오기
    try: 
        artistlink = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr > td:nth-child(7) > p > a')
        artist_official = artistlink.text
        print(artist_official)
    except:
        artist_official = '아티스트 정보가 없습니다'
        driver.quit()
    #검색결과 첫번째 url 딴 후 접속
    try:
        link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(1) > td:nth-child(5) > a')
        linkurl = link.get_attribute('href')
        driver.get(linkurl)
        print('첫번째 곡 정보 페이지 진입 성공')
    
    except:
        driver.quit()
    
    #앨범아트 따오기
    albumartlink = driver.find_element_by_css_selector('#container > section.sectionPadding.summaryInfo.summaryTrack > div > div.basicInfo > div > ul > li > a > img')
    albumart_link = albumartlink.get_attribute('src')
    print(albumart_link)

    #가사 따오기 제발 진짜
    try:
        lyriclink = driver.find_element_by_css_selector('#container > section.sectionPadding.contents.lyrics > div > div > xmp')
        lyric_official = lyriclink.text
        print(lyric_official)
    except:
        lyric_official = '가사 정보가 없거나, 19세 이상 이용가능 음악입니다'
        print(lyric_official)
    # 사용을 마치면 드라이버를 종료시킨다.
    
    driver.quit()
    ###################################################################################################################################################################
    
    tag = request.POST['tag'] 
    body = request.POST['body']
    song = f'./songs/{singer}-{music}.mp3'  #song에 받은 파일을 지정해주기
    post = Post(user=user, song=song, image=image,music=music, singer=singer, tag=tag, body=body, created_at=timezone.now() , music_official = music_official, artist_official = artist_official, album_official = album_official,
                albumart_link = albumart_link, lyric_official = lyric_official )#post에 저장
    post.save()
    # os.remove(f'{singer} - {music}.mp3')s
    return redirect('musictest:detail', post_id=post.id)
    
# @login_required    
# def search(request):
#     keyword = request.GET['song']
#     args = { "no_encode":False, 'output_ext': 'mp3', 'output_file': '{artist} - {track-name}.{output-ext}', }
#     spotdl_handler = Spotdl(args)
#     song = spotdl_handler.download_track(keyword)
#     post = Post(song = song)
#     post.save()
#     return redirect('musictest:new')
    

@login_required    
def new(request):
    # if not request.user.is_authenticated:
    #     return redirect('accounts:login')
        
    return render(request, 'musictest/new.html')

@login_required
def edit(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')
    context={'post':post}
    return render(request, 'musictest/edit.html', context)

@login_required        
def update(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')
        
    post.user = request.user
    if 'image' in request.FILES:
        post.image = request.FILES['image']
    post.music = request.POST['music']
    post.singer = request.POST['singer']
    post.tag = request.POST['tag']
    post.body = request.POST['body']
    post.save()
    return redirect('musictest:detail', post_id=post.id)

@login_required        
def delete(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('musictest:index')
    context={'post': post}
    return render(request, 'musictest/delete.html', context)

@login_required    
def realdelete(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return redirect('musictest:index')
    post.delete()
    return redirect('musictest:index')
    
@login_required
def like(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            
            if request.user in post.liked_users.all():
                post.liked_users.remove(request.user)
            else:
                post.liked_users.add(request.user)
                
            return redirect('musictest:detail',post.id)
            
        except Post.DoesNotExist:
            pass
    return redirect('musictest:index')

@login_required
def search_A(request):
    return render(request, 'musictest/new1_search.html')
    
@login_required
def search_B(request):
    music1 = request.GET['music1']
    print(music1)
    context={'music1': music1}
    return render(request, 'musictest/new2_search.html', context)
    
@login_required
def search_C(request):
    music2 = request.GET['music2']
    singer1 = request.GET['singer1']
    print(music2)
    print(singer1)
    context={'music2' : music2, 'singer1' : singer1 }
    return render(request, 'musictest/new3_search.html', context)
    
def search_D(request):
    music3 = request.GET['music3']
    singer2 = request.GET['singer2']
    print(music3)
    print(singer2)
###############################################정보 다 따오자 
    # Linux 서버에서는 GUI Browser를 구동할 수 없기 때문에 Headless Mode로 사용해야 한다.
    chrome_options = webdriver.ChromeOptions()
    # 크롬 헤드리스 모드 사용 위해 disable-gpu setting
    chrome_options.add_argument('--disable-gpu')
    # 크롬 헤드리스 모드 사용 위해 headless setting
    chrome_options.add_argument('--headless')
    
    
    #벅스 내에서 노래 검색
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(3)
    driver.get(f'https://music.bugs.co.kr/search/integrated?q={singer2} {music3}')
    print('벅스 검색 성공')
##################
    #검색결과 1위 따오기 
    try: 
        search_music1_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(1) > th > p > a')
        search_music1 = search_music1_link.text
        print(search_music1)
    except:
        search_music1 = '곡 정보가 없습니다.'
        search_album1 = False
        search_artist1 = False
        search_miniart1 = False
        search_music2 = False
        search_album2 = False
        search_artist2 = False
        search_miniart2 = False
        info2 = False
        search_music3 = False
        search_album3 = False
        search_artist3 = False
        search_miniart3 = False
        info3 = False   
        driver.quit()
    #앨범 이름 따오기
    try:
        search_album1_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr > td:nth-child(8) > a')
        search_album1 = search_album1_link.text
        print(search_album1)
    except:
        search_album1 = '앨범 정보가 없습니다'
    #아티스트 이름 따오기
    try: 
        search_artist1_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr > td:nth-child(7) > p > a')
        search_artist1 = search_artist1_link.text
        print(search_artist1)
    except:
        search_artist1 = '아티스트 정보가 없습니다'
    #미리보기 앨범아트 따오기
    try:
        search_miniart1_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(1) > td:nth-child(4) > a > img')
        search_miniart1 = search_miniart1_link.get_attribute('src')
        print(search_miniart1)
    except:
        search_miniart1 = False
    #세부정보 링크 따기
    try:
        info1_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(1) > td:nth-child(5) > a')
        info1 = info1_link.get_attribute('href')
    except:
        info1 = False
    print(info1)
##################
    #검색결과 2위 따오기 

    try: 
        search_music2_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(2) > th > p > a')
        search_music2 = search_music2_link.text
        print(search_music2)
    except:
        search_music2 = False
        search_album2 = False
        search_artist2 = False
        search_miniart2 = False
        info2 = False
        search_music3 = False
        search_album3 = False
        search_artist3 = False
        search_miniart3 = False
        info3 = False
        driver.quit()
        
    #앨범 이름 따오기
    try:
        search_album2_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(2) > td:nth-child(8) > a')
        search_album2 = search_album2_link.text
        print(search_album2)
    except:
        search_album2 = False
    #아티스트 이름 따오기
    try: 
        search_artist2_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(2) > td:nth-child(7) > p > a')
        search_artist2 = search_artist2_link.text
        print(search_artist2)
    except:
        search_artist2 = False
    #미리보기 앨범아트 따오기
    try:
        search_miniart2_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(2) > td:nth-child(4) > a > img')
        search_miniart2 = search_miniart2_link.get_attribute('src')
        print(search_miniart2)
    except:
        search_miniart2 = False
    #세부정보 링크 따기
    try:
        info2_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(2) > td:nth-child(5) > a')
        info2 = info2_link.get_attribute('href')
    except:
        info2 = False
    print(info2)
    
##################
    #검색결과 3위 따오기
    try: 
        search_music3_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(3) > th > p > a')
        search_music3 = search_music3_link.text
        print(search_music3)
    except:
        search_music3 = False
        search_album3 = False
        search_artist3 = False
        search_miniart3 = False
        info3 = False
        driver.quit()
    #앨범 이름 따오기
    try:
        search_album3_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(3) > td:nth-child(8) > a')
        search_album3 = search_album3_link.text
        print(search_album3)
    except:
        search_album3 = False
    #아티스트 이름 따오기
    try: 
        search_artist3_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(3) > td:nth-child(7) > p > a')
        search_artist3 = search_artist3_link.text
        print(search_artist3)
    except:
        search_artist3 = False
    #미리보기 앨범아트 따오기
    try:
        search_miniart3_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(3) > td:nth-child(4) > a > img')
        search_miniart3 = search_miniart3_link.get_attribute('src')
        print(search_miniart3)
    except:
        search_miniart3 = False
    #세부정보 링크 따기
    try:
        info3_link = driver.find_element_by_css_selector('#DEFAULT0 > table > tbody > tr:nth-child(3) > td:nth-child(5) > a')
        info3 = info3_link.get_attribute('href')
    except:
        info3 = False
        
    driver.quit()    
    
###################################################################값들 session으로 다음 결과창으로 넘겨주기
    context={'search_music1' : search_music1, 'search_album1' : search_album1, 'search_artist1' : search_artist1, 'search_miniart1' : search_miniart1, 'info1' : info1,
                        'search_music2' : search_music2, 'search_album2' : search_album2, 'search_artist2' : search_artist2, 'search_miniart2' : search_miniart2, 'info2' : info2,
                        'search_music3' : search_music3, 'search_album3' : search_album3, 'search_artist3' : search_artist3, 'search_miniart3' : search_miniart3, 'info3' : info3,
                        'music' : music3, 'singer' : singer2 }
    
    search_result = {'search_music1' : search_music1, 'search_album1' : search_album1, 'search_artist1' : search_artist1, 'search_miniart1' : search_miniart1, 
                        'search_music2' : search_music2, 'search_album2' : search_album2, 'search_artist2' : search_artist2, 'search_miniart2' : search_miniart2,
                        'search_music3' : search_music3, 'search_album3' : search_album3, 'search_artist3' : search_artist3, 'search_miniart3' : search_miniart3 }
    request.session['search_result'] = search_result
    return render(request, 'musictest/new4_search.html', context)
    
    
###########첫번째 꺼 클릭했을때#################
@login_required
def search_E_A(request):
    artist_official = request.GET['artist_official']
    music_official = request.GET['music_official']
    album_official = request.GET['album_official']
    info_official = request.GET['info_official']
    context = {'artist_official':artist_official, 'music_official' : music_official, 'album_official' : album_official, 'info_official':info_official}
    return render(request, 'musictest/new5_search.html',context)
    
@login_required
def search_F(request):
    artist_official = request.GET['artist_official']
    music_official = request.GET['music_official']
    album_official = request.GET['album_official']
    info_official = request.GET['info_official']
    args = { "no_encode":False, 'output_ext': 'mp3', 'output_file': f'./songs/{artist_official}-{music_official}.mp3', 'quality': 'best', 'overwrite' : 'skip'
             } #검색옵션, 다운로드 mp3형식, 다운로드 파일명은 가수 - 타이틀.mp3
    try:
        spotdl_handler = Spotdl(args) #spotdl.handler에 검색옵션 저장
        spotdl_handler.download_track(f'{artist_official} {music_official}') #'가수 타이틀' 로 노래 검색 후 다운로드
    except:
        print('노래가 검색되지 않았습니다.')
        return redirect('musictest:index')
    song_official = f'./songs/{artist_official}-{music_official}.mp3'
    
    if album_official == "None":
        album_official = False
        info_official = False
        albumart_official = False
        lyric_official = False
    else:
###############################################정보 다 따오자 
    # Linux 서버에서는 GUI Browser를 구동할 수 없기 때문에 Headless Mode로 사용해야 한다.
        chrome_options = webdriver.ChromeOptions()
        # 크롬 헤드리스 모드 사용 위해 disable-gpu setting
        chrome_options.add_argument('--disable-gpu')
        # 크롬 헤드리스 모드 사용 위해 headless setting
        chrome_options.add_argument('--headless')
        
        
        #벅스 내에서 노래 검색
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(3)
        driver.get(info_official)
        print('벅스 검색 성공')
        
        #가사 따오기 제발 진짜
        try:
            lyriclink = driver.find_element_by_css_selector('#container > section.sectionPadding.contents.lyrics > div > div > xmp')
            lyric_official = lyriclink.text
            print(lyric_official)
        except:
            lyric_official = '가사 정보가 없거나, 19세 이상 이용가능 음악입니다'
            print(lyric_official)
            
        #앨범아트 따오기
        albumartlink = driver.find_element_by_css_selector('#container > section.sectionPadding.summaryInfo.summaryTrack > div > div.basicInfo > div > ul > li > a')
        albumartlink.click()
        userName = driver.find_element_by_css_selector("#container > section.sectionPadding.summaryInfo.summaryAlbum > div > div.basicInfo > div > ul > li > a")
        driver.execute_script("arguments[0].click();", userName)
        albumart = driver.find_element_by_css_selector('#originalPhotoViewBtn > img')
        albumart_official = albumart.get_attribute('src')
        print(albumart_official)
            
        
    context = {'artist_official':artist_official, 'music_official' : music_official, 'album_official' : album_official, 'info_official':info_official, 'song_official' : song_official, 'lyric_official' : lyric_official, 'albumart_official' : albumart_official}
    return render (request, 'musictest/new6_search.html', context)

@login_required    
def write_A(request):
    artist_official = request.POST['artist_official']
    music_official = request.POST['music_official']
    album_official = request.POST['album_official']
    lyric_official = request.POST['lyric_official']
    albumart_official = request.POST['albumart_official']
    song_official = f'./songs/{artist_official}-{music_official}.mp3'
    context = {'artist_official': artist_official, 'music_official' : music_official, 'album_official' : album_official, 'song_official' : song_official, 'lyric_official' : lyric_official, 'albumart_official' : albumart_official} #info링크는 더이상 필요없으므로 삭제
    return render (request, 'musictest/new7_write.html', context)
    
@login_required
def write_B(request):
    artist_official = request.POST['artist_official']
    music_official = request.POST['music_official']
    album_official = request.POST['album_official']
    lyric_official = request.POST['lyric_official']
    albumart_official = request.POST['albumart_official']
    song_official = f'./songs/{artist_official}-{music_official}.mp3'
    #사용자가 적은 타이틀 저장
    title = request.POST['title']
    context = {'artist_official':artist_official, 'music_official' : music_official, 'album_official' : album_official, 'song_official' : song_official, 'lyric_official' : lyric_official, 'albumart_official' : albumart_official, 
                'title':title} 
    return render (request, 'musictest/new8_write.html', context)
    
@login_required
def write_C(request):
    artist_official = request.POST['artist_official']
    music_official = request.POST['music_official']
    album_official = request.POST['album_official']
    lyric_official = request.POST['lyric_official']
    albumart_official = request.POST['albumart_official']
    song_official = f'./songs/{artist_official}-{music_official}.mp3'
    title = request.POST['title']
    #사용자가 적은 태그 저장
    tag = request.POST['tag']
    context = {'artist_official':artist_official, 'music_official' : music_official, 'album_official' : album_official, 'song_official' : song_official, 'lyric_official' : lyric_official, 'albumart_official' : albumart_official, 
                    'title':title, 'tag':tag} 
    return render (request, 'musictest/new9_write.html', context)

@login_required
def create_musiary(request):
    user = request.user
    artist_official = request.POST['artist_official']
    music_official = request.POST['music_official']
    album_official = request.POST['album_official']
    lyric_official = request.POST['lyric_official']
    albumart_official = request.POST['albumart_official']
    song_official = f'./songs/{artist_official}-{music_official}.mp3'
    title = request.POST['title']
    #사용자가 적은 태그 저장
    tag = request.POST['tag']
    body = request.POST['body']
    post = Post(user=user, artist_official=artist_official, music_official=music_official, album_official = album_official, lyric_official = lyric_official, albumart_official = albumart_official,
                song_official = song_official, title = title, tag=tag, body=body, created_at=timezone.now() )#post에 저장
    post.save()
    return redirect('musictest:detail', post_id=post.id)

@login_required
def detail_test(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'musictest/detail_test.html', context)

# Profile 
def profile(request, username):
    post_id = request.user
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    context = { 'posts' : posts }
    return render(request, 'musictest/profile.html', context)

# My Page
@login_required
def mypage(request):
    post_id = request.user
    posts = Post.objects.filter(user=post_id)
    context = { 'posts' : posts }
    return render(request, 'musictest/mypage.html', context)


# Follower/Following
def followers(request, post_id):
    post_id = request.user
    if request.method == 'POST':
        try:
            posts = Post.objects.filter(user=post_id)
            
            if request.user in posts.followers.all():
                posts.followers.remove(request.user)
            else:
                posts.followers.add(request.user)
                
            return redirect('musictest:profile')
        except Post.DoesNotExist:
            pass
        
    return redirect('musictest:profile')
