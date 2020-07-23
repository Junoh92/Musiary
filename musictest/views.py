from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
import requests

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys




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
    music = request.POST['music']
    singer = request.POST['singer']
    tag = request.POST['tag']
    body = request.POST['body']
    post = Post(user=user, image=image, music=music, singer=singer, tag=tag, body=body, created_at=timezone.now())
    post.save()
    return redirect('musictest:detail', post_id=post.id)

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