import pandas as pd
import streamlit as st
import plotly.express as px
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import numpy as np


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

st.set_page_config(layout="wide")
df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympics Analysis')
st.sidebar.image("assets/vecteezy_sankt-petersburg-russia-01-02-2024-olympic-rings-olympic_36105751.png")
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis','Country-wise Analysis','Athlete Wise Analysis')
)


if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    country,year=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select Year',year)
    selected_country=st.sidebar.selectbox('Select Country',country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country=='Overall' and selected_year=='Overall':
     st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
     st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+" overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+" performance in "+str(selected_year)+" Olympics")
    st.set_page_config(layout="wide")
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    st.title('Top Statistics')
    edition=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Edition')
        st.title(edition)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time, x="Edition", y="region")
    st.title('Participating Nation over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title('Events over the years')
    st.plotly_chart(fig)


    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title('Athletes over the years')
    st.plotly_chart(fig)

    st.title('No. of Events over time(Every Sport)')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0), annot=True)
    st.pyplot(fig)

    st.title('Most successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select Country',country_list)
    country_df=helper.yearwise_medal_tally(df,selected_country)

    fig = px.line(country_df, x="Year", y="Medal")

    st.title(selected_country+' Medal Tally over the years')
    st.plotly_chart(fig)

    st.title(selected_country + ' excels in following sports')

    pt = helper.country_event_heatmap(df, selected_country)

    if pt is None or pt.empty:
        st.info(f"{selected_country} has not won any Olympic medals")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(pt, annot=True, ax=ax)
        st.pyplot(fig)

    st.title('Top 10 athletes of '+ selected_country )
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete Wise Analysis':


    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False,
        show_rug=False
    )


    fig.update_layout(autosize=False,width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football',
                     'Tug-Of-War', 'Athletics', 'Swimming',
                     'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting',
                     'Wrestling', 'Water Polo', 'Hockey',
                     'Rowing', 'Fencing', 'Equestrianism',
                     'Shooting', 'Boxing', 'Taekwondo',
                     'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Modern Pentathlon', 'Golf',
                     'Softball', 'Archery', 'Volleyball',
                     'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
                     'Beach Volleyball', 'Triathlon', 'Rugby',
                     'Lacrosse', 'Polo', 'Cricket',
                     'Ice Hockey', 'Racquets', 'Motorboating',
                     'Croquet', 'Figure Skating', 'Jeu De Paume',
                     'Roque', 'Basque Pelota', 'Alpinism',
                     'Aeronautics']
    for sport in famous_sports:
        temp_df = df[(df['Sport'] == sport) & (df['Medal'] == 'Gold')]
        ages = temp_df['Age'].dropna().values.tolist()

        if len(ages) > 1 and np.std(ages) > 0:
            x.append(ages)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age wrt Sports(Gold Medalist)')
    st.plotly_chart(fig)

    st.title('Weight vs Height')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    temp_df=helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], hue_order=['No Medal', 'Silver', 'Bronze','Gold'],style=temp_df['Sex'],s=60)

    st.pyplot(fig)

    st.title('Men Vs Women Participation Over the Years')
    final=helper.men_vs_women(df)
    fig = px.line(
        final,
        x='Year',
        y=['Male Athletes', 'Female Athletes'],
        color_discrete_map={
            'Male Athletes': 'lightblue',
            'Female Athletes': 'red'
        }
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
