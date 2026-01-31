import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import gdown
import os

# --- 1. CONFIG & MANCHESTER UNITED THEME ---
st.set_page_config(page_title="Game Luckit", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    /* Manchester United Dark Mode */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Input Boxes - United Red & Gold */
    .stNumberInput input {
        background-color: #1A1A1A !important;
        color: #DA291C !important;
        border: 2px solid #FBE122 !important;
        border-radius: 10px !important;
        font-weight: bold;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: bold !important;
        border: 1px solid #333 !important;
    }

    /* THE PEARL BUTTON (Lemon Color) */
    div.stButton > button:first-child[kind="primary"] {
        background-color: #D1FF00 !important;
        color: #000000 !important;
        border: none !important;
        font-size: 22px !important;
        height: 3.5em !important;
        box-shadow: 0px 0px 20px rgba(209, 255, 0, 0.6);
        margin-top: 20px;
    }
    
    /* Header styling */
    h1 { color: #DA291C; text-shadow: 2px 2px #000000; text-align: center; margin-bottom: 0px; }
    h3 { text-align: center; color: #FFFFFF; margin-top: 0px; opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA CONNECTION (gdown for 1.2GB Files) ---
@st.cache_data
def load_data():
    file_id = "1g3T1DhAQQTN8G1tCJ_Te3xa0qx5pBgfw"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "large_data.csv"
    
    try:
        # Download file if it doesn't exist locally on the server
        if not os.path.exists(output):
            with st.spinner("Downloading Global Database (1.2GB)... This happens only once."):
                gdown.download(url, output, quiet=False)
        
        # Read 100k rows to manage RAM
        df = pd.read_csv(output, nrows=100000) 
        
        # Standardize Columns
        df.columns = df.columns.str.strip()
        if 'Sum' in df.columns:
            df['Sum'] = pd.to_numeric(df['Sum'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return pd.DataFrame()

# Initialize Data
df = load_data()

# --- 3. STATE MANAGEMENT ---
if 'color_1' not in st.session_state: st.session_state.color_1 = 'Red'
if 'color_2' not in st.session_state: st.session_state.color_2 = 'Blue'

# --- 4. APP INTERFACE ---
st.title("⚽ Game Luckit")
st.write("### Manchester United Strategy Dashboard")

# --- PLOT 1 SECTION ---
st.markdown("---")
st.subheader("🎯 First Plot Configuration")
sum_1 = st.number_input("Enter First Target Sum", min_value=1, value=100, key="s1")

c1_col1, c1_col2, c1_col3, c1_col4 = st.columns(4)
with c1_col1:
    if st.button("🔴 Red", key="btn_r1", use_container_width=True): st.session_state.color_1 = "Red"
with c1_col2:
    if st.button("🔵 Blue", key="btn_b1", use_container_width=True): st.session_state.color_1 = "Blue"
with c1_col3:
    if st.button("🟢 Green", key="btn_g1", use_container_width=True): st.session_state.color_1 = "Green"
with c1_col4:
    if st.button("⚫ Black", key="btn_bl1", use_container_width=True): st.session_state.color_1 = "Black"

st.markdown(f"Selected: **{st.session_state.color_1}**")

# --- PLOT 2 SECTION ---
st.markdown("---")
st.subheader("📊 Second Plot Configuration")
sum_2 = st.number_input("Enter Second Target Sum", min_value=1, value=150, key="s2")

c2_col1, c2_col2, c2_col3, c2_col4 = st.columns(4)
with c2_col1:
    if st.button("🔴 Red ", key="btn_r2", use_container_width=True): st.session_state.color_2 = "Red"
with c2_col2:
    if st.button("🔵 Blue ", key="btn_b2", use_container_width=True): st.session_state.color_2 = "Blue"
with c2_col3:
    if st.button("🟢 Green ", key="btn_g2", use_container_width=True): st.session_state.color_2 = "Green"
with c2_col4:
    if st.button("⚫ Black ", key="btn_bl2", use_container_width=True): st.session_state.color_2 = "Black"

st.markdown(f"Selected: **{st.session_state.color_2}**")

st.markdown("###")

# --- 5. THE PEARL BUTTON & LOGIC ---
if st.button("RUN PEARL", type="primary", use_container_width=True):
    if df.empty:
        st.error("Database is empty or failed to load.")
    else:
        with st.spinner("⚔️ Analyzing Old Trafford Historical Data..."):
            
            # Filtering Logic
            match1 = df[
                (df['Sum'] == sum_1) & 
                (df['Winning Color'].astype(str).str.strip().str.lower() == st.session_state.color_1.lower())
            ].head(10)

            match2 = df[
                (df['Sum'] == sum_2) & 
                (df['Winning Color'].astype(str).str.strip().str.lower() == st.session_state.color_2.lower())
            ].head(10)

            if not match1.empty or not match2.empty:
                col_res1, col_res2 = st.columns(2)
                
                # Plotting Colors
                color_map = {'Red': '#DA291C', 'Blue': '#0000FF', 'Green': '#00FF00', 'Black': '#444444', 'Draw': '#FFFFFF'}

                with col_res1:
                    st.write(f"#### {st.session_state.color_1} Analysis")
                    if not match1.empty:
                        fig1, ax1 = plt.subplots()
                        fig1.patch.set_facecolor('black')
                        ax1.set_facecolor('black')
                        counts = match1['Winning Color'].value_counts()
                        ax1.bar(counts.index, counts.values, color=[color_map.get(c, 'gray') for c in counts.index])
                        ax1.tick_params(colors='white')
                        st.pyplot(fig1)
                    else:
                        st.warning("No matches for Plot 1")

                with col_res2:
                    st.write(f"#### {st.session_state.color_2} Analysis")
                    if not match2.empty:
                        fig2, ax2 = plt.subplots()
                        fig2.patch.set_facecolor('black')
                        ax2.set_facecolor('black')
                        counts2 = match2['Winning Color'].value_counts()
                        ax2.bar(counts2.index, counts2.values, color=[color_map.get(c, 'gray') for c in counts2.index])
                        ax2.tick_params(colors='white')
                        st.pyplot(fig2)
                    else:
                        st.warning("No matches for Plot 2")
            else:
                st.error("No historical matches found for these combinations.")
