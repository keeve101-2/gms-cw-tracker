import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Config
start_date = datetime(2025, 6, 11)  # Wednesday
end_date = datetime(2025, 9, 23)  # Last week inclusive
check_in_cutoff = datetime(2025, 7, 16)  # 200 points starts here

# Generate weekly date ranges (Weds to Tues)
weeks = []
current_start = start_date
while current_start <= end_date:
    current_end = current_start + timedelta(days=6)
    weeks.append((current_start, current_end))
    current_start += timedelta(days=7)

st.set_page_config(layout="wide")
st.title("CW Tracker")
st.caption("Tracks your check-ins and points from 11 Jun to 23 Sept 2025")

bosses_points = {
    "cygnus": {"easy": 50, "normal": 100},
    "zakum": {"chaos": 100},
    "hilla": {"hard": 50},
    "pink bean": {"hard": 100},
    "pierre": {"chaos": 100},
    "von bon": {"chaos": 100},
    "crimson queen": {"chaos": 100},
    "magnus": {"hard": 200},
    "vellum": {"chaos": 200},
    "papulatus": {"chaos": 250},
    "lotus": {"normal": 350, "hard": 1500},
    "damien": {"normal": 350, "hard": 1500},
    "guardian angel slime": {"normal": 500, "chaos": 2500},
    "lucid": {"easy": 500, "normal": 1000, "hard": 2000},
    "will": {"easy": 500, "normal": 1000, "hard": 2500},
    "gloom": {"normal": 1000, "chaos": 2500},
    "verus hilla": {"normal": 2000, "hard": 3000},
    "darknell": {"normal": 1000, "hard": 3000},
}

with st.container(border=True):
    st.markdown("## Boss Selector")
    st.caption("Choose the difficulties you cleared for each boss")

# Store results
    selected_difficulties = {}
    boss_list = [(key, bosses_points[key]) for key in bosses_points.keys()]

    cols_per_row_bosses = 5
    for i in range(0, len(boss_list), cols_per_row_bosses):
        cols = st.columns(cols_per_row_bosses)
        
        for col_num, col in enumerate(cols):
            with col:
                if i+col_num < len(boss_list):
                    boss_label, difficulties = boss_list[i+col_num]
                    options = list(difficulties.keys())
                    selected = st.pills(
                        label=" ".join([label.capitalize() for label in boss_label.split()]),
                        options=[option.capitalize() for option in options],
                        selection_mode="multi",
                        format_func=lambda x: x,
                        key=f"pills_{boss_label}"
                    )
                    if selected != []:
                        selected_difficulties[boss_label] = selected

    total_boss_points = 0
# Display selection summary
    if selected_difficulties:
        # st.markdown("### Selected Boss Clears")
        for boss, diffs in selected_difficulties.items():
            points = sum(bosses_points[boss][d.lower()] for d in diffs)
            total_boss_points += points
            diffs_str = ", ".join(d.title() for d in diffs)
            # st.write(f"**{boss.title()}** — {diffs_str} ({points} pts)")

    st.markdown(f"## Boss Points: `{total_boss_points}`")


st.markdown("## Check-ins")
with st.container(border=True):
# Collect check-insV
    check_in_data = []
    cols_per_row_check_ins= 5
    total_check_in_points = 0

    for i in range(0, len(weeks), cols_per_row_check_ins):
        cols = st.columns(cols_per_row_check_ins)
        
        for col_num, col in enumerate(cols):
            with col:
                if i+col_num < len(weeks):
                    week_start, week_end = weeks[i+col_num]
                    st.markdown(
                        f"**Week {i+col_num+1}: {week_start.strftime('%d %b')} – {week_end.strftime('%d %b')}**"
                    )
                    check_ins = st.radio(
                        f"Number of check-ins (Week {i+col_num+1})",
                        options=[0, 1, 2, 3, 4, 5],
                        index=0,
                        horizontal=True,
                        key=f"check_ins_{i+col_num}"
                    )
                    points_per_check_in = 100 if week_start < check_in_cutoff else 200
                    weekly_points = min(check_ins, 5) * points_per_check_in
                    check_in_data.append(
                        {
                            "Week Start": week_start.strftime("%d %b"),
                            "Week End": week_end.strftime("%d %b"),
                            "Check-ins": check_ins,
                            "Points per Check-in": points_per_check_in,
                            "Weekly Points": weekly_points,
                        }
                    )
                    

# Display summary
    df = pd.DataFrame(check_in_data)

    total_check_in_points = df["Weekly Points"].sum()
    st.markdown(f"## Total Check-in Points: `{total_check_in_points}`")
    

st.markdown("## Level Points")

with st.container(border=True):
    level_checkpoints = [260, 265, 270, 275, 280]
    level_checkpoints_points = [1000, 2000, 3000, 5000, 7000]
    total_level_checkpoint_points = 0 
    selected_levels = st.pills(
        label="Level Points",
        options=[f"{level}" for level in level_checkpoints],
        selection_mode="multi",
        format_func=lambda x: x,
        key="pills_level_points"
    )
    
    if selected_levels != []:
        for level in selected_levels:
            total_level_checkpoint_points += level_checkpoints_points[level_checkpoints.index(int(level))]

    st.markdown(f"## Total Level Points: `{total_level_checkpoint_points}`")

st.markdown(f"## Total Points: `{total_boss_points + total_check_in_points + total_level_checkpoint_points}`")
