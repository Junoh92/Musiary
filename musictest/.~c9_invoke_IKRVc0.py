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



# Create your views here.
# def test(request):
#     driver = webdriver.Chrome('chromedriver')
#     driver.get("https://www.youtube.com/")
    
#     time.sleep(3)
    
#     #검색어 창을 찾아 search 변수에 저장
#     search = driver.find_element_by_xpath('//*[@id="search"]')
    
#     #search 변수에 저장된 곳에 값을 전송
#     search.send_keys('반원 코딩')
#     time.sleep(1)
    
#     #search 변수에 저장된 곳에 엔터를 입력
#     search.send_keys(Keys.ENTER)
#     HttpResponse




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
    args = { "no_encode":False, 'output_ext': 'mp3', 'output_file': f'{singer}-{music}.mp3', 'quality': 'best',
             } #검색옵션, 다운로드 mp3형식, 다운로드 파일명은 가수 - 타이틀.mp3
    spotdl_handler = Spotdl(args) #spotdl.handler에 검색옵션 저장
    spotdl_handler.download_track(f'{singer} {music}') #'가수 타이틀' 로 노래 검색 후 다운로드
    tag = request.POST['tag'] 
    body = request.POST['body']
    song = f'/Musiary/{singer}-{music}.mp3'  #song에 받은 파일을 지정해주기
    post = Post(user=user, song=song, image=image,music=music, singer=singer, tag=tag, body=body, created_at=timezone.now())#post에 저장
    post.save()
    # os.remove(f'{singer} - {music}.mp3')
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
