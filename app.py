# 1단계 — 기본 가계부 앱

import streamlit as st
from datetime import date


# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="나의 가계부",
    page_icon="💰"
)


# ==========================================
# 2. 제목
# ==========================================

st.title("💰 나의 가계부")

st.write("수입과 지출을 기록해보세요.")


# ==========================================
# 3. 데이터 저장 공간
# ==========================================

if "transactions" not in st.session_state:
    st.session_state.transactions = []


# ==========================================
# 4. 거래 유형 선택
# ==========================================

st.subheader("① 거래 유형")

transaction_type = st.radio(
    "수입 또는 지출을 선택하세요.",
    ["지출", "수입"],
    horizontal=True
)


# ==========================================
# 5. 입력
# ==========================================

st.subheader("② 거래 내용")


transaction_date = st.date_input(
    "날짜",
    value=date.today()
)


# 거래 유형에 따라 카테고리 변경

if transaction_type == "지출":

    categories = [
        "식비",
        "교통비",
        "쇼핑",
        "문화/여가",
        "생활비",
        "기타"
    ]

else:

    categories = [
        "급여",
        "용돈",
        "부수입",
        "이자",
        "기타"
    ]


category = st.selectbox(
    "카테고리",
    categories
)


description = st.text_input(
    "내용",
    placeholder="예: 점심 식사"
)


amount = st.number_input(
    "금액",
    min_value=0,
    step=1000,
    value=0
)


# ==========================================
# 6. 저장
# ==========================================

if st.button(
    "💾 저장하기",
    type="primary"
):

    if description.strip() == "":

        st.warning(
            "내용을 입력해주세요."
        )

    elif amount == 0:

        st.warning(
            "금액을 입력해주세요."
        )

    else:

        transaction = {

            "date": transaction_date,

            "type": transaction_type,

            "category": category,

            "description": description,

            "amount": amount
        }

        st.session_state.transactions.append(
            transaction
        )

        st.success(
            f"{transaction_type} {amount:,}원이 저장되었습니다."
        )

        st.rerun()


# ==========================================
# 7. 거래 내역
# ==========================================

st.divider()

st.subheader("③ 거래 내역")


if len(st.session_state.transactions) == 0:

    st.info(
        "아직 등록된 거래 내역이 없습니다."
    )

else:

    for transaction in st.session_state.transactions:

        if transaction["type"] == "지출":

            icon = "🔴"
            sign = "-"

        else:

            icon = "🔵"
            sign = "+"


        st.write(
            f"{icon} "
            f"{transaction['date']} | "
            f"{transaction['type']} | "
            f"{transaction['category']} | "
            f"{transaction['description']} | "
            f"**{sign}{transaction['amount']:,}원**"
        )


# ==========================================
# 8. 금액 계산
# ==========================================

total_income = 0
total_expense = 0


for transaction in st.session_state.transactions:

    if transaction["type"] == "수입":

        total_income += transaction["amount"]

    else:

        total_expense += transaction["amount"]


balance = total_income - total_expense


# ==========================================
# 9. 요약
# ==========================================

st.divider()

st.subheader("④ 가계부 요약")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "총 수입",
        f"{total_income:,}원"
    )


with col2:

    st.metric(
        "총 지출",
        f"{total_expense:,}원"
    )


with col3:

    st.metric(
        "현재 잔액",
        f"{balance:,}원"
    )