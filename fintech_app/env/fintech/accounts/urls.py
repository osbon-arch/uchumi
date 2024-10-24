from django.urls import path
from . import views
from .views import landing_page,savings_overview, add_transaction, delete_transaction, community_list, join_community, add_community


urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create-group/', views.create_group_view, name='create_group'),
    path('groups/', views.group_list_view, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail_view, name='group_detail'),
    path('landing', views.landing_page_view, name='landing'),
    path('groups/<int:group_id>/contribute/', views.contribute_to_group_view, name='contribute_to_group'),
    path('groups/<int:group_id>/contributions/', views.group_contributions_view, name='group_contributions'),
    path('groups/<int:group_id>/payout/', views.payout_view, name='payout'),
    path('financial-literacy/', views.financial_literacy_view, name='financial_literacy'),
    path('articles/', views.article_list_view, name='article_list'),
    path('articles/create/', views.article_create_view, name='article_create'),
    path('videos/', views.video_list_view, name='video_list'),
    path('videos/create/', views.video_create_view, name='video_create'),
    path('quizzes/', views.quiz_list_view, name='quiz_list'),
    path('quizzes/create/', views.quiz_create_view, name='quiz_create'),
    path('', views.landing_page, name='landing_page'),
    path('savings/', savings_overview, name='savings_overview'),
    path('savings/add/', add_transaction, name='add_transaction'),
    path('savings/delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
    path('communities/', community_list, name='community_list'),  # Change this line
    path('communities/join/<int:community_id>/', join_community, name='join_community'),
    path('communities/add/', add_community, name='add_community'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('news/', views.news_feed, name='news_feed'),


    
  

]
