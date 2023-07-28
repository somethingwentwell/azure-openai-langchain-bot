import streamlit as st
<<<<<<< HEAD
#import pandas as pd
import requests
import json
#import plotly.express as px

# Define API endpoint
API_ENDPOINT = "http://insource-test-015.southeastasia.cloudapp.azure.com:8100/all_token_used/"

# Define function to query API
def query_api(params):
    response = requests.get(API_ENDPOINT + params)
    data = json.loads(response.text)
    return data

# # Define function to plot line graph
# def plot_line_graph(data, x, y, title):
#     fig = px.line(data, x=x, y=y, title=title)
#     st.plotly_chart(fig)

# # Define function to plot pie chart
# def plot_pie_chart(data, values, names, title):
#     fig = px.pie(data, values=values, names=names, title=title)
#     st.plotly_chart(fig)

# Define function to display card
def display_card(title, value):
    st.markdown(f"**{title}:**")
    st.markdown(f"<h1 style='text-align: center;'>{value}</h1>", unsafe_allow_html=True)

# Define app layout
st.set_page_config(page_title="Token Usage Monitor")
st.title("Token Usage Monitor")

# Define selectbox
query_type = st.selectbox("Select query type", ["This year", "This month", "Today"])
params = {}
if query_type == "This year":
    params = "year"
    title = "Token Usage This Year"
elif query_type == "This month":
    params = "month"
    title = "Token Usage This Month"
else:
    params = "day"
    title = "Token Usage Today"

# Query API and display results
data = query_api(params)
#df = pd.DataFrame(data)
total_token = data["all_token_used"]

#plot_line_graph(df, "date", "token", "Token Usage")
#plot_pie_chart(df, "token", "api_name", "Token Usage by API")
st.metric(label="Total Token", value=total_token)
#display_card("Total API Request", total_api_request)
#display_card("Total Token Today", total_token_today)
=======
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("token_usage.csv")

# Calculate total token and api requests
total_token = data["Token"].sum()
total_requests = data["Requests"].sum()

# Filter data by date
today = pd.Timestamp.today().strftime("%Y-%m-%d")
today_data = data[data["Date"] == today]
today_token = today_data["Token"].sum()

# Line graph of token usage by year, month, week, day
fig = px.line(data, x="Date", y="Token", title="Token Usage Over Time")
fig.update_xaxes(title="Date")
fig.update_yaxes(title="Token Usage")

# Pie chart of total token usage
fig2 = px.pie(data, values="Token", names="Date", title="Total Token Usage")

# Cards for total token, total api requests, and token usage today
st.write(f"Total Token: {total_token}")
st.write(f"Total API Requests: {total_requests}")
st.write(f"Token Used Today: {today_token}")
st.write(fig)
st.write(fig2)
>>>>>>> d659923 (test)
