import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)

    
    df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('  ', ' ').str.title()

   
    st.write("Columns found in CSV:", df.columns.tolist())


    if 'Category' not in df.columns or 'Year' not in df.columns:
        st.error("The dataset must contain 'Category' (used as Month) and 'Year' columns.")
        st.stop()

    
    df = df.dropna(subset=["Year", "Category"])
    df["Year"] = df["Year"].astype(int)
    df["Category"] = df["Category"].astype(str).str.strip().str.capitalize()

    return df


st.sidebar.title("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)

    
    st.sidebar.header("Filters")
    vehicle_types = st.sidebar.multiselect("Select Vehicle Types", sorted(df["Vehicle Class"].dropna().unique()), default=sorted(df["Vehicle Class"].dropna().unique()))


    filtered_df = df[df["Vehicle Class"].isin(vehicle_types)]

    col1, col2 = st.columns(2)

  
    with col1:
        st.subheader("Registration Trends")
        if not filtered_df.empty:
            trend_df = filtered_df.groupby(["Year", "Category"])["Count"].sum().reset_index()
            trend_df["Month_Num"] = pd.to_datetime(trend_df["Category"], format="%B", errors="coerce").dt.month
            trend_df = trend_df.dropna(subset=["Month_Num"])
            trend_df["Date"] = pd.to_datetime(dict(year=trend_df.Year, month=trend_df.Month_Num, day=1))
            trend_df = trend_df.sort_values("Date")
            fig1 = px.line(trend_df, x="Date", y="Count", title="Total Registrations Over Time")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")

    with col2:
        st.subheader("Vehicle Type Distribution")
        if not filtered_df.empty:
            fig2 = px.pie(filtered_df, names="Vehicle Class", values="Count", title="Vehicle Type Share")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No data to display pie chart.")
else:
    st.warning("Please upload a CSV file to proceed.")
