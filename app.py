import streamlit as st
from collections import defaultdict
from datetime import datetime
import pandas as pd

def 날짜로_요일_변환(날짜문자열, 포맷="%Y-%m-%d"):
    요일_목록 = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    날짜객체 = datetime.strptime(날짜문자열, 포맷)
    요일_인덱스 = 날짜객체.weekday()
    return 요일_목록[요일_인덱스]

def 지출_분석_및_경고(전체_자산, 지출_데이터):
    지출_합계 = defaultdict(int)
    for 날짜, 금액 in 지출_데이터:
        요일 = 날짜로_요일_변환(날짜)
        지출_합계[요일] += 금액

    요일_순서 = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    표_데이터 = []
    총_지출 = 0

    for 요일 in 요일_순서:
        금액 = 지출_합계[요일]
        표_데이터.append([요일, 금액])
        총_지출 += 금액

    df = pd.DataFrame(표_데이터, columns=["요일", "총 지출"])
    st.subheader("📊 요일별 지출 현황")
    st.table(df.style.format({"총 지출": "{:,}원"}))

    st.markdown(f"**전체 자산:** {전체_자산:,.0f}원")
    st.markdown(f"**총 지출:** {총_지출:,.0f}원")

    if 총_지출 > 전체_자산 * 0.5:
        st.error("⚠️ 전체 자산의 절반 이상을 지출했습니다!")
    else:
        st.success("✅ 지출이 자산의 절반 이하입니다. 건전한 소비입니다.")

# Streamlit 인터페이스
st.title("💸 요일별 지출 분석기")

전체_자산 = st.number_input("전체 자산 입력", min_value=0, value=100000)
지출_입력 = st.text_area("지출 데이터 입력\n(예: 2025-06-08,15000)", height=150)

if st.button("분석 시작"):
    try:
        지출_리스트 = []
        for 줄 in 지출_입력.strip().split("\n"):
            날짜, 금액 = 줄.strip().split(",")
            지출_리스트.append((날짜.strip(), int(금액.strip())))
        지출_분석_및_경고(전체_자산, 지출_리스트)
    except:
        st.error("입력 형식을 확인하세요. (예: 2025-06-08,15000)")

