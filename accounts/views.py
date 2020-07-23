from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def sign_up(request):
    context={}
    #POST 방식으로 request 들어왔을 경우
    if request.method == 'POST':
        if (request.POST['username'] and
                request.POST['password'] and
                request.POST['password'] == request.POST['password_check']):
                    
            # if request.POST['username'] is not None:
            #     context['error']='이미 존재하는 아이디입니다'
            
            # else:
                new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                )
            
                auth.login(request, new_user)
                return redirect('musictest:index')
        
        else:
            context['error']='아이디와 비밀번호를 다시 확인해주세영'
            
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