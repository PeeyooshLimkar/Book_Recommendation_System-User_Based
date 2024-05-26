#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
import numpy as np
import pickle


# In[2]:


popularity_df = pickle.load(open('popularity_df.pkl', 'rb'))
cf = pickle.load(open('cf.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))


# In[3]:


app = Flask(__name__)


# In[4]:


@app.route('/')
def popular_books():
    return render_template('popular_books.html', 
                           book_title = list(popularity_df['book_title'].values),
                           book_author = list(popularity_df['book_author'].values),
                           y_o_p = list(popularity_df['year_of_publication'].values),
                           image = list(popularity_df['image_url_m'].values),
                           votes = list(popularity_df['no_of_ratings'].values),
                           rate = list(round(popularity_df['avg_rating'], 2).values),
                           title = 'Popular Books')


# In[5]:


@app.route('/recommend')
def reccomend():
    return render_template('recommend_books.html')


@app.route('/recommend_books', methods = ['GET', 'POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(cf.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['book_title'] == cf.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('book_title')['image_url_m'].values))
        item.extend(list(temp_df.drop_duplicates('book_title')['book_title'].values))
        item.extend(list(temp_df.drop_duplicates('book_title')['book_author'].values))
        item.extend(list(temp_df.drop_duplicates('book_title')['year_of_publication'].values))
        item.extend(list(temp_df.drop_duplicates('book_title')['no_of_ratings'].values))
        item.extend(list(round(temp_df.drop_duplicates('book_title')['avg_rating'], 2).values))

        data.append(item)

#     print(data)

    return render_template('recommend_books.html', data = data)


# In[6]:


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8501)
# Docker Container Port
