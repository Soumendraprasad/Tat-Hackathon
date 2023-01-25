
import streamlit as st
import pandas as pd

import pickle


page_bg_img = '''
    <style>
    .stApp {
    background-image: url("https://cdn.pixabay.com/photo/2019/11/11/10/05/law-4617873_1280.jpg");
    background-size: cover;
    }
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
    """Justice Through AI"""
    st.title("Justice Through AI")

    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")
    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))    
            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task",["Recommend","Analytics","Profiles"])
                if task == "Recommend":
                    st.subheader("Get Article Recommendation")
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
                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
                else:
                    st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

                



                    

	# # 			elif task == "Analytics":
	# # 				st.subheader("Analytics")
	# 			elif task == "Profiles":
	# 				st.subheader("User Profiles")
	# 				user_result = view_all_users()
	# 				clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
	# 				st.dataframe(clean_db)
	# 		else:
	# 			st.warning("Incorrect Username/Password")

	# elif choice == "SignUp":
	# 	st.subheader("Create New Account")
	# 	new_user = st.text_input("Username")
	# 	new_password = st.text_input("Password",type='password')

	# 	if st.button("Signup"):
	# 		create_usertable()
	# 		add_userdata(new_user,make_hashes(new_password))
	# 		st.success("You have successfully created a valid Account")
	# 		st.info("Go to Login Menu to login")