"""djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

import authentication.views
import reviews.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name="login"),
    path('signup/', authentication.views.signup_page, name="signup"),
    path('flow/', reviews.views.flow_page, name="flow"),
    path('my-posts/', reviews.views.my_posts_page, name="my_posts"),
    path('user-follows/', reviews.views.user_follows_page, name="user_follows"),
    path('user-follows/<int:user_follows_id>/delete', reviews.views.delete_user_follows_page, name="user_unfollow"),
    path('review/', reviews.views.create_review_page, name='create_review'),
    path('review/<int:review_id>/update', reviews.views.update_review_page, name="update_review"),
    path('review/<int:review_id>/delete', reviews.views.delete_review_page, name="delete_review"),
    path('ticket/<int:ticket_id>/review/', reviews.views.create_review_page, name="review_ticket"),
    path('ticket/', reviews.views.create_ticket_page, name='create_ticket'),
    path('ticket/<int:ticket_id>/update', reviews.views.update_ticket_page, name="update_ticket"),
    path('ticket/<int:ticket_id>/delete', reviews.views.delete_ticket_page, name="delete_ticket")
]
