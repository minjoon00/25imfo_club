import streamlit as st
import random

# 퀴즈 데이터 (모든 질문 포함)
quiz_data = [
    # 기존 퀴즈
    {"question": "지구는 태양 주위를 돈다. (O/X)", "answer": "O", "explanation": "지구는 태양 주위를 공전합니다."},
    {"question": "대한민국의 수도는 부산이다. (O/X)", "answer": "X", "explanation": "대한민국의 수도는 서울입니다."},
    {"question": "물은 섭씨 0도에서 언다. (O/X)", "answer": "O", "explanation": "물의 어는점은 섭씨 0도입니다."},
    {"question": "파이썬은 고수준 프로그래밍 언어이다. (O/X)", "answer": "O", "explanation": "파이썬은 사람이 이해하기 쉬운 고수준 언어입니다."},
    {"question": "독도는 일본 땅이다. (O/X)", "answer": "X", "explanation": "독도는 대한민국 고유의 영토입니다."},

    # 역사/상식 퀴즈
    {"question": "세종대왕은 한글을 창제했다. (O/X)", "answer": "O", "explanation": "조선 4대 임금 세종대왕이 훈민정음을 창제했습니다."},
    {"question": "피카소는 스페인 화가이다. (O/X)", "answer": "O", "explanation": "파블로 피카소는 스페인 출신의 20세기 대표적인 화가입니다."},
    {"question": "자유의 여신상은 미국 뉴욕에 있다. (O/X)", "answer": "O", "explanation": "자유의 여신상은 프랑스가 미국 독립 100주년을 기념하여 선물한 조각상으로, 뉴욕에 위치해 있습니다."},
    {"question": "에베레스트 산은 아프리카 대륙에 있다. (O/X)", "answer": "X", "explanation": "에베레스트 산은 아시아 대륙, 히말라야 산맥에 있습니다."},
    {"question": "금강산은 북한에 있다. (O/X)", "answer": "O", "explanation": "금강산은 강원도에 위치하며, 북한 지역에 속해 있습니다."},

    # 과학/기술 퀴즈
    {"question": "지구의 70%는 물로 덮여 있다. (O/X)", "answer": "O", "explanation": "지구 표면의 약 71%가 물로 덮여 있습니다."},
    {"question": "나비는 곤충이다. (O/X)", "answer": "O", "explanation": "나비는 곤충강에 속하는 동물입니다."},
    {"question": "사람은 눈을 뜨고 재채기할 수 있다. (O/X)", "answer": "X", "explanation": "재채기를 할 때 눈을 뜨고 있기는 거의 불가능하며, 눈을 감게 됩니다."},
    {"question": "빛은 소리보다 빠르다. (O/X)", "answer": "O", "explanation": "빛의 속도는 초속 약 30만 킬로미터로, 소리의 속도보다 훨씬 빠릅니다."},
    {"question": "컴퓨터의 중앙처리장치는 CPU라고 불린다. (O/X)", "answer": "O", "explanation": "CPU는 Central Processing Unit의 약자로, 컴퓨터의 핵심 부품입니다."},

    # 재미/흥미 퀴즈
    {"question": "바나나는 나무에서 열리는 과일이다. (O/X)", "answer": "X", "explanation": "바나나는 풀의 일종인 바나나 '나무'가 아닌 바나나 '초'에서 열립니다."},
    {"question": "펭귄은 날 수 있다. (O/X)", "answer": "X", "explanation": "펭귄은 날지 못하는 새로, 수영에 능합니다."},
    {"question": "초콜릿은 강아지에게 해롭다. (O/X)", "answer": "O", "explanation": "초콜릿에 포함된 테오브로민은 강아지에게 유독할 수 있습니다."},
    {"question": "대한민국 국기에는 태극 문양이 있다. (O/X)", "answer": "O", "explanation": "대한민국 국기는 태극기이며, 중앙에 태극 문양이 있습니다."},
    {"question": "아이폰은 애플에서 만들었다. (O/X)", "answer": "O", "explanation": "아이폰은 미국의 IT 기업 애플에서 개발한 스마트폰입니다."},
]

# 세션 상태 초기화
# 'quiz_data_shuffled'는 퀴즈를 시작할 때 한 번만 섞어서 사용합니다.
if 'quiz_data_shuffled' not in st.session_state:
    st.session_state.quiz_data_shuffled = [] # 초기에는 비워둠
    st.session_state.current_quiz_index = 0
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False

st.set_page_config(layout="centered")
st.title("📚 OX 퀴즈 게임 🧠")
st.write("제시된 문장이 맞으면 **'O'**, 틀리면 **'X'**를 선택하세요!")

# 퀴즈 시작 버튼
if not st.session_state.quiz_started:
    if st.button("퀴즈 시작!"):
        st.session_state.quiz_started = True
        st.session_state.current_quiz_index = 0
        st.session_state.score = 0
        st.session_state.quiz_completed = False
        st.session_state.quiz_data_shuffled = random.sample(quiz_data, len(quiz_data)) # 퀴즈 시작 시 문제 섞기
        st.rerun() # 변경된 부분: st.experimental_rerun() -> st.rerun()

if st.session_state.quiz_started and not st.session_state.quiz_completed:
    # 현재 퀴즈 문제 가져오기
    current_quiz = st.session_state.quiz_data_shuffled[st.session_state.current_quiz_index]

    st.subheader(f"문제 {st.session_state.current_quiz_index + 1}. {current_quiz['question']}")

    # O/X 선택 버튼
    col1, col2 = st.columns(2)
    with col1:
        o_button = st.button("O", key="O_btn")
    with col2:
        x_button = st.button("X", key="X_btn")

    user_answer = None
    if o_button:
        user_answer = "O"
    elif x_button:
        user_answer = "X"

    if user_answer:
        st.write(f"당신의 선택: **{user_answer}**")
        
        if user_answer == current_quiz['answer']:
            st.success("정답입니다! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"오답입니다. 😔 정답은 **{current_quiz['answer']}** 였습니다.")
        
        st.info(f"**정답 설명:** {current_quiz['explanation']}")

        # 다음 문제로 이동 또는 퀴즈 종료
        if st.session_state.current_quiz_index < len(st.session_state.quiz_data_shuffled) - 1:
            if st.button("다음 문제", key="next_quiz_btn"):
                st.session_state.current_quiz_index += 1
                st.rerun() # 변경된 부분: st.experimental_rerun() -> st.rerun()
        else:
            st.write("---")
            st.warning("모든 퀴즈를 풀었습니다!")
            st.session_state.quiz_completed = True
            st.rerun() # 변경된 부분: st.experimental_rerun() -> st.rerun()

elif st.session_state.quiz_completed:
    st.subheader("✅ 퀴즈 결과")
    total_questions = len(st.session_state.quiz_data_shuffled)
    st.success(f"총 {total_questions}문제 중 **{st.session_state.score}**개를 맞히셨습니다!")

    if st.button("다시 시작", key="restart_btn"):
        st.session_state.current_quiz_index = 0
        st.session_state.score = 0
        st.session_state.quiz_started = False
        st.session_state.quiz_completed = False
        st.session_state.quiz_data_shuffled = [] # 섞인 퀴즈 데이터도 초기화
        st.rerun() # 변경된 부분: st.experimental_rerun() -> st.rerun()
