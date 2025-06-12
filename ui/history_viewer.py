import streamlit as st
import pandas as pd
from utils.db import get_connection

def view_history():
    st.header("Riwayat Upload Data")
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM inventory ORDER BY date DESC", conn)
    conn.close()
    st.dataframe(df)
