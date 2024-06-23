from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.get_all_posts, name='all-posts'),
    path("register/", views.register_request, name="register"),
    path("login/", views.ulogin, name="login"),
    path('logout/', views.log_out, name='logout'),
    path("password-change/", views.password_change, name="password-change"),
    path("password-reset-request/", views.password_reset_request,
         name="password-reset-request"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm,
         name='password-reset-confirm'),
    path('change-password/', views.change_password, name='change-password'),
    path('password-change-done/', views.password_change_done,
         name='password-change-done'),
    path('invalid-login/', views.invalid_login, name='invalid-login'),
    path('post-cat/<str:category>',
         views.get_all_posts_category, name='all-posts_cat'),
    path('post/<slug:slug>', views.single_post, name='single-post'),
    path('tag/<str:tag_title>/', views.posts_by_tag, name='post-by-tag'),
    path('new-post/', views.NewPostView.as_view(), name='new-post'),
    path('post-edit/<int:post_id>', views.EditPostView.as_view(), name='post-edit'),
    path('new-post-success/<str:action_mode>',
         views.new_post_success, name='new-post-success'),
    path('top-rated-posts/', views.top_rated_posts, name='top-rated-posts'),
    path('read-later-posts/', views.ReadLaterView.as_view(),
         name='read-later-posts'),
    path('post-dashboard/', views.dashboard_view, name='post-dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('account-activation-sent/', views.account_activation_sent,
         name='account-activation-sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account-activaion-complete/', views.account_activation_complete,
         name='account-activation-complete'),

]
