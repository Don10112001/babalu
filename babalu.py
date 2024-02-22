import pandas as pd 
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import altair as alt

st.set_page_config(page_title="Sales Dashboard" ,
                   page_icon=":bar_chart:",
                   layout="wide"
)
@st.cache_data
def load_data(path: str):
    data=pd.read_excel(path)
    return data
df=load_data("./supermarket_sales.xlsx")



# Add "hour" column to dataframe
try:
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
except ValueError:
    # Handle cases where seconds are missing
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour

st.sidebar.header("Please filter Here:")
city =st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df['City'].unique()
)
customer_type =st.sidebar.multiselect(
    "Select the customer type:",
    options=df["Customer_type"].unique(),
    default=df['Customer_type'].unique()
)
gender =st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df['Gender'].unique()
)



df_selection= df.query("City == @city & Customer_type == @customer_type & Gender == @gender"
)



#-------------MAINPAGE--------------#
st.title(":bar_chart:Sales Dashboard")
st.markdown("##")



#Top KPI's
total_sales=int(df_selection["Total"].sum())
average_rating=round(df_selection["Rating"].mean(),1)
star_rating=":star:"*int(round(average_rating,0))
average_sales_by_transaction=round(df_selection["Total"].mean(),2)

left_col,mid_col,right_col=st.columns(3)
with left_col:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with mid_col:
    st.subheader("Average rating:")
    st.subheader(f"{average_rating}{star_rating}")
with right_col:
    st.subheader("Average sales per transaction:")
    st.subheader(f"US $ {average_sales_by_transaction}")


st.markdown("---")

# Product sales per hour [line chart]
sales_by_hour_line = df_selection.groupby(by=["hour"]).sum()[["Quantity"]]
fig_hourly_sales_line = px.line(
    sales_by_hour_line,
    x=sales_by_hour_line.index,
    y="Quantity",
    title="<b>                                                                                                                                       Product sales per hour</b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white"
    
)
fig_hourly_sales_line.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",  # Match the background color of the bar chart
    yaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_hourly_sales_line, use_container_width=True)   

#Sales by product line [bar chart]
sales_by_product_line=(
df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales=px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b> Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"]*len(sales_by_product_line),
    template="plotly_white"
)




sales_by_hour=df_selection.groupby(by=["hour"]).sum([["Total"]])
fig_hourly_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
   
    title="<b> Sales by hour</b>",
    color_discrete_sequence=["#0083B8"]*len(sales_by_hour),
    template="plotly_white"
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)

left_colm,right_colm=st.columns(2)
left_colm.plotly_chart(fig_hourly_sales,use_container_width=True)
right_colm.plotly_chart(fig_product_sales,use_container_width=True)



st.divider()
lef_colm,righ_colm=st.columns(2)
# Pie chart for gender distribution
gender_distribution = df_selection["Gender"].value_counts(normalize=True) * 100
fig_gender_pie = px.pie(
    values=gender_distribution,
    names=gender_distribution.index,
    title="Gender",
    labels={"Gender": "Percentage", "": ""},
    color_discrete_sequence=["#0083B8"] 
)
lef_colm.plotly_chart(fig_gender_pie, use_container_width=True)












































