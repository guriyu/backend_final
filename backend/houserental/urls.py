from django.urls import path
from .views import *

urlpatterns = [
    path('location_rent/<str:name>/', location_rent, name='location_rent'),
    path('location_income/<str:name>/', location_income, name='location_income'),
    path('location_deposit/<str:name>/', location_deposit, name='location_deposit'),
    path('location_unemploy/<str:name>/', location_unemploy, name='location_unemploy'),
    path('location_sentiment/<str:name>/', location_sentiment, name='location_sentiment'),
    path('num_tweet_per_month/', num_tweet_per_month, name='num_tweet_per_month'),
    # path('mastodon_lda/', mastodon_lda, name='mastodon_lda'),
    path('state_rent/<str:name>/', state_rent, name='state_rent'),
    path('state_income/<str:name>/', state_income, name='state_income'),
    path('state_deposit/<str:name>/', state_deposit, name='state_deposit'),
    path('state_unemploy/<str:name>/', state_unemploy, name='state_unemploy'),
    path('mastodon_sentiment/', mastodon_sentiment, name='mastodon_sentiment'),
    path('twitter_sentiment/<str:name>/', twitter_sentiment, name='twitter_sentiment'),
    # path('twitter_word_cloud/<str:name>/', twitter_word_cloud, name='state_unemploy'),
    path('twitter_created_time/<str:name>/', twitter_created_time, name='twitter_created_time'),
]
