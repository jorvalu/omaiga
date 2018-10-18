"""aggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from registration.views import SignUpView, SignUpActivationSentView, SignUpActivationView, ProfileView
from registration.views import EmailChangeView, EmailChangeActivationSentView, EmailChangeActivationView
from links.views import LinkListView, LinkDetailView, LinkCreateView, LinkUpdateView, LinkDeleteView, VoteView
from comments.views import CommentCreateView, CommentDeleteView, PointView

urlpatterns = [

    # admin
    path('admin/', admin.site.urls),

    # auth
    path('accounts/', include('django.contrib.auth.urls')),

    # signup
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/activation_sent/', SignUpActivationSentView.as_view(), name='signup_activation_sent'),
    path('accounts/signup/activation/<uidb64>/<token>/', SignUpActivationView.as_view(), name='signup_activation'),

    # email_change
    path('accounts/email_change/', EmailChangeView.as_view(), name='email_change'),
    path('accounts/email_change/activation_sent/', EmailChangeActivationSentView.as_view(), name='email_change_activation_sent'),
    path('accounts/email_change/activation/<uidb64>/<token>/<email_token>', EmailChangeActivationView.as_view(), name='email_change_activation'),

    # profile
    path('accounts/profile/', ProfileView.as_view(), name='profile'),

    # links app
    path('', LinkListView.as_view(), name='link_list'),
    path('link_create/', LinkCreateView.as_view(), name='link_create'),
    path('link_detail/<pk>', LinkDetailView.as_view(), name='link_detail'),
    path('link_update/<pk>', LinkUpdateView.as_view(), name='link_update'),
    path('link_delete/<pk>', LinkDeleteView.as_view(), name='link_delete'),

    # voting app
    path('vote/<pk>', VoteView.as_view(), name='vote'),

    # comments app
    path('link_detail/<pk>/comment', CommentCreateView.as_view(), name='comment_create'),
    path('link_detail/<id>/comment/delete/<pk>', CommentDeleteView.as_view(), name='comment_delete'),
    path('link_detail/comment/point/<pk>/', PointView.as_view(), name='point'),

]
