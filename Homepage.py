import streamlit as st

st.set_page_config(page_title="Streamline Estates")


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
            color: #7743DB;  
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
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title('Welcome to Streamline Estates')

# Create a rounded box for the content
st.markdown("""
<div class="box center">
<p>
    Here we redefine your real estate experience with a suite of innovative features. Our platform offers 
    a unique flat price prediction mechanism that leverages key features to 
    provide accurate estimations. The Insights module delivers valuable 
    information on diverse property features, empowering users with comprehensive 
    knowledge to make informed decisions. Immerse yourself in our Visualization module, 
    allowing you to vividly explore and understand different property aspects. 
    Additionally, our platform goes beyond by providing personalized 
    recommendations for various societies, ensuring you find the perfect match for your needs. 
    At Streamline Estates, we're committed to simplifying your real estate journey through 
    cutting-edge technology and insightful solutions.
</p>
</div>
""", unsafe_allow_html=True)
