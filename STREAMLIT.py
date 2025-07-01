import streamlit as st
import mysql.connector
import pandas as pd
import os

# --- Function to connect to the MySQL database ---
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='04101998',
        database='redbus'
    )

# --- Function to construct SQL query based on filters ---
def construct_query(route, bus_type, seats, price):
    query = "SELECT * FROM bus_routes WHERE 1=1"

    if route != 'All':
        query += f" AND route_name='{route}'"
    if bus_type != 'All':
        query += f" AND bustype='{bus_type}'"

    seat_ranges = {
        '<10': 'seats_available < 10',
        '10-20': 'seats_available BETWEEN 10 AND 20',
        '20-30': 'seats_available BETWEEN 20 AND 30',
        '30-40': 'seats_available BETWEEN 30 AND 40',
        '40-50': 'seats_available BETWEEN 40 AND 50',
        '>50': 'seats_available > 50'
    }
    if seats != 'All':
        query += f" AND {seat_ranges[seats]}"

    price_ranges = {
        '<1000': 'price < 1000',
        '1000-2000': 'price BETWEEN 1000 AND 2000',
        '2000-3000': 'price BETWEEN 2000 AND 3000',
        '3000-4000': 'price BETWEEN 3000 AND 4000',
        '>4000': 'price > 4000'
    }
    if price != 'All':
        query += f" AND {price_ranges[price]}"

    return query

# --- Streamlit UI ---
st.set_page_config(page_title="Redbus Bus Finder", layout="wide")
st.markdown("## 🚌 REDBUS Bus Search Application")

# Load Excel
file_path = "D:/santhanam/REDBUS/output_redbus.xlsx"
if not os.path.isfile(file_path):
    st.error(f"❌ File not found: `{file_path}`")
    st.stop()

df = pd.read_excel(file_path)

# --- Filter Selection in Columns ---
with st.expander("🔎 Filter Your Search", expanded=True):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        route_name = st.selectbox("🛣️ Route", ['All'] + sorted(df['Bus Route Name'].unique().tolist()))
    with col2:
        bus_type = st.selectbox("🚌 Bus Type", ['All'] + sorted(df['Bus Type'].unique().tolist()))
    with col3:
        seats = st.selectbox("💺 Seats Available", ['All', '<10', '10-20', '20-30', '30-40', '40-50', '>50'])
    with col4:
        price = st.selectbox("💰 Price Range", ['All', '<1000', '1000-2000', '2000-3000', '3000-4000', '>4000'])

    search = st.button("🔍 Search Buses")

# --- Perform Search ---
if search:
    with st.spinner("🔄 Connecting to database and fetching results..."):
        try:
            con = get_db_connection()
            cursor = con.cursor()
            query = construct_query(route_name, bus_type, seats, price)
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            con.close()
        except Exception as e:
            st.error(f"❌ Database error: {e}")
            st.stop()

        if rows:
            df_result = pd.DataFrame(rows, columns=[
                'Id', 'Route Name', 'Route Link', 'Bus Name', 'Bus Type',
                'Departing Time', 'Duration', 'Reaching Time', 'Rating',
                'Price', 'Seats Available'
            ])
            st.success(f"✅ {len(df_result)} bus(es) found.")
            st.dataframe(df_result.drop(columns=['Id']), use_container_width=True)
        else:
            st.warning("😕 No buses found for the selected filters.")
