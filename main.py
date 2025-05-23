import streamlit as st

# MBTI 궁합 데이터 (위에서 제안한 딕셔너리 사용)
mbti_best_friends = {
    "ISTJ": ["ESFP", "ESTP"],
    "ISFJ": ["ESFP", "ESTP"],
    "INFJ": ["ENFP", "ENTP"],
    "INTJ": ["ENFP", "ENTP"],
    "ISTP": ["ESFJ", "ENFJ"],
    "ISFP": ["ESTJ", "ENTJ"],
    "INFP": ["ENFJ", "ENTJ"],
    "INTP": ["ESFJ", "ENFJ"],
    "ESTP": ["ISFJ", "ISTJ"],
    "ESFP": ["ISTJ", "ISFJ"],
    "ENFP": ["INFJ", "INTJ"],
    "ENTP": ["INFJ", "INTJ"],
    "ESTJ": ["ISFP", "INTP"],
    "ESFJ": ["ISTP", "INTP"],
    "ENFJ": ["INFP", "ISFP"],
    "ENTJ": ["INFP", "ISFP"]
}

# MBTI 유형 설명 (간단한 예시, 필요에 따라 더 추가)
mbti_descriptions = {
    "ISTJ": "현실적이고 책임감이 강한 사람",
    "ESFP": "활동적이고 사교적인 사람",
    # ... 모든 MBTI 유형에 대한 설명 추가
}


st.set_page_config(layout="centered") # 페이지 레이아웃 설정 (선택 사항)

st.title("💖 MBTI 베프 찾기 앱 💖")
st.write("당신의 MBTI를 선택하고, 최고의 베프 유형을 찾아보세요!")

# 사용자 MBTI 선택
mbti_types = sorted(list(mbti_best_friends.keys()))
selected_mbti = st.selectbox("당신의 MBTI 유형을 선택하세요:", mbti_types)

if selected_mbti:
    st.write(f"---")
    st.subheader(f"✨ 당신의 MBTI는 **{selected_mbti}** 이군요!")

    # 선택된 MBTI에 대한 설명 표시 (선택 사항)
    if selected_mbti in mbti_descriptions:
        st.info(f"**{selected_mbti}**: {mbti_descriptions[selected_mbti]}")

    st.subheader(f"🎉 **{selected_mbti}**와(과) 잘 맞는 베프 유형은 다음과 같아요!")

    best_friends = mbti_best_friends.get(selected_mbti, [])

    if best_friends:
        for bf_type in best_friends:
            st.success(f"- **{bf_type}**")
            if bf_type in mbti_descriptions:
                st.write(f"  > *{mbti_descriptions[bf_type]}*")
            st.write("") # 줄 간격
    else:
        st.warning("선택하신 MBTI 유형에 대한 베프 정보가 아직 없습니다. 😅")

st.markdown("---")
st.caption("이 앱은 일반적인 MBTI 궁합 정보를 기반으로 하며, 개인의 실제 성격과 다를 수 있습니다.")
st.caption("궁합 정보는 참고용이며, 더 자세한 내용은 전문 자료를 참고해주세요.")
