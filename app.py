import pandas as pd
import matplotlib.pyplot as plt
import ast

#df = pd.read_csv("randomnumber.csv")
#df = df[['Numbers','Sum','Winning Color','Color Counts']]

try:
    df = pd.read_csv("randomnumber.csv", encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv("randomnumber.csv", encoding='latin1')
    except UnicodeDecodeError:
        df = pd.read_csv("randomnumber.csv", encoding='cp1252')
df = df[['Numbers', 'Sum', 'Winning Color', 'Color Counts']]

# --- 1. Single Input Collection for Sum and Winning Color ---
import pandas as pd
import matplotlib.pyplot as plt


# --- 1. Single Input Collection for Sum and Winning Color ---
while True:
    try:
        input_sum = int(input("Enter the target 'Sum' value (e.g., 100): "))
        break # Exit loop if input is a valid integer
    except ValueError:
        print("Invalid input. Please enter an integer for 'Sum'.")

# Convert to lowercase for consistent comparison
input_winning_color = input("Enter the target 'Winning Color' (e.g., Red): ").strip().lower()


# --- Initial Filtering to find the starting point for both charts ---
# This filtered_df_initial will find the *first* occurrence of the sum and winning color.
condition_sum_initial = (df['Sum'] == input_sum)
condition_winning_color_initial = (df['Winning Color'].str.lower() == input_winning_color)

filtered_df_initial_match = df[condition_sum_initial & condition_winning_color_initial].head(1)

# Initialize DataFrames for plotting
first_chart_data = pd.DataFrame()
second_chart_data = pd.DataFrame()
third_chart_data = pd.DataFrame()
first_chart_title = "Winning Color Counts (First 10 from Initial Match)"
second_chart_title = "Winning Color Counts (First 10 with 6+ Count of a Color)"
third_chart_title = "Winning Color Counts (First 5 with 3+ Count of a Color)"

if not filtered_df_initial_match.empty:
    first_matching_index_label = filtered_df_initial_match.index[0]
    print(f"\nInitial match for Sum={input_sum} and Winning Color='{input_winning_color}' found at original index: {first_matching_index_label}")

    # Get the integer position (iloc) of this first matching index label
    start_iloc_position_global = df.index.get_loc(first_matching_index_label)

    # --- Data for the First Chart: First 10 rows from the initial match ---
    # Ensure we don't go out of bounds of the DataFrame
    end_iloc_position_first_chart = min(start_iloc_position_global + 10, len(df))
    first_chart_data = df.iloc[start_iloc_position_global : end_iloc_position_first_chart].copy()
    print(f"Data for First Chart covers indices from {df.index[start_iloc_position_global]} to {df.index[end_iloc_position_first_chart-1]}.")

    # --- Data for the Second Chart: First 10-row window with at least one winning color having 6+ counts ---
    found_second_chart_window = False

    # Iterate from the global starting position to find the specific 10-row window
    for i in range(start_iloc_position_global, len(df) - 9):
        current_10_rows_for_check = df.iloc[i : i + 10].copy()
        current_color_counts = current_10_rows_for_check['Winning Color'].value_counts()

        # Check if any winning color in this window has a count of 6 or more
        if any(count >= 6 for count in current_color_counts.values):
            second_chart_data = current_10_rows_for_check
            found_second_chart_window = True
            print(f"Data for Second Chart found starting at original index {df.index[i]} where a color has 6+ counts.")
            break # Stop searching as we found the first such window

    if not found_second_chart_window:
        print("No 10-row window was found (starting from or after the initial match) where at least one winning color has 6 or more counts within the 10 rows.")
        # If not found, clear the second chart data to avoid plotting empty/irrelevant data
        second_chart_data = pd.DataFrame()

    # --- Data for the third Chart: First 5-row window with at least one winning color having 4+ counts ---
    found_third_chart_window = False

    # Iterate from the global starting position to find the specific 5-row window
    for i in range(start_iloc_position_global, len(df) - 3):
        current_5_rows_for_check = df.iloc[i : i + 5].copy()
        current_color_counts = current_5_rows_for_check['Winning Color'].value_counts()

        # Check if any winning color in this window has a count of 6 or more
        if any(count >= 3 for count in current_color_counts.values):
            third_chart_data = current_5_rows_for_check
            found_third_chart_window = True
            print(f"Data for third Chart found starting at original index {df.index[i]} where a color has 3+ counts.")
            break # Stop searching as we found the first such window

    if not found_third_chart_window:
        print("No 5-row window was found (starting from or after the initial match) where at least one winning color has 3 or more counts within the 5 rows.")
        # If not found, clear the second chart data to avoid plotting empty/irrelevant data
        third_chart_data = pd.DataFrame()


    # --- Plotting Function (Modified for side-by-side) ---
    def plot_colored_bar_charts_side_by_side(df1, title1, df2, title2,  df3, title3):
        """
        Plots three bar charts side-by-side.
        Each chart shows winning color counts for the given DataFrame slices.
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 5)) # 1 row, 3 columns for side-by-side plots

        colors_map = {
            'Green': 'green',
            'Blue': 'blue',
            'Red': 'red',
            'Draw': 'black'
        }

        # Plot for the First Chart
        if not df1.empty:
            color_counts1 = df1["Winning Color"].value_counts()
            bar_colors1 = [colors_map.get(color, 'gray') for color in color_counts1.index]
            axes[0].bar(color_counts1.index, color_counts1.values, color=bar_colors1)
            axes[0].set_title(title1)
            axes[0].set_xlabel("Winning Colors")
            axes[0].set_ylabel("Counts")
            axes[0].grid(axis='y', linestyle='--', alpha=0.7)
        else:
            axes[0].text(0.5, 0.5, "No data for this chart", horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
            axes[0].set_title(title1)
            axes[0].axis('off') # Hide axes if no data

        # Plot for the Second Chart
        if not df2.empty:
            color_counts2 = df2["Winning Color"].value_counts()
            bar_colors2 = [colors_map.get(color, 'gray') for color in color_counts2.index]
            axes[1].bar(color_counts2.index, color_counts2.values, color=bar_colors2)
            axes[1].set_title(title2)
            axes[1].set_xlabel("Winning Colors")
            axes[1].set_ylabel("Counts")
            axes[1].grid(axis='y', linestyle='--', alpha=0.7)
        else:
            axes[1].text(0.5, 0.5, "No data for this chart", horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
            axes[1].set_title(title2)
            axes[1].axis('off') # Hide axes if no data

        # Plot for the third Chart
        if not df3.empty:
            color_counts3 = df3["Winning Color"].value_counts()
            bar_colors3 = [colors_map.get(color, 'gray') for color in color_counts3.index]
            axes[2].bar(color_counts3.index, color_counts3.values, color=bar_colors3)
            axes[2].set_title(title3)
            axes[2].set_xlabel("Winning Colors")
            axes[2].set_ylabel("Counts")
            axes[2].grid(axis='y', linestyle='--', alpha=0.7)
        else:
            axes[2].text(0.5, 0.5, "No data for this chart", horizontalalignment='center', verticalalignment='center', transform=axes[2].transAxes)
            axes[2].set_title(title3)
            axes[2].axis('off') # Hide axes if no data


        plt.tight_layout() # Adjust layout to prevent overlapping
        plt.show()

    def plot_merged_bar_chart(merged_df, title):
        """
        Plots a single bar chart for the combined data.
        """
        fig, ax = plt.subplots(figsize=(8, 5)) # Create a single subplot

        colors_map = {
            'Green': 'green',
            'Blue': 'blue',
            'Red': 'red',
            'Draw': 'black'
        }

        if not merged_df.empty:
            merged_color_counts = merged_df["Winning Color"].value_counts().sort_index()
            bar_colors = [colors_map.get(color, 'gray') for color in merged_color_counts.index]
            ax.bar(merged_color_counts.index, merged_color_counts.values, color=bar_colors)
            ax.set_title(title)
            ax.set_xlabel("Winning Colors")
            ax.set_ylabel("Total Counts")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
        else:
            ax.text(0.5, 0.5, "No data for this chart", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.set_title(title)
            ax.axis('off')

        plt.tight_layout()
        plt.show()


    # Call the plotting function with both sets of data
    plot_colored_bar_charts_side_by_side(first_chart_data, first_chart_title, second_chart_data, second_chart_title, third_chart_data, third_chart_title)

    # --- Data and Plot for the Fourth Chart (Merged) ---
    merged_data = pd.concat([first_chart_data, second_chart_data, third_chart_data], ignore_index=True)
    plot_merged_bar_chart(merged_data, "Total Winning Color Counts (All Plots Combined)")


else:
    print("No initial match found for the given 'Sum' and 'Winning Color' in the DataFrame. No charts generated.")

import random
import matplotlib.pyplot as plt

def get_color(n):
    if n == 49: return 'Black'
    mapping = {1: 'Red', 2: 'Blue', 0: 'Green'}
    return mapping[n % 3]

def calculate_winner(numbers):
    counts = {'Red': 0, 'Blue': 0, 'Green': 0, 'Black': 0}
    for n in numbers:
        counts[get_color(n)] += 1
    
    max_val = max(counts['Red'], counts['Blue'], counts['Green'])
    winners = [c for c, count in counts.items() if count == max_val and c != 'Black']
    
    if len(winners) > 1:
        return "Draw"
    else:
        return winners[0] if max_val >= 3 else "No Majority"

# --- User Input ---
try:
    user_sum = int(input("Enter Target Sum (e.g., 100): "))
    user_color = input("Enter Winning Color (Red, Blue, Green, or Draw): ").capitalize()

    # 1. Generate Master and 9 Random Outcomes
    winners_list = []
    
    # Search for Master Row
    found = False
    for _ in range(50000):
        selected = random.sample(range(1, 49), 6) # Excluding 49 for master to make it easier
        if sum(selected) == user_sum:
            win = calculate_winner(selected)
            if win == user_color:
                winners_list.append(win)
                found = True
                break
    
    if not found:
        print("Could not find a master row for that specific sum. Try 100-180.")
    else:
        # Generate 9 more
        for _ in range(9):
            rand_nums = random.sample(range(1, 50), 6)
            winners_list.append(calculate_winner(rand_nums))

        # 2. Prepare Data for Plotting
        categories = ['Red', 'Blue', 'Green', 'Draw', 'No Majority']
        counts = [winners_list.count(cat) for cat in categories]
        
        # Sort data for the bar chart (Highest to Lowest)
        plot_data = sorted(zip(categories, counts), key=lambda x: x[1], reverse=True)
        sorted_cats, sorted_counts = zip(*plot_data)

        # 3. Create the Chart
        color_map = {'Red': 'red', 'Blue': 'blue', 'Green': 'green', 'Draw': 'gray', 'No Majority': 'black'}
        bar_colors = [color_map[cat] for cat in sorted_cats]

        plt.bar(sorted_cats, sorted_counts, color=bar_colors)
        plt.xlabel('Winning Result')
        plt.ylabel('Frequency (Out of 10)')
        plt.title(f'Winning Color Distribution (Master: {user_color})')
        plt.show()

except ValueError:

    print("Please enter a valid number for the sum.")
