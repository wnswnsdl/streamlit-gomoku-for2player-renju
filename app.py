import streamlit as st

BOARD_SIZE = 15
ALPHABETS = [chr(i) for i in range(65, 65 + BOARD_SIZE)]  # A~O

# 세션 상태 초기화
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"  # 흑 먼저
    st.session_state.winner = None

st.title("🕹️ 렌주룰 오목 게임 (15x15)")

# 승리 조건 체크 함수
def check_win(x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        # 양쪽 방향 체크
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

# 게임판 출력
for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE + 1)  # +1은 왼쪽 알파벳
    cols[0].write(f"**{ALPHABETS[row]}**")
    for col in range(BOARD_SIZE):
        cell = st.session_state.board[row][col]
        if cell or st.session_state.winner:
            cols[col + 1].write(cell or "")
        else:
            if cols[col + 1].button(" ", key=f"{row}_{col}"):
                if st.session_state.winner:
                    continue
                # 착수
                st.session_state.board[row][col] = st.session_state.current_player
                # 승리 확인
                if check_win(col, row, st.session_state.current_player):
                    st.session_state.winner = st.session_state.current_player
                    st.success(f"{st.session_state.current_player} 승리!")
                else:
                    st.session_state.current_player = "⚪" if st.session_state.current_player == "⚫" else "⚫"
                st.rerun()

# 상단 숫자 헤더
header_cols = st.columns(BOARD_SIZE + 1)
header_cols[0].write(" ")  # 왼쪽 빈칸
for i in range(BOARD_SIZE):
    header_cols[i + 1].write(f"**{i + 1}**")

# 상태 출력
if not st.session_state.winner:
    st.write(f"👉 현재 턴: {st.session_state.current_player}")

# 리셋 버튼
if st.button("🔄 게임 리셋"):
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "⚫"
    st.session_state.winner = None
    st.rerun()
