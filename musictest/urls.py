from django.urls import path
from musictest import views

app_name='musictest'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('<int:post_id>/2', views.detail_test, name='detail_test'),
    path('create/', views.create, name="create"),
    # path('search/', views.search, name='search'),
    path('new/', views.new, name="new"),
    path('<int:post_id>/edit/', views.edit, name='edit'),
    path('<int:post_id>/update/',views.update,name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/realdelete/', views.realdelete, name='realdelete'),
    path('<int:post_id>/like/', views.like, name='like'),
    path('music_search/', views.search_A, name='new1_search'),
    path('artist_search/', views.search_B, name='new2_search'),
    path('searching/', views.search_C, name='new3_search'),
    path('search_result/', views.search_D, name='new4_search'),
    path('downloading/', views.search_E_A, name='new5_search'),
    path('downloaded/', views.search_F, name="new6_search"),
    path('write_title/', views.write_A, name="new7_write"),
    path('write_tag/', views.write_B, name="new8_write"),
    path('write_body/', views.write_C, name="new9_write"),
    path('create_musiary/', views.create_musiary, name="create_musiary"),
    
    # path('search_result_b/', views.search_E_B, name='new5_searchB'),
    # path('search_result_c/', views.search_E_C, name='new5_searchC'),
    # path('test/', views.test, name ='test'),
    
    path('profile/<username>/', views.profile, name='profile'),
    path('mypage', views.mypage, name='mypage'),
    path('followers/', views.followers, name='followers'),
    ]
