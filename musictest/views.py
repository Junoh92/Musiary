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


def index(request):
    print (' api  호출호출')
    dog_api_response=requests.get('https://dog.ceo/api/breeds/image/random')
    print (dog_api_response)
    dog_api_response_dictionary = dog_api_response.json()
    posts = Post.objects.all()
    dog=None
    if dog_api_response_dictionary['status']=='success':
        dog = dog_api_response_dictionary['message']
    context = {'posts': posts,
               'dog': dog}
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
