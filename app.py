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
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
    .stNumberInput input { background-color: #1A1A1A !important; color: #DA291C !important; border: 2px solid #FBE122 !important; border-radius: 10px !important; font-weight: bold; }
    .stButton>button { border-radius: 8px !important; font-weight: bold !important; border: 1px solid #333 !important; }
    div.stButton > button:first-child[kind="primary"] { background-color: #D1FF00 !important; color: #000000 !important; font-size: 22px !important; height: 3.5em !important; box-shadow: 0px 0px 20px rgba(209, 255, 0, 0.6); margin-top: 20px; width: 100%; }
    h1 { color: #DA291C; text-shadow: 2px 2px #000000; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA CONNECTION ---
@st.cache_data
def load_data():
    file_id = "1g3T1DhAQQTN8G1tCJ_Te3xa0qx5pBgfw"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "large_data.csv"
    try:
        if not os.path.exists(output):
            with st.spinner("Downloading Database (1.2GB)..."):
                gdown.download(url, output, quiet=False)
        df = pd.read_csv(output, nrows=100000) 
        df.columns = df.columns.str.strip()
        if 'Sum' in df.columns:
            df['Sum'] = pd.to_numeric(df['Sum'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- 3. HELPER FUNCTIONS FOR SIMULATION ---
def get_color_name(n):
    if n == 49: return 'Black'
    mapping = {1: 'Red', 2: 'Blue', 0: 'Green'}
    return mapping[n % 3]

def calculate_winner(numbers):
    counts = {'Red': 0, 'Blue': 0, 'Green': 0, 'Black': 0}
    for n in numbers:
        counts[get_color_name(n)] += 1
    max_val = max(counts['Red'], counts['Blue'], counts['Green'])
    winners = [c for c, count in counts.items() if count == max_val and c != 'Black']
    return winners[0] if len(winners) == 1 and max_val >= 3 else "Draw"

# --- 4. STATE MANAGEMENT ---
if 'selected_color' not in st.session_state: st.session_state.selected_color = 'Red'

# --- 5. UI ---
st.title("⚽ Game Luckit")
st.write("<h3 style='text-align: center;'>Unified Strategy Dashboard</h3>", unsafe_allow_html=True)

st.markdown("---")
col_input1, col_input2 = st.columns([1, 2])

with col_input1:
    user_sum = st.number_input("Enter Target Sum", min_value=1, value=100)

with col_input2:
    st.write("Select Winning Color")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔴 Red", use_container_width=True): st.session_state.selected_color = "Red"
    with c2:
        if st.button("🔵 Blue", use_container_width=True): st.session_state.selected_color = "Blue"
    with c3:
        if st.button("🟢 Green", use_container_width=True): st.session_state.selected_color = "Green"
    with c4:
        if st.button("⚫ Black", use_container_width=True): st.session_state.selected_color = "Black"

st.info(f"Analysis targeting: **Sum {user_sum}** and **Color {st.session_state.selected_color}**")

# --- 6. THE PEARL LOGIC (Double Analysis) ---
if st.button("RUN PEARL", type="primary"):
    if df.empty:
        st.error("Database failed to load.")
    else:
        with st.spinner("⚔️ Executing Master Analysis..."):
            
            # --- PART A: HISTORICAL PATTERN SEARCH ---
            condition = (df['Sum'] == user_sum) & (df['Winning Color'].str.lower() == st.session_state.selected_color.lower())
            initial_match = df[condition].head(1)

            if not initial_match.empty:
                start_pos = df.index.get_loc(initial_match.index[0])
                
                # Slices
                chart1_data = df.iloc[start_pos : min(start_pos + 10, len(df))]
                
                chart2_data = pd.DataFrame()
                for i in range(start_pos, min(start_pos + 500, len(df) - 9)):
                    win = df.iloc[i : i + 10]
                    if any(win['Winning Color'].value_counts() >= 6):
                        chart2_data = win
                        break
                
                chart3_data = pd.DataFrame()
                for i in range(start_pos, min(start_pos + 500, len(df) - 4)):
                    win = df.iloc[i : i + 5]
                    if any(win['Winning Color'].value_counts() >= 3):
                        chart3_data = win
                        break

                # --- PART B: PROBABILITY SIMULATION ---
                winners_list = [st.session_state.selected_color]
                for _ in range(9):
                    winners_list.append(calculate_winner(random.sample(range(1, 50), 6)))
                sim_df = pd.DataFrame(winners_list, columns=['Winning Color'])

                # --- PART C: PLOTTING ALL CHARTS ---
                st.markdown("### 📊 Historical Patterns (From Database)")
                fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
                fig.patch.set_facecolor('black')
                color_map = {'Red': 'red', 'Blue': 'blue', 'Green': 'green', 'Black': '#444444', 'Draw': 'white', 'No Majority': 'gray'}

                def draw_chart(ax, data, title):
                    if not data.empty:
                        counts = data['Winning Color'].value_counts()
                        ax.bar(counts.index, counts.values, color=[color_map.get(c, 'gray') for c in counts.index])
                        ax.set_title(title, color='white')
                        ax.tick_params(colors='white')
                        ax.set_facecolor('black')
                    else:
                        ax.text(0.5, 0.5, "Pattern Not Found", color='red', ha='center')
                        ax.axis('off')

                draw_chart(ax1, chart1_data, "First 10 Rows")
                draw_chart(ax2, chart2_data, "6+ Color Pattern")
                draw_chart(ax3, chart3_data, "3+ Color Pattern")
                st.pyplot(fig)

                st.markdown("---")
                st.markdown("### 🎲 Probability Distribution (Simulation)")
                fig_sim, ax_sim = plt.subplots(figsize=(10, 4))
                fig_sim.patch.set_facecolor('black')
                ax_sim.set_facecolor('black')
                sim_counts = sim_df['Winning Color'].value_counts()
                ax_sim.bar(sim_counts.index, sim_counts.values, color=[color_map.get(c, 'gray') for c in sim_counts.index])
                ax_sim.tick_params(colors='white')
                st.pyplot(fig_sim)

            else:
                st.error("No matches found in the database for those inputs.")
