import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# --- 1. THE MANCHESTER UNITED "THEATER OF DREAMS" THEME ---
st.set_page_config(page_title="Game Luckit", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    /* Manchester United Dark Mode */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Input Boxes */
    .stNumberInput input {
        background-color: #1A1A1A !important;
        color: #DA291C !important; /* United Red */
        border: 2px solid #FBE122 !important; /* United Gold */
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
        background-color: #D1FF00 !important; /* Lemon */
        color: #000000 !important;
        border: none !important;
        font-size: 20px !important;
        height: 3em !important;
        box-shadow: 0px 0px 15px rgba(209, 255, 0, 0.4);
    }
    
    /* Header styling */
    h1 { color: #DA291C; text-shadow: 2px 2px #000000; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Loading subset for speed, ensure file is in same directory
        return pd.read_csv("randomnumber.csv", usecols=['Numbers', 'Sum', 'Winning Color'])
    except:
        return pd.DataFrame(columns=['Numbers', 'Sum', 'Winning Color'])

df = load_data()

# --- 3. STATE MANAGEMENT FOR COLOR BUTTONS ---
if 'color_1' not in st.session_state: st.session_state.color_1 = 'Red'
if 'color_2' not in st.session_state: st.session_state.color_2 = 'Blue'

# --- 4. APP INTERFACE ---
st.title("⚽ Game Luckit")
st.write("### Manchester United Strategy Dashboard")

# --- PLOT 1 SECTION ---
st.markdown("---")
st.subheader("🎯 First Plot Configuration")
sum_1 = st.number_input("Enter First Target Sum", min_value=1, value=100, key="s1")

# Color Selection Row 1
c1_col1, c1_col2, c1_col3, c1_col4 = st.columns(4)
with c1_col1:
    if st.button("🔴 Red", key="btn_r1", use_container_width=True): st.session_state.color_1 = "Red"
with c1_col2:
    if st.button("🔵 Blue", key="btn_b1", use_container_width=True): st.session_state.color_1 = "Blue"
with c1_col3:
    if st.button("🟢 Green", key="btn_g1", use_container_width=True): st.session_state.color_1 = "Green"
with c1_col4:
    if st.button("⚫ Black", key="btn_bl1", use_container_width=True): st.session_state.color_1 = "Black"

st.write(f"Selected Color: **{st.session_state.color_1}**")

# --- PLOT 2 SECTION ---
st.markdown("---")
st.subheader("📊 Second Plot Configuration")
sum_2 = st.number_input("Enter Second Target Sum", min_value=1, value=150, key="s2")

# Color Selection Row 2
c2_col1, c2_col2, c2_col3, c2_col4 = st.columns(4)
with c2_col1:
    if st.button("🔴 Red ", key="btn_r2", use_container_width=True): st.session_state.color_2 = "Red"
with c2_col2:
    if st.button("🔵 Blue ", key="btn_b2", use_container_width=True): st.session_state.color_2 = "Blue"
with c2_col3:
    if st.button("🟢 Green ", key="btn_g2", use_container_width=True): st.session_state.color_2 = "Green"
with c2_col4:
    if st.button("⚫ Black ", key="btn_bl2", use_container_width=True): st.session_state.color_2 = "Black"

st.write(f"Selected Color: **{st.session_state.color_2}**")

st.markdown("###")

# --- 5. THE PEARL BUTTON ---
if st.button("RUN PEARL", type="primary", use_container_width=True):
    with st.spinner("Analyzing Old Trafford Data..."):
        # Logic for Plot 1
        match1 = df[(df['Sum'] == sum_1) & (df['Winning Color'] == st.session_state.color_1)].head(10)
        # Logic for Plot 2
        match2 = df[(df['Sum'] == sum_2) & (df['Winning Color'] == st.session_state.color_2)].head(10)

        if not match1.empty or not match2.empty:
            col_res1, col_res2 = st.columns(2)
            
            color_map = {'Red': '#DA291C', 'Blue': '#0000FF', 'Green': '#00FF00', 'Black': '#000000'}

            with col_res1:
                st.write(f"### {st.session_state.color_1} Analysis")
                fig1, ax1 = plt.subplots()
                fig1.patch.set_facecolor('black')
                ax1.set_facecolor('black')
                counts = match1['Winning Color'].value_counts()
                ax1.bar(counts.index, counts.values, color=[color_map.get(c, 'gray') for c in counts.index])
                ax1.tick_params(colors='white')
                st.pyplot(fig1)

            with col_res2:
                st.write(f"### {st.session_state.color_2} Analysis")
                fig2, ax2 = plt.subplots()
                fig2.patch.set_facecolor('black')
                ax2.set_facecolor('black')
                counts2 = match2['Winning Color'].value_counts()
                ax2.bar(counts2.index, counts2.values, color=[color_map.get(c, 'gray') for c in counts2.index])
                ax2.tick_params(colors='white')
                st.pyplot(fig2)
        else:
            st.error("No matches found for these specific combinations.")