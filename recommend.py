import streamlit as st
import pickle
import pandas as pd


# page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("https://cdn.pixabay.com/photo/2019/11/11/10/05/law-4617873_1280.jpg");
#     background-size: cover;
#     }
#     </style>
#     '''
# st.markdown(page_bg_img, unsafe_allow_html=True)

article_dict=pickle.load(open("article_dict.pkl","rb"))
articles=pd.DataFrame(article_dict)

st.title("Article Recommender System")

select_article_heading= st.selectbox(
     'Heading Of The Article!',
     articles["heading"].values)

similarity=pickle.load(open("similarity.pkl","rb"))

def recommend(article):
    article_index=articles[articles["heading"]==article].index[0]
    distances=similarity[article_index]
    article_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_articles=[]
    for i in article_list:
        recommended_articles.append(articles.iloc[i[0]].heading)
        recommended_articles.append(articles.iloc[i[0]].article_link)
    return recommended_articles


if st.button("Recommend"):
     recommendations=recommend(select_article_heading)
     for i in recommendations:
          st.write(i)
# def recommendation_pg():
#     import streamlit as st
#     import time
#     import numpy as np

#     st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    
# page_names_to_funcs = {
#     "—": intro,
#     "Plotting Demo": recommendation_pg,
  
# }

# demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
# page_names_to_funcs[demo_name]()