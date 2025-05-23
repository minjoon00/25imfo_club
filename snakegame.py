import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# --- 게임 설정 ---
BOARD_SIZE = 10
CELL_SIZE = 30 # Matplotlib plot에서 셀 크기 (시각화용)

# 색상 정의
COLOR_BACKGROUND = 'black'
COLOR_SNAKE = 'lime'
COLOR_FOOD = 'red'

# --- 초기 게임 상태 설정 함수 ---
def init_game_state():
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2)] # 초기 지렁이 위치 (중앙)
    st.session_state.direction = 'right' # 초기 방향
    st.session_state.food = generate_food_position()

# --- 먹이 생성 함수 ---
def generate_food_position():
    while True:
        food_pos = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
        if food_pos not in st.session_state.snake:
            return food_pos

# --- 게임 보드 그리기 함수 ---
def draw_board():
    fig, ax = plt.subplots(figsize=(BOARD_SIZE, BOARD_SIZE))
    ax.set_xlim(-0.5, BOARD_SIZE - 0.5)
    ax.set_ylim(-0.5, BOARD_SIZE - 0.5)
    ax.set_xticks(np.arange(-0.5, BOARD_SIZE, 1))
    ax.set_yticks(np.arange(-0.5, BOARD_SIZE, 1))
    ax.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5)
    ax.set_facecolor(COLOR_BACKGROUND) # 배경색 설정

    # 지렁이 그리기
    for segment in st.session_state.snake:
        rect = plt.Rectangle((segment[0] - 0.5, segment[1] - 0.5), 1, 1, color=COLOR_SNAKE)
        ax.add_patch(rect)

    # 먹이 그리기
    food_x, food_y = st.session_state.food
    rect = plt.Rectangle((food_x - 0.5, food_y - 0.5), 1, 1, color=COLOR_FOOD)
    ax.add_patch(rect)

    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    plt.gca().set_aspect('equal', adjustable='box')
    st.pyplot(fig)
    plt.close(fig) # 메모리 누수 방지

# --- 지렁이 이동 및 게임 로직 처리 함수 ---
def move_snake():
    if st.session_state.game_over:
        return

    head_x, head_y = st.session_state.snake[0]
    direction = st.session_state.direction

    if direction == 'up':
        new_head = (head_x, head_y - 1)
    elif direction == 'down':
        new_head = (head_x, head_y + 1)
    elif direction == 'left':
        new_head = (head_x - 1, head_y)
    elif direction == 'right':
        new_head = (head_x + 1, head_y)
    else:
        return # 방향이 설정되지 않으면 이동하지 않음

    # 벽 충돌 감지
    if not (0 <= new_head[0] < BOARD_SIZE and 0 <= new_head[1] < BOARD_SIZE):
        st.session_state.game_over = True
        return

    # 몸통 충돌 감지
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head) # 새 머리 추가

    # 먹이 먹었는지 확인
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = generate_food_position() # 새 먹이 생성
    else:
        st.session_state.snake.pop() # 꼬리 제거 (먹지 않았으면)

# --- 방향 설정 함수 ---
def set_direction(new_direction):
    if st.session_state.game_over:
        return

    current_dir = st.session_state.direction
    # 반대 방향으로 즉시 전환 방지
    if (new_direction == 'up' and current_dir == 'down') or \
       (new_direction == 'down' and current_dir == 'up') or \
       (new_direction == 'left' and current_dir == 'right') or \
       (new_direction == 'right' and current_dir == 'left'):
        pass # 허용하지 않음
    else:
        st.session_state.direction = new_direction
        move_snake() # 방향 설정 후 바로 한 칸 이동

# --- Streamlit 앱 메인 함수 ---
def main():
    st.set_page_config(layout="centered", page_title="간단 지렁이 게임")
    st.title("🐍 간단 지렁이 게임")

    # 세션 상태 초기화
    if 'game_over' not in st.session_state:
        init_game_state()

    st.sidebar.header("조작")
    col1, col2, col3 = st.sidebar.columns(3)

    with col2:
        if st.button("⬆️", key="up_btn"):
            set_direction('up')
    with col1:
        if st.button("⬅️", key="left_btn"):
            set_direction('left')
    with col3:
        if st.button("➡️", key="right_btn"):
            set_direction('right')
    with col2:
        if st.button("⬇️", key="down_btn"):
            set_direction('down')

    st.sidebar.markdown("---")
    if st.sidebar.button("게임 재시작", key="restart_btn"):
        init_game_state()
        st.rerun()

    st.header(f"점수: {st.session_state.score}")

    draw_board()

    if st.session_state.game_over:
        st.error("게임 오버!")
        st.balloons() # 게임 오버 시 풍선 효과

    st.markdown("---")
    st.info("이 게임은 Streamlit의 특성상 버튼 클릭으로 지렁이가 한 칸씩 이동합니다.")
    st.info("더 복잡한 실시간 게임은 JavaScript를 포함하는 Streamlit Components를 고려해보세요.")

if __name__ == "__main__":
    main()
