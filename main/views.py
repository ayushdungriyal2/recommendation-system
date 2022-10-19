from django.shortcuts import render
from django.http import HttpResponse
import pickle
import numpy as np
import os

from django.conf import settings

dir = settings.BASE_DIR


popular_df = pickle.load(open(rf'{dir}\popular.pkl', 'rb'))
pt = pickle.load(open(rf'{dir}\pt.pkl','rb'))
books = pickle.load(open(rf'{dir}\books.pkl','rb'))
similarity_scores = pickle.load(open(rf'{dir}\similarity_scores.pkl','rb'))

book_name = list(popular_df['Book-Title']),
author = list(popular_df['Book-Author']),
image = list(popular_df['Image-URL-M']),
votes = list(popular_df['num_ratings']),
rating = list(popular_df['avg_rating'])

custom_array = list(zip(book_name[0],author[0],image[0]))


def HOME(request):
    if request.method == 'POST':
        user_input = request.POST["name"]
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
        print(similar_items)
        data = []

        r_book_name = []
        r_author = []
        r_image = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            r_book_name.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
            r_author.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
            r_image.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))

        # print(data)
        r_custom_array = list(zip(r_book_name,r_author,r_image))

        context = {"custom_array":custom_array, "data":data,"r_custom_array":r_custom_array, 'x':'x' }

    else:

        context = {"custom_array":custom_array}
        
    
    return render(request, 'index.html', context)