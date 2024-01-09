import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="Predict",
    page_icon="🏨",
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
        img{
            height: 150px;
            width: 100%;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title('Predict the Price of Your Dream Flats Here')

data = pd.read_csv('./flat_price_prediction_data.csv')
flats_data = pd.read_csv('./flats.csv')
col1, col2 = st.columns(2)

with col1:
    unique_sectors = data['sector'].unique().tolist()
    sector = st.selectbox('Select sector', unique_sectors)

with col2:
    unique_age_group = data['age_group'].unique().tolist()
    age_group = st.selectbox('Pick the age category for the house', unique_age_group)

col1, col2, col3 = st.columns(3)

with col1:
    unique_num_bedrooms = data['num_bedrooms']
    num_bedrooms = st.text_input('Number of bedrooms', placeholder="Enter number of bedrooms")

with col2:
    unique_num_bathrooms = data['num_bathrooms']
    num_bathrooms = st.text_input('Number of bathrooms', placeholder="Enter number of bathrooms")

with col3:
    unique_num_balconies = data['num_balconies']
    num_balconies = st.text_input('Number of balconies', placeholder="Enter number of balconies")

col1, col2 = st.columns(2)

with col1:
    super_built_up_area = st.number_input('Super Built Up Area')

with col2:
    floor_number = st.text_input('Floor Number', placeholder="Enter floor number")

furnished = st.selectbox('Do you want the room to be furnished?', ['No', 'Yes'])

if furnished == 'Yes':
    with st.expander("Click here to fill additional furnishing details"):
        ac = st.text_input('How many ACs do you want', placeholder='Enter number of ACs')
        geyser = st.text_input('How many geysers do you want', placeholder='Enter number of geysers')
        fan = st.text_input('How many fans do you want', placeholder='Enter number of fans')
        light = st.text_input('How many lights do you want', placeholder='Enter number of lights')
        wardrobe = st.text_input('How many wardrobe do you want', placeholder='Enter number of wardrobe')

col1, col2, col3, col4 = st.columns(4)

with col1:
    store_room = st.selectbox('Store room needed', ['No', 'Yes'])
with col2:
    pooja_room = st.selectbox('Pooja room needed', ['No', 'Yes'])
with col3:
    study_room = st.selectbox('Study room needed', ['No', 'Yes'])
with col4:
    servant_room = st.selectbox('Servant room needed', ['No', 'Yes'])


if servant_room == 'Yes':
    separate_entry = st.selectbox('Do you want a separate entry for servant room', ['Yes', 'No'])
else:
    separate_entry = 0

st.subheader("Do you want the following additional features:")
col1, col2, col3 = st.columns(3)

with col1:
    spacious_interiors = st.selectbox("Spacious Interiors", ['No', 'Yes'])

with col2:
    centrally_air_conditioned = st.selectbox("Centrally Air Conditioned", ['No', 'Yes'])

with col3:
    false_ceiling = st.selectbox("False Ceiling", ['No', 'Yes'])


col1, col2, col3 = st.columns(3)

with col1:
    swimming_pool = st.selectbox("Swimming Pool", ['No', 'Yes'])

with col2:
    club_house = st.selectbox("Community Centre", ['No', 'Yes'])

with col3:
    intercom = st.selectbox("Intercom Facility", ['No', 'Yes'])


col1, col2, col3 = st.columns(3)

with col1:
    private_garden = st.selectbox("Private Garden/Terrace", ['No', 'Yes'])

with col2:
    low_density_society = st.selectbox("Low Density Society", ['No', 'Yes'])

with col3:
    piped_gas = st.selectbox("Piped Gas", ['No', 'Yes'])


def encode(val):
    if val == 'No':
        return 0
    else:
        return 1


def convert_rupees_to_words(rupees):
    if rupees < 1:
        return str(round(rupees * 100, 2)) + ' Lakhs'
    else:
        return str(round(rupees, 2)) + ' Crore'


def get_price(price):
    try:
        price_value = price.split()[0]
        if 'Crore' in price:
            return round(float(price_value), 2)
        elif 'Lac' in price:
            return round(float(price_value) / 100, 2)
    except AttributeError:
        return np.nan


def get_society(society):
    try:
        return society[:-5] if '★' in society else society
    except AttributeError:
        return society


if st.button('Predict Price'):
    total_num_rooms = 0
    show_result = True
    try:
        num_bedrooms = int(num_bedrooms)
        num_bathrooms = int(num_bathrooms)
        num_balconies = int(num_balconies)
        floor_number = int(floor_number)
        store_room = encode(store_room)
        study_room = encode(study_room)
        pooja_room = encode(pooja_room)
        servant_room = encode(servant_room)

        total_num_rooms = num_bedrooms + num_bathrooms + num_balconies + store_room + study_room + pooja_room + servant_room
    except ValueError:
        show_result = False
        st.error('Please enter all the number of rooms properly.')

    furnished = encode(furnished)
    try:
        ac = int(ac) if furnished == 1 else 0
        geyser = int(geyser) if furnished == 1 else 0
        fan = int(fan) if furnished == 1 else 0
        light = int(light) if furnished == 1 else 0
        wardrobe = int(wardrobe) if furnished == 1 else 0
    except ValueError:
        show_result = False
        st.error('Please enter all furnishing details details properly.')

    separate_entry = 0 if servant_room == 0 else encode(separate_entry)
    spacious_interiors = encode(spacious_interiors)
    centrally_air_conditioned = encode(centrally_air_conditioned)
    false_ceiling = encode(false_ceiling)
    swimming_pool = encode(swimming_pool)
    club_house = encode(club_house)
    intercom = encode(intercom)
    private_garden = encode(private_garden)
    low_density_society = encode(low_density_society)
    piped_gas = encode(piped_gas)

    if show_result:
        pipe = joblib.load('./flat_pipeline.joblib')
        input_data = np.array([
            sector,
            num_bedrooms,
            num_bathrooms,
            num_balconies,
            age_group,
            super_built_up_area,
            floor_number,
            servant_room,
            furnished,
            centrally_air_conditioned,
            false_ceiling,
            intercom,
            private_garden,
            separate_entry,
            spacious_interiors,
            swimming_pool,
            club_house,
            piped_gas,
            ac,
            geyser,
            fan,
            wardrobe,
            light,
            low_density_society,
            total_num_rooms
        ])
        input_data = pd.DataFrame(input_data.reshape(1, -1), columns=data.columns[:-1])
        transformer = joblib.load('./y_transformer.joblib')
        predicted_price = transformer.inverse_transform(pipe.predict(input_data).reshape(1, -1))[0][0]
        max_price = max(data['price'])
        tolerance_ratio = predicted_price / max_price

        # mean absolute error was of 25 L
        lower_limit = convert_rupees_to_words(predicted_price - tolerance_ratio * 0.25)
        upper_limit = convert_rupees_to_words(predicted_price + tolerance_ratio * 0.25)
        st.info(f'You may expect your flat to fall within the range of {lower_limit} to {upper_limit}.')

        society_images = joblib.load('./flats_data_society_images.joblib')

        price_series = flats_data['price'].apply(get_price)
        filtered_flats = flats_data[((price_series > predicted_price - tolerance_ratio * 0.25) & (price_series < predicted_price + tolerance_ratio * 0.25))].sort_values('area').reset_index(drop=True)
        filtered_societies = []
        filtered_links = []
        societies_taken = []
        for i in range(filtered_flats.shape[0]):
            society_name = filtered_flats['society'][i]
            link = filtered_flats['link'][i]
            if society_name not in societies_taken:
                filtered_societies.append(get_society(society_name))
                filtered_links.append(link)
                societies_taken.append(society_name)
                if len(filtered_societies) == 3:
                    break

        if filtered_flats.shape[0] < 2:
            st.warning('There are no such flats in such price range')
        elif filtered_flats.shape[0] == 2:
            col1, col2 = st.columns(2)
            with col1:
                society_name = filtered_societies[0]
                image_url = society_images[society_name]
                redirect_url = filtered_links[0]
                st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
            with col2:
                society_name = filtered_societies[1]
                image_url = society_images[society_name]
                redirect_url = filtered_links[1]
                st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
        elif filtered_flats.shape[0] > 2:
            col1, col2, col3 = st.columns(3)
            with col1:
                society_name = filtered_societies[0]
                image_url = society_images[society_name]
                redirect_url = filtered_links[0]
                st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
            with col2:
                society_name = filtered_societies[1]
                image_url = society_images[society_name]
                redirect_url = filtered_links[1]
                st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
            with col3:
                society_name = filtered_societies[2]
                image_url = society_images[society_name]
                redirect_url = filtered_links[2]
                st.markdown(f"[![Clickable Image]({image_url})]({redirect_url})", unsafe_allow_html=True)
                st.markdown(f'<p style="text-align: center">{society_name}</p>', unsafe_allow_html=True)
