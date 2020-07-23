from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post
from django.utils import timezone

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render (request, 'musictest/index.html', context)
    
def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'musictest/detail.html', context)
    
def create(request):
    author = request.POST['author']
    music = request.POST['music']
    singer = request.POST['singer']
    tag = request.POST['tag']
    body = request.POST['body']
    created_at = request.POST['created_at']
    post = Post(author=author, music=music, singer=singer, tag=tag, body=body, created_at=timezone.now())
    post.save()
    return redirect('musictest:detail', post_id=post.id)
    
def new(request):
    return render(request, 'musictest/new.html')

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    context={'post':post}
    return render(request, 'posts/edit.html', context)
    
def update(request, post_id):
    author = request.POST['author']
    music = request.POST['music']
    singer = request.POST['singer']
    tag = request.POST['tag']
    body = request.POST['body']
    created_at = request.POST['created_at']
    post = Post(author=author, music=music, singer=singer, tag=tag, body=body, created_at=timezone.now())
    post.save()
    return redirect('musictest:detail', post_id=post.id)
    
def delete(request, post_id):
    post=Post.objects.get(id=post_id)
    context={'post': post}
    return render(request, 'musictest/delete.html', context)

def realdelete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect(m:index')