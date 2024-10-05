import streamlit as st
import mysql.connector
import pandas as pd
import os
# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='04101998',
        database='redbus'
    )

# Function to construct SQL query based on user filters
def construct_query(route, bus_type, seats, price):
    query = "SELECT * FROM bus_routes WHERE 1=1"
    
    if route != 'All':
        query += f" AND route_name='{route}'"
    if bus_type != 'All':
        query += f" AND bustype='{bus_type}'"
    
    seat_ranges = {'<10': 'seats_available < 10', '10-20': 'seats_available BETWEEN 10 AND 20', 
                   '20-30': 'seats_available BETWEEN 20 AND 30', '30-40': 'seats_available BETWEEN 30 AND 40', 
                   '40-50': 'seats_available BETWEEN 40 AND 50', '>50': 'seats_available > 50'}
    if seats != 'All':
        query += f" AND {seat_ranges[seats]}"
    
    price_ranges = {'<1000': 'price < 1000', '1000-2000': 'price BETWEEN 1000 AND 2000',
                    '2000-3000': 'price BETWEEN 2000 AND 3000', '3000-4000': 'price BETWEEN 3000 AND 4000', 
                    '>4000': 'price > 4000'}
    if price != 'All':
        query += f" AND {price_ranges[price]}"
    
    return query

# Streamlit app layout
st.header('REDBUS DataScraping Project :bus:')
#file_path = "c:/Users/SATHISH KUMAR/Desktop/REDBUS/REDBUS OUTPUT.XLSX.xlsx"
file_path = "C:/Users/SATHISH KUMAR/Desktop/REDBUS/output_redbus.xlsx"

if not os.path.isfile(file_path):
    st.error(f"File not found: {file_path}")
else:
    df = pd.read_excel(file_path)


# Load data to display filters
#df = pd.read_excel("C:/path/to/your/output_redbus.xlsx")

df = pd.read_excel("c:/Users/SATHISH KUMAR/Desktop/REDBUS/output_redbus.xlsx")

# Route name filter
route_name = st.selectbox("Select Route:", ['All'] + sorted(df['Bus Route Name'].unique().tolist()))

# Bus type filter
bus_type = st.selectbox("Select Bus Type:", ['All'] + sorted(df['Bus Type'].unique().tolist()))

# Seats availability filter
seats = st.selectbox("Select Seats Available:", ['All', '<10', '10-20', '20-30', '30-40', '40-50', '>50'])

# Price filter
price = st.selectbox("Select Price Range:", ['All', '<1000', '1000-2000', '2000-3000', '3000-4000', '>4000'])

# Fetch data based on filters
with st.spinner("Fetching data..."):
    con = get_db_connection()
    cursor = con.cursor()
    
    query = construct_query(route_name, bus_type, seats, price)
    cursor.execute(query)
    rows = cursor.fetchall()
    
    df_filtered = pd.DataFrame(rows, columns=['Id', 'Route Name', 'Route Link', 'Bus Name', 'Bus Type', 
                                              'Departing Time', 'Duration', 'Reaching Time', 'Rating', 'Price', 'Seats Available'])
    
    cursor.close()
    con.close()

# Display filtered results
st.header("Filtered Bus Details")
st.dataframe(df_filtered.drop(columns=['Id']), use_container_width=True)

