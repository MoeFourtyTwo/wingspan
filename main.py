import random
import time

import pandas as pd
import streamlit as st

for prop in st.session_state:
    if prop.startswith("p_"):
        st.session_state[prop] = st.session_state[prop]

if st.session_state.get("p_state") is None:
    st.session_state["p_state"] = 1

if st.session_state.get("p_num_players") is None:
    st.session_state["p_num_players"] = 4


def previous_state():
    st.session_state["p_state"] -= 1


def next_state():
    st.session_state["p_state"] += 1


def stream_string(string: str):
    for char in string:
        time.sleep(0.05)
        yield char


def generate_header():
    st.title("🪽 Flügelschlag - Punktezähler 🦉")
    back_col, _, reset_col = st.columns([1, 4, 1])

    back_col.button("Zurück", use_container_width=True, on_click=previous_state)
    reset_col.button("Reset", use_container_width=True, on_click=st.session_state.clear)
    st.divider()


def generate_footer():
    st.divider()
    _, _, next_col = st.columns([1, 4, 1])

    next_col.button("Weiter", use_container_width=True, on_click=next_state)


def collect_player_data():
    st.number_input(
        "Anzahl Spieler", value=4, step=1, min_value=1, max_value=6, key="p_num_players"
    )

    for i in range(st.session_state["p_num_players"]):
        st.text_input(
            f"Spieler {i+1}",
            value=st.session_state.get(f"p_name_{i}"),
            key=f"p_name_{i}",
        )


def debug():
    st.write(st.session_state)


def animate_starting_player():
    with st.spinner("Wähle einen zufälligen Spieler aus..."):
        time.sleep(2)
        starting_player_index = random.randint(0, st.session_state["p_num_players"] - 1)

    _, mid, _ = st.columns([2, 2, 2])
    mid.write_stream(stream_string("Der Startspieler ist..."))
    mid.subheader(st.session_state[f"p_name_{starting_player_index}"])


def collect_bird_points():
    st.subheader("Vogelpunkte")
    for i in range(st.session_state["p_num_players"]):
        st.number_input(
            st.session_state[f"p_name_{i}"],
            value=0,
            key=f"p_bird_points_{i}",
            step=1,
            min_value=0,
        )


def collect_bonus_points():
    st.subheader("Bonuspunkte")
    for i in range(st.session_state["p_num_players"]):
        st.number_input(
            st.session_state[f"p_name_{i}"],
            value=0,
            key=f"p_bonus_points_{i}",
            step=1,
            min_value=0,
        )


def collect_goal_points():
    st.subheader("Rundenziele")
    options = ["Erster", "Zweiter", "Dritter", "Vierter"]

    columns = st.columns(4)

    for round_index in range(4):
        for index in range(st.session_state["p_num_players"]):
            columns[round_index].pills(
                f"Runde {round_index + 1} - {st.session_state[f'p_name_{index}']}",
                options,
                selection_mode="single",
                key=f"p_goal_{round_index}_{index}",
            )


def collect_egg_points():
    st.subheader("Eier auf Vögeln")
    for i in range(st.session_state["p_num_players"]):
        st.number_input(
            st.session_state[f"p_name_{i}"],
            value=0,
            key=f"p_egg_points_{i}",
            step=1,
            min_value=0,
        )


def collect_food_points():
    st.subheader("Futter auf Vögeln")
    for i in range(st.session_state["p_num_players"]):
        st.number_input(
            st.session_state[f"p_name_{i}"],
            value=0,
            key=f"p_food_points_{i}",
            step=1,
            min_value=0,
        )


def collect_cards_under_points():
    st.subheader("Karten unter Vögeln")
    for i in range(st.session_state["p_num_players"]):
        st.number_input(
            st.session_state[f"p_name_{i}"],
            value=0,
            key=f"p_card_points_{i}",
            step=1,
            min_value=0,
        )


def collect_nectar_points():
    st.subheader("Gesammelter Nektar")

    options = ["Erster", "Zweiter"]

    columns = st.columns(3)

    for field_index, name in enumerate(["Wald", "Steppe", "Wasser"]):
        for index in range(st.session_state["p_num_players"]):
            columns[field_index].pills(
                f"{name} - {st.session_state[f'p_name_{index}']}",
                options,
                selection_mode="single",
                key=f"p_nectar_{field_index}_{index}",
            )


def calc_goal_points():
    round_points = [
        [4, 1, 0, 0],
        [5, 2, 1, 0],
        [6, 3, 2, 0],
        [7, 4, 3, 0],
    ]

    for round_index in range(4):
        options = ["Erster", "Zweiter", "Dritter", "Vierter"]

        order = [[], [], [], []]

        for index in range(st.session_state["p_num_players"]):
            value = st.session_state.get(f"p_goal_{round_index}_{index}", "Vierter")
            order_index = options.index(value)
            order[order_index].append(index)

        for index, value in enumerate(order):
            if len(value) == 0:
                continue

            if len(value) > 0:
                points = sum(
                    round_points[round_index][index : index + len(value)]
                ) // len(value)

                for player_index in value:
                    st.session_state[f"p_goal_points_{round_index}_{player_index}"] = (
                        points
                    )


