import streamlit as st

BOARD_SIZE = 15
ALPHABETS = [chr(i) for i in range(65, 65 + BOARD_SIZE)]

# 바둑판 배경 스타일 삽입
st.markdown("""
    <style>
    body {
        background-color: #f5deb3;  /* 연한 나무색 */
    }
    .stButton>button {
        border: 1px solid #444444 !important;
        border-radius: 50% !important;
        height: 2em !important;
        width: 2em !important;
        padding: 0 !important;
        font-size: 20px !important;
        background-color: #deb887 !important;  /* 밝은 황갈색 */
    }
    .cell {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 2em;
        width: 2em;
        background-color: #f5deb3;  /* 연한 바둑판 색 */
        border: 1px solid #aaaaaa;
        font-size: 20px;
    }
    .highlight {
        color: red;
    }
    </style>
""", unsafe_allow_html=True)

# 상태 초기화
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"
    st.session_state.winner = None
    st.session_state.win_coords = []

st.title("🪵 렌주룰 오목 게임 (바둑판 스타일 + 33 금지 + 승리 하이라이트)")

# 헤더
header = st.columns(BOARD_SIZE + 1)
header[0].write(" ")
for i in range(BOARD_SIZE):
    header[i + 1].markdown(f"<div style='text-align:center'><b>{i+1}</b></div>", unsafe_allow_html=True)

# 승리 조건 검사
def check_win(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        win_path = [(x, y)]
        for dir in [1, -1]:
            nx, ny = x, y
            while True:
                nx += dx * dir
                ny += dy * dir
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and st.session_state.board[ny][nx] == player:
                    count += 1
                    win_path.append((nx, ny))
                else:
                    break
        if count >= 5:
            return win_path
    return []

# 33 금지 확인
def is_open_three(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    open_three_count = 0
    temp = [row[:] for row in st.session_state.board]
    temp[y][x] = player

    for dx, dy in directions:
        line = ""
        for i in range(-4, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                line += temp[ny][nx] if temp[ny][nx] else "."
            else:
                line += "X"
        if line.count("⚫⚫⚫") == 1:
            idx = line.find("⚫⚫⚫")
            if idx > 0 and idx + 3 < len(line):
                if line[idx - 1] == "." and line[idx + 3] == ".":
                    open_three_count += 1
    return open_three_count >= 2

# 바둑판 출력
for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE + 1)
    cols[0].markdown(f"<div style='text-align:center'><b>{ALPHABETS[row]}</b></div>", unsafe_allow_html=True)
    for col in range(BOARD_SIZE):
        symbol = st.session_state.board[row][col]
        is_win = (col, row) in st.session_state.win_coords

        if is_win:
            display = "🔴"
            cols[col + 1].markdown(f"<div class='cell highlight'>{display}</div>", unsafe_allow_html=True)
        elif symbol:
            display = symbol
            cols[col + 1].markdown(f"<div class='cell'>{display}</div>", unsafe_allow_html=True)
        elif not st.session_state.winner:
            if cols[col + 1].button(" ", key=f"{row}-{col}"):
                if st.session_state.current_player == "⚫" and is_open_three(col, row, "⚫"):
                    st.warning("⚠️ 흑돌은 33 금지입니다!")
                    st.rerun()

                st.session_state.board[row][col] = st.session_state.current_player
                win_path = check_win(col, row, st.session_state.current_player)
                if win_path:
                    st.session_state.winner = st.session_state.current_player
                    st.session_state.win_coords = win_path
                    st.success(f"{st.session_state.current_player} 승리!")
                else:
                    st.session_state.current_player = "⚪" if st.session_state.current_player == "⚫" else "⚫"
                st.rerun()
        else:
            cols[col + 1].markdown("<div class='cell'></div>", unsafe_allow_html=True)

# 상태
if not st.session_state.winner:
    st.write(f"현재 턴: {st.session_state.current_player}")
else:
    st.write(f"🎉 게임 종료")

# 리셋
if st.button("🔄 게임 리셋"):
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"
    st.session_state.winner = None
    st.session_state.win_coords = []
    st.rerun()
