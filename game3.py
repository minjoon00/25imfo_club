st.experimental_rerun()을 st.rerun()으로 고쳤는데도 계속 같은 질문만 나온다면, 이는 스트림릿 앱의 세션 상태(Session State) 관리 로직에 문제가 있을 가능성이 높습니다. 특히 "다음 문제" 버튼이 눌렸을 때 current_quiz_index가 제대로 업데이트되지 않거나, 업데이트되더라도 앱이 올바르게 다시 렌더링되지 않는 경우에 발생할 수 있습니다.

가장 흔한 원인은 버튼 클릭 시점과 st.rerun() 호출의 순서 또는 세션 상태 초기화 로직 때문입니다.

문제 해결 및 수정된 코드
다음은 문제를 해결하기 위해 수정된 코드입니다. 주요 변경 사항은 다음과 같습니다.

버튼 클릭 후 바로 상태 업데이트 및 st.rerun() 호출: 사용자가 O/X 버튼을 눌러 답변을 제출했을 때, 그 결과를 처리하고 나서 바로 다음 문제로 넘어가거나 결과를 표시하기 위해 st.rerun()을 호출하도록 로직을 재구성했습니다. 특히 st.button은 클릭될 때마다 다시 실행되는 특성을 이용합니다.
key 속성 활용: 스트림릿 버튼이나 위젯은 고유한 key가 없으면 특정 상황에서 오작동할 수 있습니다. 특히 같은 스크립트 내에서 여러 번 나타나거나, 조건부로 나타날 때 key를 명시적으로 부여하는 것이 좋습니다.
Python

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
if 'quiz_data_shuffled' not in st.session_state:
    st.session_state.quiz_data_shuffled = [] # 퀴즈 시작 시 섞인 데이터 저장
    st.session_state.current_quiz_index = 0
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.answer_submitted = False # 답변 제출 여부 추적
    st.session_state.last_answer_correct = False # 마지막 답변 정답 여부

st.set_page_config(layout="centered")
st.title("📚 OX 퀴즈 게임 🧠")
st.write("제시된 문장이 맞으면 **'O'**, 틀리면 **'X'**를 선택하세요!")

# 퀴즈 시작 버튼
if not st.session_state.quiz_started:
    if st.button("퀴즈 시작!", key="start_quiz_btn"):
        st.session_state.quiz_started = True
        st.session_state.current_quiz_index = 0
        st.session_state.score = 0
        st.session_state.quiz_completed = False
        st.session_state.quiz_data_shuffled = random.sample(quiz_data, len(quiz_data)) # 퀴즈 시작 시 문제 섞기
        st.session_state.answer_submitted = False
        st.rerun() # 앱을 새로고침하여 첫 번째 문제 표시

if st.session_state.quiz_started and not st.session_state.quiz_completed:
    current_quiz = st.session_state.quiz_data_shuffled[st.session_state.current_quiz_index]

    st.subheader(f"문제 {st.session_state.current_quiz_index + 1}. {current_quiz['question']}")

    # 답변이 제출되지 않은 상태일 때만 O/X 버튼 표시
    if not st.session_state.answer_submitted:
        col1, col2 = st.columns(2)
        with col1:
            o_button = st.button("O", key=f"O_btn_{st.session_state.current_quiz_index}")
        with col2:
            x_button = st.button("X", key=f"X_btn_{st.session_state.current_quiz_index}")

        user_answer = None
        if o_button:
            user_answer = "O"
        elif x_button:
            user_answer = "X"

        if user_answer:
            st.session_state.answer_submitted = True # 답변 제출됨 상태로 변경
            st.session_state.user_selected_answer = user_answer # 사용자가 선택한 답변 저장

            if user_answer == current_quiz['answer']:
                st.session_state.score += 1
                st.session_state.last_answer_correct = True
            else:
                st.session_state.last_answer_correct = False
            
            st.rerun() # 답변 결과 표시를 위해 앱 새로고침

    # 답변이 제출된 후 결과와 설명, 다음 문제 버튼 표시
    if st.session_state.answer_submitted:
        user_answer = st.session_state.user_selected_answer
        
        st.write(f"당신의 선택: **{user_answer}**")

        if st.session_state.last_answer_correct:
            st.success("정답입니다! 🎉")
        else:
            st.error(f"오답입니다. 😔 정답은 **{current_quiz['answer']}** 였습니다.")
        
        st.info(f"**정답 설명:** {current_quiz['explanation']}")

        # 다음 문제로 이동 또는 퀴즈 종료
        if st.session_state.current_quiz_index < len(st.session_state.quiz_data_shuffled) - 1:
            if st.button("다음 문제", key=f"next_quiz_btn_{st.session_state.current_quiz_index}"):
                st.session_state.current_quiz_index += 1
                st.session_state.answer_submitted = False # 다음 문제를 위해 답변 제출 상태 초기화
                st.session_state.last_answer_correct = False # 다음 문제를 위해 정답 여부 초기화
                st.rerun() # 다음 문제 표시를 위해 앱 새로고침
        else:
            st.write("---")
            st.warning("모든 퀴즈를 풀었습니다!")
            st.session_state.quiz_completed = True
            st.rerun() # 최종 결과 표시를 위해 앱 새로고침

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
        st.session_state.answer_submitted = False
        st.session_state.last_answer_correct = False
        st.rerun() # 앱을 새로고침하여 초기 상태로

st.markdown("---")
st.caption(f"현재 점수: {st.session_state.score} / {st.session_state.current_quiz_index if st.session_state.quiz_started else 0}")
st.caption("궁금한 점이 있다면 언제든지 질문해주세요!")
