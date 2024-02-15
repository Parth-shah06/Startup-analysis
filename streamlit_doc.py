import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout='wide',page_title='Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df.replace('Bengaluru','Bangalore',inplace=True)
df['investors'].replace('1Crowd (through crowd funding)','1Crowd',inplace=True)
df['investors'].replace('1Crowd, Ankur Capital','1Crowd',inplace=True)
df['investors'].replace('1Crowd (through crowdfunding)','1Crowd',inplace=True)

def load_overall_analysis():
    st.title('Overall Analysis')

    c1,c2,c3,c4 = st.columns(4)

    total = round(df['amount'].sum())
    maximum = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg = round(df.groupby('startup')['amount'].sum().mean())
    total_startups = df.groupby('startup')['startup'].count().sum()
    funding = df.groupby('round')['amount'].sum().sort_values(ascending=False).head(10)
    city_wise_funding = temp_df = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
    top_startups = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
    # total amount invested
    with c1:
        st.metric('Total Investments', str(total) +' Cr','+10%')
    # highest investment
    with c2:
        st.metric('Highest Investment', str(maximum) + ' Cr','+9.3%')
    with c3:
        st.metric('Avg Investments',str(avg) + ' Cr', '+5%')

    # total funded startups
    with c4:
        st.metric('Total Funded Startups',str(total_startups))

    # month on month graph
    st.header('Month on Month Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    # Grouping and aggregating based on the selected option
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    elif selected_option == 'Count':
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    # Create a column for x-axis
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    # Plotting using Plotly Express
    fig = px.line(temp_df, x='x_axis', y='amount', title='',
                  labels={'x_axis': 'Month-Year', 'amount': 'Total' if selected_option == 'Total' else 'Count'})
    # Rotate x-axis labels for better visibility
    fig.update_layout(xaxis_tickangle=-45)
    # Display the plot using Streamlit
    st.plotly_chart(fig)

#   City wise Funding
    st.header('City Wise Funding')
    fig4 = px.bar(city_wise_funding, x=city_wise_funding['city'], y=city_wise_funding['amount'], title='')
    st.plotly_chart(fig4)

    c5,c6 = st.columns(2)
#   Sector Analysis Pie -> top sectors(Count + Sum)
    with c5:
        st.header('Sector Analysis')
        temp = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
        fig2 = px.pie(temp_df, values=temp.values, names=temp.index, title='',
                      labels={'Category: Vertical'})
        st.plotly_chart(fig2)
#   Type of Funding
    with c6:
        st.header('Type of Funding')
        fig3 = px.bar(funding, x=funding.index, y=funding.values, title='')
        st.plotly_chart(fig3)

# top startups year wise and overall
    st.header('Top Startups based on Funding Genreated!')
    fig4 = px.bar(top_startups,x=top_startups['startup'],y=top_startups['amount'],title='')
    st.plotly_chart(fig4)

# top startup based on funding generated year wise
    year_wise = st.selectbox('Select the year',[2015,2016,2017,2018,2019,2020])
    st.header('Top Startups of the year ' + str(year_wise))
    mask = df['year'] == year_wise
    year_wise_df = df[mask].groupby('startup')['amount'].max().sort_values(ascending=False).head(5).reset_index()
    fig5 = px.bar(year_wise_df,x=year_wise_df['startup'],y=year_wise_df['amount'],title='')
    st.plotly_chart(fig5)



def load_investor_details(investor):

    print(investor)
    st.title(investor)
    # latest 5 investments
    last_5df = df[df['investors'].str.contains(investor)].head(5)[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)
    # print(last_5df)

    c1,c2,c3 = st.columns(3)
    c4,c5 = st.columns(2)

#   biggest 5 investments
    with c1:
        big5_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5).reset_index()
        st.subheader('Biggest 5 investments')
        fig = px.bar(big5_df, x=big5_df['startup'], y=big5_df['amount'], title='')
        st.plotly_chart(fig)

#   sectors invested in
    with c3:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head(5).reset_index()
        st.subheader('Sectors invested in')
        fig1 = px.pie(vertical_series, values=vertical_series['amount'], names=vertical_series['vertical'], title='',
                      labels={'Category: Vertical'})
        st.plotly_chart(fig1)

# YoY investments in
    with c4:
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum().reset_index()
        print(year_series)
        fig = px.line(year_series, x=year_series['year'], y=year_series['amount'], title='YoY investments',
                      labels={'year': 'Year', 'amount': 'Amount ($)'},
                      line_shape='linear', render_mode='svg')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)
# similar investors homework

# startup analysis


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select one',['Overall Analysis','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

else:
    investor_name = st.sidebar.selectbox('Select Investor', sorted(df['investors'].unique().tolist()))
    btn2 = st.sidebar.button('Find Investor Details')

    if btn2:
        load_investor_details(investor_name)