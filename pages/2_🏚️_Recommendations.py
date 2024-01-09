import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from sklearn.preprocessing import StandardScaler

st.set_page_config(
    page_title="Recommend",
    page_icon="🏚️",
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
            font-size: 38px;
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
        .st-emotion-cache-1j6rxz7{
            font-size: 15px;
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
        .st-bl{
            font-size: 15px;
        }
        img{
            height: 150px;
            width: 100%;
        }
        .st-ak{
            font-size: 15px;
        }
        #curr{
            height: 200px;
            width: 50%;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title('Society Recommender')

recommendation_type = st.selectbox('Select the type of recommendations you want', ['Choose recommendation type', 'Society Name Based', 'Nearby Location Based'])


recommendation_data = pd.read_csv('./recommendation_data.csv')
society_names = recommendation_data['PropertyName'].tolist()
society_data = pd.read_csv('./societies.csv')
index_ = recommendation_data['PropertyName'].tolist()


sector_columns = ['PropertyName'] + recommendation_data.columns[1: 62 + 1].tolist()
building_details_columns = ['PropertyName'] + recommendation_data.columns[63: 71 + 1].tolist()
nearby_locations_columns = ['PropertyName'] + recommendation_data.columns[72: 784 + 1].tolist()
cost_columns = ['PropertyName', 'remainder__price_per_sqft']
facilities_columns = ['PropertyName'] + recommendation_data.columns[786:].tolist()


def get_similarity(property_name, data, top_n=6):
    data = data.set_index('PropertyName')
    scaler = StandardScaler()
    data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    data.index = index_
    features = data.loc[property_name].values.reshape(1, -1)

    similarities = cosine_similarity(features, data.values)
    return similarities


def get_top_k_similar_societies(property_name, top_n=6):
    sector_similarity = get_similarity(property_name, recommendation_data[sector_columns], top_n)
    building_details_similarity = get_similarity(property_name, recommendation_data[building_details_columns], top_n)
    nearby_locations_similarity = get_similarity(property_name, recommendation_data[nearby_locations_columns], top_n)
    cost_similarity = get_similarity(property_name, recommendation_data[cost_columns], top_n)
    facilities_similarity = get_similarity(property_name, recommendation_data[facilities_columns], top_n)

    sector_weightage = 75
    building_details_weightage = 85
    nearby_locations_weightage = 50
    cost_weightage = 100
    facilities_weightage = 60

    net_similarity = sector_weightage * sector_similarity + \
                     building_details_weightage * building_details_similarity + \
                     nearby_locations_weightage * nearby_locations_similarity + \
                     cost_weightage * cost_similarity + \
                     facilities_weightage * facilities_similarity

    top_indices = net_similarity.argsort()[0][::-1][1:top_n + 1]

    top_similar_flats = recommendation_data.loc[top_indices, 'PropertyName'].tolist()
    return top_similar_flats


def get_societies(nearby_location, radius_):
    column_name = 'remainder__' + nearby_location
    radius_ *= 1000
    return recommendation_data[recommendation_data[column_name] <= radius_]['PropertyName'].values.tolist()


if recommendation_type == 'Nearby Location Based':
    unique_locations = [location.title() for location in joblib.load('./unique_locations.joblib')]
    col1, col2 = st.columns(2)

    with col1:
        location = st.selectbox('Select favourable location', ['Choose Location'] + unique_locations)
    with col2:
        radius = st.number_input('Select radius(in Km)')

    if location != 'Choose Location' and radius != 0:
        societies = get_societies(location.lower(), radius)

        if len(societies) == 0:
            st.info(f'None of the societies are available at a distance of {radius} Km from {location.title()}')
        else:
            st.write(f'We found {len(societies)} society(s) at a distance of {radius} Km from {location.title()}')
            society_name = st.selectbox('Select any society', ['Choose a society'] + sorted(societies))
            if society_name != 'Choose a society':
                society_images = joblib.load('./society_image.joblib')

                image_url = society_images[society_name]

                image_height = 170
                image_width = 200

                st.markdown(
                    f'<div style="display: flex; justify-content: center; align-items: center; height: {image_height}px; width: {image_width}">'
                    f'<img id="curr" src="{image_url}" alt="{society_name}" style="height: {image_height}px; width: {image_width};">'
                    f'</div>'
                    f'<p style="text-align: center">{society_name}</p>',
                    unsafe_allow_html=True
                )

                recommendations = get_top_k_similar_societies(society_name)
                st.subheader('Following are the recommendations: ')

                col1, col2, col3 = st.columns(3)

                with col1:
                    society_name = recommendations[0]
                    image_url = society_images[society_name]
                    redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
                    st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
                with col2:
                    society_name = recommendations[1]
                    image_url = society_images[society_name]
                    redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
                    st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
                with col3:
                    society_name = recommendations[2]
                    image_url = society_images[society_name]
                    redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
                    st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    society_name = recommendations[3]
                    image_url = society_images[society_name]
                    redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
                    st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
                with col2:
                    society_name = recommendations[4]
                    image_url = society_images[society_name]
                    redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
                    st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
                with col3:
                    society_name = recommendations[5]
                    image_url = society_images[society_name]
                    redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
                    st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)

elif recommendation_type == 'Society Name Based':

    society_name = st.selectbox('Select any society', ['Choose a society'] + sorted(society_names))
    if society_name != 'Choose a society':
        society_images = joblib.load('./society_image.joblib')

        image_url = society_images[society_name]
        redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]

        image_height = 170
        image_width = 200

        st.markdown(
            f'<div style="display: flex; justify-content: center; align-items: center; height: {image_height}px; width: {image_width}">'
            f'<img id="curr" src="{image_url}" alt="{society_name}" style="height: {image_height}px; width: {image_width};">'
            f'</div>'
            f'<p style="text-align: center">{society_name}</p>',
            unsafe_allow_html=True
        )

        recommendations = get_top_k_similar_societies(society_name)
        st.subheader('Following are the recommendations: ')

        col1, col2, col3 = st.columns(3)

        with col1:
            society_name = recommendations[0]
            image_url = society_images[society_name]
            redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
            st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
        with col2:
            society_name = recommendations[1]
            image_url = society_images[society_name]
            redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
            st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
        with col3:
            society_name = recommendations[2]
            image_url = society_images[society_name]
            redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
            st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            society_name = recommendations[3]
            image_url = society_images[society_name]
            redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
            st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
        with col2:
            society_name = recommendations[4]
            image_url = society_images[society_name]
            redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
            st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
        with col3:
            society_name = recommendations[5]
            image_url = society_images[society_name]
            redirect_url = society_data[society_data['PropertyName'] == society_name]['Link'].values[0]
            st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
