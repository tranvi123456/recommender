import streamlit as st
import pandas as pd
from pre_process import pre_process
import pickle




df0_1 = pd.read_csv("df0_1.csv")
df0_2 = pd.read_csv("df0_2.csv")
df_user = pd.read_csv("df_user.csv")

# Load models
# import pickle
pkl_tfidf_vectorizer = 'tfidf_vectorizer.pkl'
with open(pkl_tfidf_vectorizer, 'rb') as file_vec:
    tfidf_vectorizer = pickle.load(file_vec)

pkl_tfidf_matrix = 'tfidf_matrix.pkl'
with open(pkl_tfidf_matrix, 'rb') as file_mat:
    tfidf_matrix = pickle.load(file_mat)

pkl_algorithm_model = 'algorithm_model.pkl'
with open(pkl_algorithm_model, 'rb') as file_mod:
    algorithm_model = pickle.load(file_mod)

# GUI
# st.title("Coursera")
menu = ['About Coursera', 'Explore Topics and Skills']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'About Coursera':
    st.image('IMG_6122.png')
    st.write('Coursera is a popular online learning platform founded in 2012 by Andrew Ng and Daphne Koller, both professors from Stanford University. It offers a wide range of online courses, specializations, degrees, and professional certificates from various universities and institutions worldwide')
    st.image('IMG_6119.png')
    st.image('IMG_6121.png') ## https://www.coursera.org/about/partners

    # File paths
    icahn_school_img = 'icahnschool.png'
    iese_school_img = 'ieseschool.png'
    ie_university_img = 'ieuniversity.png'

    # URLs to link to
    icahn_school_url = 'https://icahn.mssm.edu/'
    iese_school_url = 'https://www.iese.edu/'
    ie_university_url = 'https://www.ie.edu/'

    # Function to load images and convert to base64
    def load_image(image_path):
        import base64
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    # Load images
    icahn_school_base64 = load_image(icahn_school_img)
    iese_school_base64 = load_image(iese_school_img)
    ie_university_base64 = load_image(ie_university_img)

    # Display images with links and responsive layout
    st.markdown(
        f"""
        <style>
            .image-container {{
                display: flex;
                justify-content: space-around;
                width: 100%; /* Ensure the container fills the width of the page */
            }}
            .image-container img {{
                width: 33%; /* Each image takes up 30% of the container width */
                height: 200; /* Maintain the aspect ratio */
                object-fit: cover; /* Ensure the images cover the area without stretching */
            }}
        </style>
        <div class="image-container">
            <a href="{icahn_school_url}" target="_blank">
                <img src="data:image/png;base64,{icahn_school_base64}" alt="Icahn School of Medicine" />
            </a>
            <a href="{iese_school_url}" target="_blank">
                <img src="data:image/png;base64,{iese_school_base64}" alt="IESE Business School" />
            </a>
            <a href="{ie_university_url}" target="_blank">
                <img src="data:image/png;base64,{ie_university_base64}" alt="IE University" />
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image('IMG_6120.png')

elif choice == 'Explore Topics and Skills':
    st.subheader("Explore Topics and Skills")
    type = st.radio('',options=["Which courses are suitable for me", "Search courses by course's name", "Search courses by course's content"])
    if type == "Which courses are suitable for me":
        df_sample_user = df_user['UserId'].drop_duplicates().sample(10, random_state=42).sort_values().tolist()
        st.write("##### Please select your ID")
        selected = st.selectbox("Select your ID", df_sample_user)
        st.write("Courses you have studied:")
        studied = df_user[df_user['UserId'] == selected][['CourseName', 'Unit', 'Level']]
        studied = studied.reset_index(drop=True)
        studied

        st.write("Suggested courses:")
        df_score = pd.DataFrame(df0_2['CourseId'])
        df_score['EstimateScore'] = df_score['CourseId'].apply(lambda x: algorithm_model.predict(selected, x).est)
        df_score = df_score.sort_values(by=['EstimateScore'], ascending=False)
        df_score = df_score.drop_duplicates()
        df_score = pd.merge(df_score, df0_2, on='CourseId', how='left')
        df_score = pd.merge(df_score, df0_1, on='CourseName', how='left')
        df_score = df_score[['CourseName', 'Unit', 'Level', 'Description']].head(3)
        card_style = """
        <style>
        .card {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 15px;
            margin: 10px;
            box-shadow: 2px 2px 2px grey;
        }
        </style>
        """
        cols = st.columns(3)
        st.markdown(card_style, unsafe_allow_html=True)
        for i, col in enumerate(cols):
            with col:
                if i < len(df_score):
                    st.markdown(f"""
                    <div class="card">
                        <h3 style='text-align: center;'>{df_score.iloc[i]['CourseName']}</h3>
                        <p><strong>Unit:</strong> {df_score.iloc[i]['Unit']}</p>
                        <p><strong>Level:</strong> {df_score.iloc[i]['Level']}</p>
                        <p><strong>Description:</strong> {df_score.iloc[i]['Description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")

    elif type == "Search courses by course's name":
        df_sample_course = df0_1['CourseName'].sort_values().sample(10, random_state=42).tolist()
        st.write("##### Please select course")
        selected = st.selectbox("Select courses", df_sample_course)
        course1 = df0_1[df0_1['CourseName'] == selected][['CourseName', 'Unit', 'Level', 'Description', 'ReviewNumber', 'AvgStar']]
        for _, course in course1.iterrows():
            st.write(f"Course Name: {course['CourseName']}")
            st.write(f"Unit: {course['Unit']}")
            st.write(f"Level: {course['Level']}")
            st.write(f"Description: {course['Description']}")
            st.write("---")

        st.write("Suggested courses:")
        test_df = pd.DataFrame({'products': [selected]})
        test_df['products'] = test_df['products'].apply(pre_process)
        test_tfidf = tfidf_vectorizer.transform(test_df['products'])
        cosine_similarities = cosine_similarity(test_tfidf, tfidf_matrix)
        sus = pd.DataFrame(cosine_similarities)
        suggestions = sus.transpose().reset_index(drop=True)
        suggestions = suggestions.rename(columns={0: 'Similar'})
        suggestions = suggestions.nlargest(3, 'Similar')
        suggestions = suggestions.reset_index()
        suggestions = suggestions.rename(columns={'index': 'CourseID'})
        suggestions = pd.merge(suggestions, df0_1, on='CourseID', how='left')
        suggestions = suggestions[['CourseName', 'Unit', 'Level', 'Description']].head(3)
        card_style = """
        <style>
        .card {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 15px;
            margin: 10px;
            box-shadow: 2px 2px 2px grey;
        }
        </style>
        """
        cols = st.columns(3)
        st.markdown(card_style, unsafe_allow_html=True)
        for i, col in enumerate(cols):
            with col:
                if i < len(suggestions):
                    st.markdown(f"""
                    <div class="card">
                        <h3 style='text-align: center;'>{suggestions.iloc[i]['CourseName']}</h3>
                        <p><strong>Unit:</strong> {suggestions.iloc[i]['Unit']}</p>
                        <p><strong>Level:</strong> {suggestions.iloc[i]['Level']}</p>
                        <p><strong>Description:</strong> {suggestions.iloc[i]['Description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")


    elif type == "Search courses by course's content":
        st.write("##### Search courses by content")
        find_text = st.text_input('Enter content of courses')
        if st.button('Get Suggestions'):
            test_df = pd.DataFrame({'products': [find_text]})
            test_df['products'] = test_df['products'].apply(pre_process)
            test_tfidf = tfidf_vectorizer.transform(test_df['products'])
            cosine_similarities = cosine_similarity(test_tfidf, tfidf_matrix)
            sus = pd.DataFrame(cosine_similarities)
            suggestions = sus.transpose().reset_index(drop=True)
            suggestions = suggestions.rename(columns={0: 'Similar'})
            suggestions = suggestions.nlargest(3, 'Similar')
            suggestions = suggestions.reset_index()
            suggestions = suggestions.rename(columns={'index': 'CourseID'})
            suggestions = pd.merge(suggestions, df0_1, on='CourseID', how='left')
            suggestions = suggestions[['CourseName', 'Unit', 'Level', 'Description']].head(3)

            card_style = """
            <style>
            .card {
                border-radius: 8px;
                border: 1px solid #ccc;
                padding: 15px;
                margin: 10px;
                box-shadow: 2px 2px 2px grey;
            }
            </style>
            """
            cols = st.columns(3)
            st.markdown(card_style, unsafe_allow_html=True)
            for i, col in enumerate(cols):
                with col:
                    if i < len(suggestions):
                        st.markdown(f"""
                        <div class="card">
                            <h3 style='text-align: center;'>{suggestions.iloc[i]['CourseName']}</h3>
                            <p><strong>Unit:</strong> {suggestions.iloc[i]['Unit']}</p>
                            <p><strong>Level:</strong> {suggestions.iloc[i]['Level']}</p>
                            <p><strong>Description:</strong> {suggestions.iloc[i]['Description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("")


