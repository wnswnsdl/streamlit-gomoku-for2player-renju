import streamlit as st

BOARD_SIZE = 15
ALPHABETS = [chr(i) for i in range(65, 65 + BOARD_SIZE)]  # A~O

if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"
    st.session_state.winner = None

st.title("🕹️ 렌주룰 오목 게임 (15x15 with 33 금지)")

# 좌표 표시
header = st.columns(BOARD_SIZE + 1)
header[0].write(" ")
for i in range(BOARD_SIZE):
    header[i + 1].write(f"**{i + 1}**")

# 승리 판정
def check_win(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for dir in [1, -1]:
            nx, ny = x, y
            while True:
                nx += dx * dir
                ny += dy * dir
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and st.session_state.board[ny][nx] == player:
                    count += 1
                else:
                    break
        if count >= 5:
            return True
    return False

# 열린 3 확인 (33 금지용)
def is_open_three(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    open_three_count = 0

    temp_board = [row[:] for row in st.session_state.board]
    temp_board[y][x] = player

    for dx, dy in directions:
        line = ""
        for i in range(-4, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                line += temp_board[ny][nx] if temp_board[ny][nx] else "."
            else:
                line += "X"

        patterns = ["⚫⚫⚫..", ".⚫⚫⚫.", "..⚫⚫⚫"]
        for p in patterns:
            if p in line and line.count("⚫⚫⚫") == 1:
                # 좌우에 빈칸이 있고 양쪽 막히지 않은 열린 3인지 판단
                idx = line.find(p)
                if idx > 0 and idx + len(p) < len(line) and line[idx - 1] == "." and line[idx + len(p)] == ".":
                    open_three_count += 1

    return open_three_count >= 2

# 게임판
for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE + 1)
    cols[0].write(f"**{ALPHABETS[row]}**")
    for col in range(BOARD_SIZE):
        stone = st.session_state.board[row][col]
        if stone or st.session_state.winner:
            cols[col + 1].write(stone or "")
        else:
            if cols[col + 1].button(" ", key=f"{row}-{col}"):
                if st.session_state.winner:
                    continue

                # 33 금지 체크 (흑돌만)
                if st.session_state.current_player == "⚫" and is_open_three(col, row, "⚫"):
                    st.warning("⚠️ 흑돌은 33 금지입니다!")
                    st.rerun()

                # 착수
                st.session_state.board[row][col] = st.session_state.current_player

                # 승리 판정
                if check_win(col, row, st.session_state.current_player):
                    st.session_state.winner = st.session_state.current_player
                    st.success(f"{st.session_state.current_player} 승리!")
                else:
                    st.session_state.current_player = "⚪" if st.session_state.current_player == "⚫" else "⚫"
                st.rerun()

# 상태
if not st.session_state.winner:
    st.write(f"👉 현재 턴: {st.session_state.current_player}")

# 리셋
if st.button("🔄 게임 리셋"):
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"
    st.session_state.winner = None
    st.rerun()
