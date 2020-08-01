from django.urls import path
from musictest import views

app_name='musictest'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('create/', views.create, name="create"),
    # path('search/', views.search, name='search'),
    path('new/', views.new, name="new"),
    path('<int:post_id>/edit/', views.edit, name='edit'),
    path('<int:post_id>/update/',views.update,name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/realdelete/', views.realdelete, name='realdelete'),
    path('<int:post_id>/like/', views.like, name='like'),
    # path('test/', views.test, name ='test'),
    ]
