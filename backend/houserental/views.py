import json
import os

from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.conf import settings

from houserental.couchdb_connector import connect_to_db

# from houserental.lda import preprocess_text, LDA_100, draw_word_cloud

from houserental.sentiment import get_sentiment_polarity
from houserental.models import count_dict


# Create your views here.
design_doc = settings.COUDB_DOC


@csrf_exempt
@api_view(['GET'])
def low_income_mean(request, name):
    # if request.method == 'POST':
    #     data = request.POST.get('name')
    response = JsonResponse({'result': {"location_name": name, "low_income_mean": 0.12}})
    return response


@csrf_exempt
@api_view(['GET'])
def location_rent(request, name):
    db = connect_to_db('rent_cities')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def location_income(request, name):
    db = connect_to_db('income_cities')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def location_deposit(request, name):
    db = connect_to_db('mortgage_cities')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def location_unemploy(request, name):
    db = connect_to_db('unemploy_cities')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def location_sentiment(request, name):
    db = connect_to_db('twitter')
    result = db.view('_design/location_sentiment/_view/by_city/', group=True, params={'stale': 'ok'}, index='location')
    response = JsonResponse({'content': {}})
    for row in result:
        if row.key is not None and row.key == name:
            if isinstance(row.value, float):
                print('index building')
                # response = JsonResponse({'content': row.value})
            else:
                response = JsonResponse({'content': row.value.get[name]})
            break
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def num_tweet_per_month(request):
    db = connect_to_db('twitter')
    result = db.view('_design/rent_tweets_num/_view/tweets_by_month/', group=True, params={'stale': 'ok'}, index='text')
    result_dict = {}
    for row in result:
        if row.key is not None:
            result_dict['-'.join(str(part) for part in row.key)] = row.value
    response = JsonResponse({'content': result_dict})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


# @csrf_exempt
# @api_view(['GET'])
# def mastodon_lda(request):
#     db = connect_to_db('mastodon_au_rents')
#     result = db.view('_design/mastodon_rent/_view/recent100/', descending=True, limit=100, index='created_at')
#     result_list = []
#     for row in result:
#         if row.key is not None:
#             result_list.append(row.value)
#     print(result_list)
#     preprocessed_documents = [preprocess_text(doc) for doc in result_list]
#     lda_topics = LDA_100(preprocessed_documents)
#     response = JsonResponse({'content': lda_topics})
#     response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
#     return response


@csrf_exempt
@api_view(['GET'])
def state_rent(request, name):
    db = connect_to_db('rent_by_state')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def state_income(request, name):
    db = connect_to_db('income_by_state')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def state_deposit(request, name):
    db = connect_to_db('mortgage_by_state')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def state_unemploy(request, name):
    db = connect_to_db('unemploy_by_state')
    result = db.view('_design/location_rent/_view/by_city/', key=name)
    response = JsonResponse({'content': {}})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def mastodon_sentiment(request):
    db = connect_to_db('mastodon_au')
    result = db.view('_design/sentiment/_view/by_content/', index='text')
    for row in result:
        if row.value is not None:
            polarity = get_sentiment_polarity(row.value)
            if polarity > 0:
                count_dict["positive"] += 1
            elif polarity < 0:
                count_dict["negative"] += 1
            else:
                count_dict["neutral"] += 1
    response = JsonResponse({'content': count_dict})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


@csrf_exempt
@api_view(['GET'])
def twitter_sentiment(request, name):
    db = connect_to_db('twitter')
    result = db.view('_design/sentiment_map_reduce/_view/sentiment_distribution/', key=name)
    response = JsonResponse({'content': count_dict})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response


# @csrf_exempt
# @api_view(['GET'])
# def twitter_word_cloud(request, name):
#     db = connect_to_db('twitter')
#     result = db.view('_design/sentiment_lda/_view/by_rent/', key=name, index='text')
#     result_list = []
#     for row in result:
#         if row.value is not None:
#             print(row.value)
#             result_list.append(row.value)
#     preprocessed_documents = [preprocess_text(doc) for doc in result_list]
#     lda_topics = LDA_100(preprocessed_documents)
#     image_data_generator = draw_word_cloud(lda_topics)
#     image_data = next(image_data_generator)
#     response = HttpResponse(content_type='image/png')
#     response.write(image_data)
#     return response


@csrf_exempt
@api_view(['GET'])
def twitter_created_time(request, name):
    db = connect_to_db('twitter')
    result = db.view('_design/tweets_in_hour/_view/by_rent/', key=name, index='text')
    response = JsonResponse({'content': count_dict})
    for row in result:
        if row.value is not None:
            response = JsonResponse({'content': row.value})
    response["Access-Control-Allow-Origin"] = 'http://172.26.134.0:3000'
    return response