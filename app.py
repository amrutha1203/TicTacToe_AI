import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Tic Tac Toe AI",
    layout="centered"
)

# Load CSS
css_path = Path(__file__).parent / "static" / "style.css"

with open(css_path, "r", encoding="utf-8") as file:
    css = file.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


# -----------------------------
# Game state
# -----------------------------

if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "message" not in st.session_state:
    st.session_state.message = "Your Turn"

if "game_over" not in st.session_state:
    st.session_state.game_over = False

board = st.session_state.board


# -----------------------------
# Check winner
# -----------------------------

def check():
    winning_positions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for position in winning_positions:
        a = position[0]
        b = position[1]
        c = position[2]

        if board[a] != "":
            if board[a] == board[b] == board[c]:
                return board[a]

    if "" not in board:
        return "Draw"

    return None


# -----------------------------
# Find winning move
# -----------------------------

def find_move(player):
    for i in range(9):
        if board[i] == "":
            board[i] = player

            result = check()

            board[i] = ""

            if result == player:
                return i

    return None


# -----------------------------
# Minimax with Alpha-Beta
# -----------------------------

def minimax(depth, maximizing, alpha, beta):
    result = check()

    if result == "O":
        return 10 - depth

    if result == "X":
        return depth - 10

    if result == "Draw":
        return 0

    if maximizing:
        best_score = -1000

        for i in range(9):
            if board[i] == "":
                board[i] = "O"

                score = minimax(
                    depth + 1,
                    False,
                    alpha,
                    beta
                )

                board[i] = ""

                best_score = max(best_score, score)

                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = 1000

        for i in range(9):
            if board[i] == "":
                board[i] = "X"

                score = minimax(
                    depth + 1,
                    True,
                    alpha,
                    beta
                )

                board[i] = ""

                best_score = min(best_score, score)

                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score


# -----------------------------
# Get AI move
# -----------------------------

def get_ai_move():

    # AI winning move
    move = find_move("O")

    if move is not None:
        return move

    # Block player's winning move
    move = find_move("X")

    if move is not None:
        return move

    # Minimax
    best_score = -1000
    best_move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"

            score = minimax(
                0,
                False,
                -1000,
                1000
            )

            board[i] = ""

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# -----------------------------
# Player move
# -----------------------------

def player_move(position):

    if st.session_state.game_over:
        return

    if board[position] != "":
        st.session_state.message = "Position already selected!"
        return

    # Player X
    board[position] = "X"

    result = check()

    if result == "X":
        st.session_state.message = "You Win!"
        st.session_state.game_over = True
        return

    if result == "Draw":
        st.session_state.message = "Game Draw!"
        st.session_state.game_over = True
        return

    # AI O
    move = get_ai_move()

    if move is not None:
        board[move] = "O"

    result = check()

    if result == "O":
        st.session_state.message = "AI Wins!"
        st.session_state.game_over = True

    elif result == "Draw":
        st.session_state.message = "Game Draw!"
        st.session_state.game_over = True

    else:
        st.session_state.message = "Your Turn"


# -----------------------------
# Restart
# -----------------------------

def restart():
    st.session_state.board = [""] * 9
    st.session_state.message = "Your Turn"
    st.session_state.game_over = False


# -----------------------------
# Title
# -----------------------------

st.markdown(
    """
    <h1 class="game-title">TIC TAC TOE</h1>

    <p class="players">You = X || AI = O</p>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Message
# -----------------------------

st.markdown(
    f"""
    <h3 class="game-message">
        {st.session_state.message}
    </h3>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Game board
# -----------------------------

for row in range(3):

    columns = st.columns(
        3,
        gap="small"
    )

    for col in range(3):

        position = row * 3 + col

        with columns[col]:

            if board[position] == "":

                if st.button(
                    " ",
                    key=f"cell_{position}",
                    use_container_width=False
                ):
                    player_move(position)
                    st.rerun()

            else:

                st.markdown(
                    f"""
                    <div class="cell {board[position]}">
                        {board[position]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# -----------------------------
# Small centered Restart button
# -----------------------------

with st.container(key="restart-container"):

    if st.button(
        "Restart",
        key="restart",
        use_container_width=False
    ):
        restart()
        st.rerun()