def calc_nectar_points():
    nectar_points = [5, 2, 0, 0]

    for field_index in range(3):
        options = ["Erster", "Zweiter"]

        order = [[], []]

        for index in range(st.session_state["p_num_players"]):
            value = st.session_state.get(f"p_nectar_{field_index}_{index}", "")
            try:
                order_index = options.index(value)
            except ValueError:
                continue
            order[order_index].append(index)

        for index, value in enumerate(order):
            if len(value) == 0:
                continue

            if len(value) > 0:
                points = sum(nectar_points[index : index + len(value)]) // len(value)

                for player_index in value:
                    st.session_state[
                        f"p_nectar_points_{field_index}_{player_index}"
                    ] = points


def zero_if_none(value):
    return value if value is not None else 0


def calculate_points():
    calc_goal_points()
    calc_nectar_points()

    for index in range(st.session_state["p_num_players"]):
        st.session_state[f"p_total_points_{index}"] = (
            zero_if_none(st.session_state.get(f"p_bird_points_{index}"))
            + zero_if_none(st.session_state.get(f"p_bonus_points_{index}"))
            + zero_if_none(st.session_state.get(f"p_goal_points_0_{index}"))
            + zero_if_none(st.session_state.get(f"p_goal_points_1_{index}"))
            + zero_if_none(st.session_state.get(f"p_goal_points_2_{index}"))
            + zero_if_none(st.session_state.get(f"p_goal_points_3_{index}"))
            + zero_if_none(st.session_state.get(f"p_egg_points_{index}"))
            + zero_if_none(st.session_state.get(f"p_food_points_{index}"))
            + zero_if_none(st.session_state.get(f"p_card_points_{index}"))
            + zero_if_none(st.session_state.get(f"p_nectar_points_0_{index}"))
            + zero_if_none(st.session_state.get(f"p_nectar_points_1_{index}"))
            + zero_if_none(st.session_state.get(f"p_nectar_points_2_{index}"))
        )


def show_points():
    calculate_points()

    player_scores = sorted(
        [
            (st.session_state[f"p_total_points_{i}"], st.session_state[f"p_name_{i}"])
            for i in range(st.session_state["p_num_players"])
        ],
        reverse=True,
    )

    order = [[]]
    pointer = -1
    emojis = ["🥇", "🥈", "🥉", ""]
    emoji_pointer = 0

    for score, player in player_scores:
        if pointer < 0:
            order[0].append((score, emojis[emoji_pointer], player))
            pointer = 0
            continue

        if score == order[pointer][0][0]:
            order[pointer].append((score, emojis[emoji_pointer], player))
        else:
            emoji_pointer += len(order[pointer])
            order.append([(score, emojis[emoji_pointer], player)])
            pointer += 1

    cols = st.columns(3)
    for players in reversed(order):
        time.sleep(1)
        for score, emoji, player in players:
            cols[0].header(emoji)
            cols[1].header(player)
            cols[2].header(score)

    st.balloons()


def show_details():
    df = pd.DataFrame(
        {
            "Spieler": [
                st.session_state[f"p_name_{i}"]
                for i in range(st.session_state["p_num_players"])
            ],
            "Vogelpunkte": [
                zero_if_none(st.session_state.get(f"p_bird_points_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Bonuspunkte": [
                zero_if_none(st.session_state.get(f"p_bonus_points_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Runde 1": [
                zero_if_none(st.session_state.get(f"p_goal_points_0_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Runde 2": [
                zero_if_none(st.session_state.get(f"p_goal_points_1_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Runde 3": [
                zero_if_none(st.session_state.get(f"p_goal_points_2_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Runde 4": [
                zero_if_none(st.session_state.get(f"p_goal_points_3_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Eier auf Vögeln": [
                zero_if_none(st.session_state.get(f"p_egg_points_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Futter auf Vögeln": [
                zero_if_none(st.session_state.get(f"p_food_points_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Karten unter Vögeln": [
                zero_if_none(st.session_state.get(f"p_card_points_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Nektar Wald": [
                zero_if_none(st.session_state.get(f"p_nectar_points_0_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Nektar Steppe": [
                zero_if_none(st.session_state.get(f"p_nectar_points_1_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Nektar Wasser": [
                zero_if_none(st.session_state.get(f"p_nectar_points_2_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
            "Summe": [
                zero_if_none(st.session_state.get(f"p_total_points_{i}"))
                for i in range(st.session_state["p_num_players"])
            ],
        }
    )
    df = df.transpose()
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)
    st.dataframe(df, use_container_width=True)


def draw():
    generate_header()
    match st.session_state["p_state"]:
        case 1:
            collect_player_data()
        case 2:
            animate_starting_player()
        case 3:
            collect_bird_points()
        case 4:
            collect_bonus_points()
        case 5:
            collect_goal_points()
        case 6:
            collect_egg_points()
        case 7:
            collect_food_points()
        case 8:
            collect_cards_under_points()
        case 9:
            collect_nectar_points()
        case 10:
            show_points()
        case 11:
            show_details()

    # debug()
    generate_footer()


draw()
