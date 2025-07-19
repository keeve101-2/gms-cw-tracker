import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
# Config
start_date = datetime(2025, 6, 11)  # Wednesday
end_date = datetime(2025, 9, 23)  # Last week inclusive
check_in_cutoff = datetime(2025, 7, 16)  # 200 points starts here

tiers = ["-", "Bronze", "Silver", "Gold", "Emerald", "Diamond", "Challenger"]
tiers_points = [0, 5000, 10000, 15000, 20000, 30000, 40000]

# Generate weekly date ranges (Weds to Tues)
weeks = []
current_start = start_date
while current_start <= end_date:
    current_end = current_start + timedelta(days=6)
    weeks.append((current_start, current_end))
    current_start += timedelta(days=7)

st.title("GMS Challenger World Points Calculator")

tab1, tab2, tab3 = st.tabs(["Boss Missions", "Hunting Missions", "Level Missions"])

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

with tab1:
    with st.container(border=True):
        # Store results
        selected_difficulties = {}
        boss_list = [(key, bosses_points[key]) for key in bosses_points.keys()]

        cols_per_row_bosses = 5
        for i in range(0, len(boss_list), cols_per_row_bosses):
            cols = st.columns(cols_per_row_bosses)

            for col_num, col in enumerate(cols):
                with col:
                    if i + col_num < len(boss_list):
                        boss_label, difficulties = boss_list[i + col_num]
                        boss_label = boss_label.title()
                        options = list(difficulties.keys())
                        selected = st.pills(
                            label=boss_label,
                            options=[
                                f"{option.capitalize()}: {difficulties[option]:,} points"
                                for option in options
                            ],
                            selection_mode="multi",
                            format_func=lambda x: x,
                            key=f"pills_{boss_label}",
                        )
                        if selected != []:
                            selected_difficulties[boss_label] = selected

        total_boss_points = 0
        # Display selection summary
        if selected_difficulties:
            # st.markdown("### Selected Boss Clears")
            for boss, diffs in selected_difficulties.items():
                points = sum(
                    bosses_points[boss.lower()][d.split(":")[0].lower()] for d in diffs
                )
                total_boss_points += points
                diffs_str = ", ".join(d.title() for d in diffs)
                # st.write(f"**{boss.title()}** — {diffs_str} ({points} pts)")

with tab2:
    with st.container(border=True):
        # Collect check-insV
        check_in_data = []
        cols_per_row_check_ins = 5
        total_check_in_points = 0

        for i in range(0, len(weeks), cols_per_row_check_ins):
            cols = st.columns(cols_per_row_check_ins)

            for col_num, col in enumerate(cols):
                with col:
                    if i + col_num < len(weeks):
                        week_start, week_end = weeks[i + col_num]
                        points_per_check_in = (
                            100 if week_start < check_in_cutoff else 200
                        )
                        check_ins = st.radio(
                            f"{week_start.strftime('%d %b')} – {week_end.strftime('%d %b')}",
                            options=[0, 1, 2, 3, 4, 5],
                            index=0,
                            horizontal=True,
                            key=f"check_ins_{i+col_num}",
                        )
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


with tab3:
    with st.container(border=True):
        level_checkpoints = [260, 265, 270, 275, 280]
        level_checkpoints_points = [1000, 2000, 3000, 5000, 7000]
        total_level_checkpoint_points = 0
        selected_levels = st.pills(
            label="Level Points",
            options=[f"{level}: {points:,} points" for level, points in zip(level_checkpoints, level_checkpoints_points)],
            selection_mode="multi",
            format_func=lambda x: x,
            key="pills_level_points",
        )

        if selected_levels != []:
            for level in selected_levels:
                total_level_checkpoint_points += level_checkpoints_points[
                    level_checkpoints.index(int(level.split(":")[0]))
                ]

total_points = total_boss_points + total_check_in_points + total_level_checkpoint_points

current_tier = "-"
for tier, points in zip(tiers, tiers_points):
    if total_points >= points:
        current_tier = tier

st.markdown("## Breakdown")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Boss Points", value=f"{total_boss_points:,}")
    with col2:
        st.metric(label="Check-in Points", value=f"{total_check_in_points:,}")
    with col3:
        st.metric(label="Level Points", value=f"{total_level_checkpoint_points:,}")


st.markdown("## Summary")

with st.container(border=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Current Tier", value=current_tier)

    with col2:
        st.metric(label="Total Points", value=f"{total_points:,}")

    with col3:
        if current_tier != tiers[-1]:
            next_tier_points = tiers_points[tiers.index(current_tier) + 1]
            st.metric(
                label="Points to Next Tier",
                value=f"{next_tier_points - total_points:,}",
            )
            progress = total_points / next_tier_points
            st.progress(progress)
        else:
            st.metric(label="Max Tier Reached", value="🎉")
