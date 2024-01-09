import streamlit as st

st.set_page_config(
    page_title="Insights",
    page_icon="💡"
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

st.title('Gain Some Insights!')

st.write('Enrich your knowledge by gaining insights on how the value of a property changes when we change one of the features, while keeping others constant!')

initial_price = st.number_input('Enter price of your property(in Cr.)')


def convert_rupees_to_words(rupees):
    if rupees < 1:
        return str(round(rupees * 100, 2)) + ' Lakhs'
    else:
        return str(round(rupees, 2)) + ' Crore'


if initial_price != 0:
    st.subheader('Bedroom')

    num_bedrooms = st.slider('How many more bedrooms do you want', 0, 5, 0)

    coefficient_num_bedrooms = 0.114232
    new_price_bedroom = convert_rupees_to_words(initial_price + num_bedrooms * coefficient_num_bedrooms)
    if num_bedrooms != 0:
        st.write(f'The same flat will cost you at {new_price_bedroom }')

    st.subheader('Balcony')
    num_balconies = st.slider('How many more balconies do you want', 0, 4, 0)

    coefficient_num_balconies = 0.063594
    new_price_balcony = convert_rupees_to_words(initial_price + num_balconies * coefficient_num_balconies)
    if num_balconies != 0:
        st.write(f'The same flat will cost you at {new_price_balcony}')

    st.subheader('Floor Number')
    floor_number = st.slider('How many floors higher do you wanna go', 0, 20, 0)

    coefficient_floor_number = 0.062142
    new_price_floor_number = convert_rupees_to_words(initial_price + floor_number * coefficient_floor_number)
    if floor_number != 0:
        st.write(f'The same flat will cost you at {new_price_floor_number}')

    st.subheader('Air Conditioner')
    ac = st.slider('How many more ACs do you want', 0, 20, 0)

    coefficient_ac = 0.044977
    new_price_ac = convert_rupees_to_words(initial_price + ac * coefficient_ac)
    if ac != 0:
        st.write(f'The same flat will cost you at {new_price_ac}')
