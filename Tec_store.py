import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
import google.generativeai as genai
import pandas as pd
with st.sidebar:
    st.header('⚙️ Response Settings')
    tones = ['Formal', 'Friendly', 'Creative']
    tone = st.radio('Choose tone:', tones)
    levels = ['Low details', 'Medium details', 'High details']
    level = st.select_slider('Choose details level:', levels)
genai.configure(api_key='AIzaSyD1PFNZsNHW37dp2E7zBaqGtVcDqf8Rwnc')
ai_model = genai.GenerativeModel('gemini-2.5-flash')
tab1, tab2 = st.tabs(['🚘 laptop Price Prediction', '🤖 AI laptop Assistant'])
with tab1:
    df = pd.read_csv('laptops.csv')
    df = df.drop(['Unnamed: 0', 'City', 'Color'], axis=1)
    with st.expander('View dataset:'):
        st.dataframe(df.head())
    st.subheader('Enter laptop details:')
    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox('Brand:', df['Brand'].unique())
        filtered_df = df[df['Brand']==brand]
        model = st.selectbox('Model:', filtered_df['Model'].unique())
        body = st.selectbox('Body:', df['Body'].unique())
        year = st.slider('Year', min_value=1975, max_value=2024)
    with col2:
        transmission = st.selectbox('Transmission:', df['Transmission'].unique())
        fuel = st.selectbox('Fuel:', df['Fule'].unique())
        km_driven = st.number_input('KM driven:', min_value=1, step=1)
        engine_cc = st.select_slider('CC:', [800, 1000, 1200, 1400, 1600, 2000])
    df.loc[len(df.index)] = [brand, model, body, transmission,
                            year, fuel, engine_cc, km_driven, 0]
    encoder = LabelEncoder()
    for column in df.select_dtypes(include='object'):
        df[column] = encoder.fit_transform(df[column])
    features = df.drop('Price', axis=1)
    target = df['Price']
    model = LinearRegression()
    model.fit(features[:-1], target[:-1])
    user_input = features.tail(1)
    if st.button('Predict car price:'):
        prediction = model.predict(user_input)
        st.subheader(f'Predicted Price = {prediction[0]:.2f} EGP')
with tab2:
    st.title('🤖 AI Car Assitant')
    st.caption('Here, you can ask anything questions in cars field.')
    user_question = st.chat_input('Ask me anything about cars ...')
    if user_question:
        with st.chat_message('user'):
            st.write(user_question)
        prompt = f'''
        Answer the following car-related question:
        {user_question}
        With {tone} tone and {level} level.
        If the user asked you anything irrelevant to cars field,
        answer it with: (Sorry, I can assist you in cars field only.)
        '''
        with st.chat_message('assistant'):
            with st.spinner('Generating answer...'):
                answer = ai_model.generate_content(prompt)
                st.write(answer.text)
