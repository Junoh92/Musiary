from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile


# Create your views here.
def sign_up(request):
    context={}
    #POST 방식으로 request 들어왔을 경우
    if request.method == 'POST':
        if (request.POST['username'] and
                request.POST['password'] and
                request.POST['password'] == request.POST['password_check']):
                    
            if User.objects.filter(username = request.POST['username']).exists() == True:
                context['error'] = '아이디가 이미 존재합니다'
                
            else:
                new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                )
                user_img = None
                if 'user_img' in request.FILES:
                    user_img = request.FILES['user_img']
                profile = Profile(user=new_user, name=request.POST['name'], nickname=request.POST['nickname'], email=request.POST['email'], user_img = user_img)
                profile.save()
                auth.login(request, new_user)
                return redirect('musictest:index')
        else:
            context['error']='비밀번호가 맞지 않습니다'
            
    # GET 방식으로 request 들어왔을 경우
    return render(request, 'accounts/sign_up.html', context)
    
def login(request):
    context = {}
        # POST Method
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:

            user = auth.authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )

            if user is not None:
                auth.login(request, user)
                return redirect('musictest:index')
            else:
                context['error'] = '아이디와 비밀번호를 다시 확인해주세영.'

        else:
            context['error'] = '아이디와 비밀번호를 모두 입력해주세영.'

    return render(request, 'accounts/login.html', context)
    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        
        
    return redirect('musictest:index')