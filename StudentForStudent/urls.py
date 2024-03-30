"""
URL configuration for StudentForStudent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from S4S import views, DataVisuals,blogim, options,notifcations,comments, user_profile,email,likes,sessions,superusers

urlpatterns = [
    path('', views.home, name=''),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('data/', DataVisuals.display_data, name='data'),
    path('forgotpass/', views.forgotpassword, name='forgotpass'),
    path('admin/', admin.site.urls),
    path('create_post/', blogim.create_post, name='create_post'),
    path('mainforum/', views.mainforum, name='mainforum'),
    path('check_session/', sessions.check_session, name='check_session'),
    path('active_sessions/', sessions.active_sessions, name='active_sessions'),
    path('blog/<int:blog_id>/create_post/', blogim.create_post, name='create_post'),
    path('blog/<int:blog_id>/', blogim.blog_detail, name='blog_detail'),
    path('post/<int:post_id>/delete/', blogim.delete_post, name='delete_post'),
    path('blog/<int:pk>/', blogim.blog_detail, name='blog-detail'),
    path('edit_post/<int:post_id>/', blogim.edit_post, name='edit_post'),
    path('post/<int:post_id>/', blogim.post_detail, name='post_detail'),
    path('delete_comment/<int:comment_id>/', blogim.delete_comment, name='delete_comment'),
    path('Settings/', options.settings, name='settings'),
    path('toggle_dark_mode/', options.toggle_dark_mode, name='toggle_dark_mode'),
    path('notifications/unseen_count/', notifcations.unseen_count, name='unseen_count'),
    path('notifications/mark_seen/<int:notification_id>/', notifcations.mark_notification_seen, name='mark_notification_seen'),
    path('notifications/', notifcations.notifications, name='notifications'),
    path('About_us/', blogim.about_us, name='about_us'),
    path('About_us1/', blogim.about_us1, name='about_us1'),
    path('My_Profile/', user_profile.my_profile, name='My_Profile'),
    path('like_post/<int:post_id>/', likes.like_post, name='like_post'),
    path('sent_test_email/', email.send_test_email, name='send_test_email'),
    path('enter_code/', email.enter_code, name='enter_code'),
    path('superuser_home/', superusers.superuser_home, name='superuser_home'),
    path('edit_comment/<int:comment_id>/', comments.edit_comment, name='edit_comment'),
    path('has_liked_comment/<int:comment_id>/', comments.has_liked_comment, name='has_liked_comment'),
    path('comment_detail/<int:comment_id>/', comments.comment_detail, name='comment_detail'),
    path('manage_users/', superusers.manage_users, name='manage_users'),
    path('delete_user/<int:user_id>/', superusers.delete_user, name='delete_user'),

]
