import streamlit as st
import plotly.express as px
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Visualize",
    page_icon="🏘️"
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
        p{
            font-size: 15px;
            text-align: center;
            margin-top: 40px;
        }
        .plot-container {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #f8f8f8;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title('Visualize and gain insights!')

sector_data = pd.read_csv('./sector_data.csv')
data = pd.read_csv('./cleaned_data_v2.csv')

# Plot1 Sectors vs Price/Square Feet
st.write('Sectors v/s Price Per Sqft')

fig = px.scatter_mapbox(sector_data,
                        lat='latitude',
                        lon='longitude',
                        hover_name="sector",
                        hover_data=["price_per_sqft", "super_built_up_area"],
                        color="price_per_sqft",
                        size="super_built_up_area",
                        color_continuous_scale='Viridis',
                        zoom=10,
                        height=300)

fig.update_geos(fitbounds="locations", visible=False)  # Fit the map to the bounds of the markers
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig)


# Plot2 Feature WordCloud
st.write('Feature WordCloud')
wordcloud = joblib.load('./wordcloud.joblib')

# Display Word Cloud using Matplotlib
plt.imshow(wordcloud)
plt.axis('off')  # Turn off axis labels
st.pyplot(plt)  # Display the plot in Streamlit


# Plot3 Area v/s Price
st.write('Area v/s Price')
fig = px.scatter(data, x='super_built_up_area', y='price', color='num_bedrooms',
                 hover_name='society_name', hover_data=['num_bedrooms'],
                 color_continuous_scale='Viridis')
st.plotly_chart(fig)


# Plot 4 Facing v/s Price
st.write('Facing v/s Price')
fig = px.violin(data, x='facing', y='price',
                labels={'price': 'Price'}, color='facing', box=True)
st.plotly_chart(fig)

# Plot 5 Age Group v/s Sector(Price Heatmap)
st.write('Age Group v/s Sector(Price Heatmap)')
median_prices = data.groupby(['sector', 'age_group']).median().reset_index()
top_sectors = data['sector'].value_counts().nlargest(10).index

filtered_data = median_prices[median_prices['sector'].isin(top_sectors)]
fig = px.imshow(filtered_data.pivot('sector', 'age_group', 'price_per_sqft'),
                x=filtered_data['age_group'].unique(),
                y=filtered_data['sector'].unique(),
                labels=dict(color='Median Price/sqft'),
                color_continuous_scale='Viridis')
st.plotly_chart(fig)

st.write('Analyze any of the pair of features')

categorical_columns = ['floor_number', 'servant_room', 'study_room', 'pooja_room',
                       'other_additional_room', 'store_room', 'ac',
                       'bed', 'chimney', 'curtains', 'dining', 'exhaust', 'fan', 'fridge',
                       'geyser', 'light', 'microwave', 'modular', 'sofa', 'stove', 'tv',
                       'wardrobe', 'washing', 'water', 'Airy Rooms', 'Bank Attached Property',
                       'Centrally Air Conditioned', 'Club house / Community Center',
                       'False Ceiling Lighting', 'Feng Shui / Vaastu Compliant',
                       'Fitness Centre / GYM', 'High Ceiling Height', 'Intercom Facility',
                       'Internet/wi-fi connectivity', 'Lift(s)', 'Low Density Society',
                       'Maintenance Staff', 'Natural Light', 'No open drainage around', 'Park','Piped-gas', 'Power Back-up', 'Private Garden / Terrace',
                       'Rain Water Harvesting', 'Recently Renovated', 'Security / Fire Alarm',
                       'Security Personnel', 'Separate entry for servant room',
                       'Shopping Centre', 'Spacious Interiors', 'Swimming Pool',
                       'Visitor Parking', 'Waste Disposal', 'Water Storage', 'Water purifier',
                       'Water softening plant']

data[categorical_columns] = data[categorical_columns].astype(str)

col1, col2 = st.columns(2)
with col1:
    feature1 = st.selectbox('Select Feature 1', ['Choose a feature'] + categorical_columns)
with col2:
    feature2 = st.selectbox('Select Feature 2', ['Choose a feature'] + categorical_columns)

if feature1 != 'Choose a feature' and feature2 != 'Choose a feature':
    st.write(f'{feature1} v/s {feature2}')
    pivot_table = pd.pivot_table(data, values='price_per_sqft', index=feature1, columns=feature2, aggfunc='median')
    fig = px.imshow(pivot_table,
                    labels=dict(color='Median Price Per Sqft'),
                    x=pivot_table.columns,
                    y=pivot_table.index,
                    color_continuous_scale='Viridis')
    st.plotly_chart(fig)


st.write(f'Visualize any of the features against price/sqft')
feature = st.selectbox('Select a feature', ['Choose a feature', 'facing'] + categorical_columns)

if feature != 'Choose a feature':
    st.write(f'Pie plot for {feature}')
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data, x='price_per_sqft', fill=True, hue=feature, ax=ax)

    # Customize the plot
    ax.set_xlabel(feature, fontsize=14)
    ax.set_ylabel('Density', fontsize=14)
    st.pyplot(fig)

