import streamlit as st

st.set_page_config(
    page_title="Instructions",
    page_icon="📝"
)

custom_css = """
    <style>
        .appview-container {
            background-color: #F1EAFF;
        }
        .st-emotion-cache-18ni7ap {
            background-color: #D0A2F7;
        }
        .st-emotion-cache-6qob1r {
            background-color: #E5D4FF;
        }
        .stMarkdown h1 {
            text-align: center;
            font-size: 60px;
            color: #7743DB;  
            margin-bottom: 20px;
        }
        .st-ak {
            background-color: #E5D4FF;
        }
        .css-16idsys{
            font-size: 24px;
        }
        .box {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: #E5D4FF; 
            font-family: 'Arial', sans-serif;
        }
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .heading {
            text-align: center;
        }
        .css-6qob1r {
            background-color: #E5D4FF;
        }
        .st-bf{
            background-color: #E5D4FF;
        }
        .st-bd{
            background-color: #E5D4FF;
        }
        .st-cx{
            background-color: #E5D4FF;
        }
        .css-10trblm {
            margin-top: 20px;
            color: #7743DB; 
        }
        .stButton {
            font-size: 40px; 
            color: black; 
            margin-top: 10px;
            cursor: pointer;
        }
        .st-emotion-cache-5rimss p {
            font-size: 18px;
        }
        p{
            font-size: 15px;
        }
        .plot-container {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #f8f8f8;
        }
        .st-emotion-cache-10trblm{
            margin-top: 20px;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title('Instructions')
st.write('Disclaimer: The information provided on this website pertains specifically to flats and apartments in Gurgaon and may not accurately reflect property prices in other cities.')

st.header('This webapp has 4 modules')

st.subheader('Module1: Predict')
st.write("""
If you provide accurate and relevant input features for predicting 
the price of a house, the model can generate a more reliable output. 
Ensuring that the features are correct and representative of the property's 
characteristics will contribute to a more accurate prediction.
Once the prices are predicted, societies having flats in those price ranges
at minimum price per unit area is recommended to the user.
""")


st.subheader('Module2: Recommendations')
st.write("""
There are two types of recommendations based upon preferences of user.
User may choose his/her favourite society name(Society Name Based) and the underlying model
will recommend the user with 6 similar such societies.

The Nearby Location based recommendations are useful if one wants a society in the vicinity
of a particular location(like 10 km from Airport etc.)

Note: Similarity is based on location of that society, how costly that society is and some other
details about the societies.
""")


st.subheader('Module3: Visualize')
st.write("""
Several visual plots like how much the flats in each sectors costs on an average, how prices vary
with different features and combination of features are being mentioned here. The user can gain
deep insights about how prices of flats vary with changing features.
""")


st.subheader('Module4: Insights')
st.write("""
This module enables user to gain exact numerical insights about how much price will
vary if one of the features are changed keeping rest of them as constant. This is based on 
an inference model.
""")
