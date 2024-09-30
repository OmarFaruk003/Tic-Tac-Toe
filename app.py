import streamlit as st
import numpy as np

# Initialize player names
if 'player1' not in st.session_state:
    st.session_state.player1 = ''
if 'player2' not in st.session_state:
    st.session_state.player2 = ''

# Initialize game board
if 'board' not in st.session_state:
    st.session_state.board = np.full((3, 3), '')
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Function to check if the current player has won
def check_winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i, 0] == board[i, 1] == board[i, 2] != '':
            return board[i, 0]
        if board[0, i] == board[1, i] == board[2, i] != '':
            return board[0, i]
    
    if board[0, 0] == board[1, 1] == board[2, 2] != '':
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] != '':
        return board[0, 2]
    
    # Check if the board is full (draw)
    if '' not in board:
        return 'Draw'
    
    return None

# Function to handle a move
def make_move(row, col):
    if st.session_state.board[row, col] == '' and not st.session_state.game_over:
        st.session_state.board[row, col] = st.session_state.current_player
        st.session_state.winner = check_winner(st.session_state.board)
        
        if st.session_state.winner:
            st.session_state.game_over = True
        else:
            # Switch player
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

# Streamlit UI
st.title('Tic-Tac-Toe')

# Player name input
if not st.session_state.player1 or not st.session_state.player2:
    st.session_state.player1 = st.text_input("Enter Player 1 Name (X):", key="player1_input")
    st.session_state.player2 = st.text_input("Enter Player 2 Name (O):", key="player2_input")

    if st.button('Start Game'):
        if st.session_state.player1 and st.session_state.player2:
            st.session_state.current_player = 'X'
            st.experimental_rerun()
        else:
            st.error('Please enter both player names!')
else:
    # Display the current player
    current_player_name = st.session_state.player1 if st.session_state.current_player == 'X' else st.session_state.player2
    st.write(f"Current Player: {current_player_name} ({st.session_state.current_player})")

    # Display the game board
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            with cols[col]:
                if st.button(st.session_state.board[row, col] or ' ', key=f"{row}-{col}"):
                    make_move(row, col)

    # Display the result
    if st.session_state.game_over:
        if st.session_state.winner == 'Draw':
            st.write("It's a draw!")
        else:
            winner_name = st.session_state.player1 if st.session_state.winner == 'X' else st.session_state.player2
            st.write(f"Player {winner_name} wins!")
    
    # Restart the game
    if st.button('Restart Game'):
        st.session_state.board = np.full((3, 3), '')
        st.session_state.current_player = 'X'
        st.session_state.winner = None
        st.session_state.game_over = False
