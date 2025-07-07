import streamlit as st

BOARD_SIZE = 15
ALPHABETS = [chr(i) for i in range(65, 65 + BOARD_SIZE)]

# 세션 상태 초기화
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"
    st.session_state.winner = None
    st.session_state.win_coords = []  # 승리선 좌표

st.title("♟️ 렌주룰 오목 게임 (15x15, 승리선 표시 포함)")

# 숫자 헤더 출력
header = st.columns(BOARD_SIZE + 1)
header[0].write(" ")
for i in range(BOARD_SIZE):
    header[i + 1].markdown(f"<div style='text-align:center'><b>{i+1}</b></div>", unsafe_allow_html=True)

# 승리 체크 함수 (좌표 반환 포함)
def check_win(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        win_positions = [(x, y)]

        for dir in [1, -1]:
            nx, ny = x, y
            while True:
                nx += dx * dir
                ny += dy * dir
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and st.session_state.board[ny][nx] == player:
                    count += 1
                    win_positions.append((nx, ny))
                else:
                    break
        if count >= 5:
            return win_positions
    return []

# 열린 3 패턴 체크 (흑돌만 제한)
def is_open_three(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    count_open_threes = 0
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
                    count_open_threes += 1
    return count_open_threes >= 2

# 바둑판 그리기
for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE + 1)
    cols[0].markdown(f"<div style='text-align:center'><b>{ALPHABETS[row]}</b></div>", unsafe_allow_html=True)
    for col in range(BOARD_SIZE):
        stone = st.session_state.board[row][col]
        btn_style = "height:2em;width:2em;padding:0;border-radius:50%;font-size:20px;"
        key = f"{row}-{col}"

        if (col, row) in st.session_state.win_coords:
            symbol = "🔴"
            cols[col + 1].markdown(f"<div style='{btn_style}text-align:center'>{symbol}</div>", unsafe_allow_html=True)
        elif stone:
            symbol = stone
            cols[col + 1].markdown(f"<div style='{btn_style}text-align:center'>{symbol}</div>", unsafe_allow_html=True)
        elif not st.session_state.winner:
            if cols[col + 1].button(" ", key=key):
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
            cols[col + 1].markdown(f"<div style='{btn_style}'></div>", unsafe_allow_html=True)

# 상태 표시
if not st.session_state.winner:
    st.write(f"현재 턴: {st.session_state.current_player}")
else:
    st.write(f"🏁 게임 종료")

# 리셋 버튼
if st.button("🔄 게임 리셋"):
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"
    st.session_state.winner = None
    st.session_state.win_coords = []
    st.rerun()
