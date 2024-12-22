import streamlit as st

st.title("Flügelschlag - Punktezähler")


num_players = st.number_input("Anzahl Spieler", value=4, step=1)

columns = st.columns(num_players)


def calc_nectar_points(player_index: int, nectar_type: str) -> int:
    firsts = [
        i
        for i in range(num_players)
        if "Erster" == st.session_state[f"nectar_{nectar_type}_{i}"]
    ]
    seconds = [
        i
        for i in range(num_players)
        if "Zweiter" == st.session_state[f"nectar_{nectar_type}_{i}"]
    ]

    if player_index in firsts:
        if len(firsts) == 1:
            return 5
        if len(firsts) >= 2:
            return 7 // len(firsts)

    if player_index in seconds and len(firsts) == 1:
        return 2 // len(seconds)
    return 0


def calc_victory(player_index: int, points: list[int]) -> str:
    sorted_points = sorted(points, reverse=True)
    if points[player_index] == sorted_points[0]:
        return "🥇 "
    if points[player_index] == sorted_points[1]:
        return "🥈 "
    if points[player_index] == sorted_points[2]:
        return "🥉 "
    return ""


for index in range(num_players):
    columns[index].text_input(f"Spieler {index+1}", key=f"name_{index}")
    columns[index].number_input("Vögel", value=0, step=1, key=f"birds_{index}")
    columns[index].number_input("Bonuspunkte", value=0, step=1, key=f"bonus_{index}")
    columns[index].number_input("Rundenziele", value=0, step=1, key=f"goal_{index}")
    columns[index].number_input("Eier auf Vögeln", value=0, step=1, key=f"eggs_{index}")
    columns[index].number_input(
        "Futter auf Vögeln", value=0, step=1, key=f"food_{index}"
    )
    columns[index].number_input(
        "Karten unter Vögeln", value=0, step=1, key=f"under_{index}"
    )
    options = ["Erster", "Zweiter"]
    columns[index].pills(
        "Nektar im Wald", options, selection_mode="single", key=f"nectar_green_{index}"
    )
    columns[index].pills(
        "Nektar in Steppe",
        options,
        selection_mode="single",
        key=f"nectar_yellow_{index}",
    )
    columns[index].pills(
        "Nektar im Wasser", options, selection_mode="single", key=f"nectar_blue_{index}"
    )

nectar_points = [0] * num_players
for index in range(num_players):
    nectar_points[index] = (
        calc_nectar_points(index, "green")
        + calc_nectar_points(index, "yellow")
        + calc_nectar_points(index, "blue")
    )
    columns[index].subheader(f"{nectar_points[index]}")
st.divider()
columns = st.columns(num_players)

total_points = [0] * num_players
for index in range(num_players):
    total_points[index] = (
        st.session_state[f"birds_{index}"]
        + st.session_state[f"bonus_{index}"]
        + st.session_state[f"goal_{index}"]
        + st.session_state[f"eggs_{index}"]
        + st.session_state[f"food_{index}"]
        + st.session_state[f"under_{index}"]
        + nectar_points[index]
    )

for index in range(num_players):
    columns[index].caption(f"Punkte {st.session_state[f'name_{index}']}")
    columns[index].header(f"{calc_victory(index, total_points)}{total_points[index]}")
