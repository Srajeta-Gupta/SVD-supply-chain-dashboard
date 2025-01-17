import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import os 
import warnings



warnings.filterwarnings('ignore')

st.set_page_config(page_title = "Supply Chain Management", page_icon = ":baggage_claim", layout = "wide")
st.title(" :baggage_claim: Supply Chain DashBoard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)



        
fl = st.file_uploader(":file_folder: Upload Supply Chain Data Set",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding='latin-1')

    col1, col2 = st.columns((2))
    df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
    startDate = pd.to_datetime(df['order date (DateOrders)']).min()
    endDate = pd.to_datetime(df['order date (DateOrders)']).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    df = df[(df["order date (DateOrders)"] >= date1) & (df["order date (DateOrders)"] <= date2)].copy()
    st.sidebar.header("Add Filter: ")

    region = st.sidebar.multiselect("Pick your Region", df["Market"].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df["Market"].isin(region)]

    # Create for State
    state = st.sidebar.multiselect("Pick the State", df2["Customer State"].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2["Customer State"].isin(state)]

    # Create for City
    city = st.sidebar.multiselect("Pick the City",df3["Customer City"].unique())

    if not region and not state and not city:
        filtered_df = df
    elif not state and not city:
        filtered_df = df[df["Market"].isin(region)]
    elif not region and not city:
        filtered_df = df[df["Customer State"].isin(state)]
    elif state and city:
        filtered_df = df3[df["Customer State"].isin(state) & df3["Customer City"].isin(city)]
    elif region and city:
        filtered_df = df3[df["Market"].isin(region) & df3["Customer City"].isin(city)]
    elif region and state:
        filtered_df = df3[df["Market"].isin(region) & df3["Customer State"].isin(state)]
    elif city:
        filtered_df = df3[df3["Customer City"].isin(city)]
    else:
        filtered_df = df3[df3["Market"].isin(region) & df3["Customer State"].isin(state) & df3["Customer City"].isin(city)]

    category_df = filtered_df.groupby(by = ["Category Name"], as_index = False)["Sales"].sum()

    with col1:
        st.subheader("Category wise Supplies")
        fig = px.bar(category_df, x = "Category Name", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)

    with col2:
        st.subheader("Region wise Supplies")
        fig = px.pie(filtered_df, values = "Sales", names = "Market", hole = 0.5)
        fig.update_traces(text = filtered_df["Market"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)

    st.subheader('Time Series Analysis')
    filtered_df["month_year"] = filtered_df["order date (DateOrders)"].dt.to_period("M")
    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
    fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Order Item Product Price"},height=500, width = 1000,template="gridon")
    st.plotly_chart(fig2,use_container_width=True)


    # Create a treem based on Region, category, sub-Category
    st.subheader("Hierarchical view of Sales using TreeMap")
    fig3 = px.treemap(filtered_df, path = ["Market","Category Name"], values = "Sales",hover_data = ["Sales"],
                    color = "Category Name")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3, use_container_width=True)

    chart1, chart2 = st.columns((2))
    with chart1:
        st.subheader('Segment wise Sales')
        fig = px.pie(filtered_df, values = "Sales", names = "Market", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Market"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with chart2:
        st.subheader('Category wise Sales')
        fig = px.pie(filtered_df, values = "Sales", names = "Category Name", template = "gridon")
        fig.update_traces(text = filtered_df["Category Name"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Sub-Category Sales Summary")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["Market","Customer State","Customer City","Category Name","Sales","Order Profit Per Order","Order Item Quantity"]]
        fig = ff.create_table(df_sample, colorscale = "Cividis")
        st.plotly_chart(fig, use_container_width=True)


    # scatter plot
    data1 = px.scatter(filtered_df, x = "Sales", y = "Order Profit Per Order", size = "Order Item Quantity")
    data1['layout'].update(
        title="Relationship between Sales and Profits using Scatter Plot.",
        titlefont = dict(size=20),
        xaxis = dict(title="Sales",
        titlefont=dict(size=19)),
        yaxis = dict(title = "Profit", titlefont = dict(size=19)))
    st.plotly_chart(data1,use_container_width=True)

cmain1, cmain2, cmain3 = st.columns((3))
with cmain1:
    # st.subheader('Explore Other Amazon Products')
    centered_div = """
    <div style="
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            text-align: center;
        ">
        <h2 style="margin-bottom: 20px;">Explore Various Supply Chain Visibility</h2>
        <h4 style="margin-bottom: 20px; font-weight: 50; font-size: 100%;">  
Improved visibility ensures better order fulfillment rates and on-time deliveries.            </h4>
        <button 
            style="width: 200px; 
            padding: 10px; 
            background-color: #ffaa00; 
            border: none; 
            border-radius: 5px;
        ">Explore SVD</button>
    </div>
    """

    st.markdown(centered_div, unsafe_allow_html=True)

with cmain2:
    centered_div = """
    <div style="
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            text-align: center;
        ">
        <h2 style="margin-bottom: 20px;">Explore Relationships</h2>
        <h4 style="margin-bottom: 20px; font-weight: 100; font-size: 100%;"> 
Access to real-time data helps in making informed decisions based on current conditions and trends.Helps maintain optimal inventory levels, reducing carrying costs and avoiding stockouts or overstock situations            </h4>
        <button 
            style="width: 200px; 
            padding: 10px; 
            background-color: #ffaa00; 
            border: none; 
            border-radius: 5px;
        ">Explore SVD Products</button>
    </div>
    """
    st.markdown(centered_div, unsafe_allow_html=True)

with cmain3:
    centered_div = """
    <div style="
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            text-align: center;
        ">
        <h2 style="margin-bottom: 20px;">
                Explore SVD Dashbords
            </h2> 
        <h4 style="margin-bottom: 20px; font-weight: 100; font-size: 100%;"> 
 Dashboards provide real-time data, enabling stakeholders to monitor the supply chain's status and performance            </h4>
        <button 
            style="width: 200px; 
            padding: 10px; 
            background-color: #ffaa00; 
            border: none; 
            border-radius: 5px;
            transition: background-color 0.3s ease; 
        "
        >Explore SVD</button>
    </div>
    """

    st.markdown(centered_div, unsafe_allow_html=True)
