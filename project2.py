import streamlit as st
import pandas as pd
import pickle
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns
from PIL import Image
import os
import base64

# # Load models 
# # import pickle
# pkl_filename = 'SVD_model_GUI.pkl'
# with open(pkl_filename, 'rb') as file:  
#     SVD_model_GUI = pickle.load(file)


# find_user_rec = user_recs.filter(user_recs['UserId'] == UserId)
# user = find_user_rec.first()

# lst = []
# for row in user['recommendations']:
#     lst.append((row['CourseId'], row['rating']))
# dic_user_rec = {'UserId' : user.UserId, 'recommendations' :lst}
# dic_user_rec





# def display_course_suggestions():
#     customer_id = st.text_input('Enter Customer ID')
#     if st.button('Get Suggestions'):
#         suggestions = get_course_suggestions(customer_id)
#         if suggestions:
#             st.subheader('Course Suggestions')
#             for course in suggestions:
#                 st.write(course)
#         else:
#             st.write('No suggestions available for this Customer ID.')





# GUI
st.title("Coursera's Recommender System")
menu = ['About Coursera', 'what do you want to learn?']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'About Coursera':
    st.subheader('Courses in Coursera')
    st.markdown('''<a href="https://www.coursera.org" target="_blank">
                    <img src="https://img.icons8.com/ios-filled/50/000000/info.png" style="vertical-align:middle; margin-right:5px"/>
                    For more information, please contact us at this link
                  </a>''', unsafe_allow_html=True)
    st.write('Coursera is a popular online learning platform founded in 2012 by Andrew Ng and Daphne Koller, both professors from Stanford University. It offers a wide range of online courses, specializations, degrees, and professional certificates from various universities and institutions worldwide')
    st.image('course_by_year.png')
    st.image('top10course.png')
    st.image('top10unit.png')

    
    
    
    
    st.markdown('We collaborate with [325+ leading universities and companies](https://www.coursera.org/about/partners).')
    

    # Function to load and encode images
    def load_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string

    # File paths
    icahn_school_img = 'icahnschool.png'
    iese_school_img = 'ieseschool.png'
    ie_university_img = 'ieuniversity.png'

    # URLs to link to
    icahn_school_url = 'https://icahn.mssm.edu/'
    iese_school_url = 'https://www.iese.edu/'
    ie_university_url = 'https://www.ie.edu/'

    # Load images
    icahn_school_base64 = load_image(icahn_school_img)
    iese_school_base64 = load_image(iese_school_img)
    ie_university_base64 = load_image(ie_university_img)

    # Display images with links
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-around;">
            <a href="{icahn_school_url}" target="_blank">
                <img src="data:image/png;base64,{icahn_school_base64}" width="150" />
            </a>
            <a href="{iese_school_url}" target="_blank">
                <img src="data:image/png;base64,{iese_school_base64}" width="150" />
            </a>
            <a href="{ie_university_url}" target="_blank">
                <img src="data:image/png;base64,{ie_university_base64}" width="150" />
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    
              
elif choice == 'what do you want to learn?':
    display_course_suggestions()