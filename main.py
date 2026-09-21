import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("365일 동안의 일별 박스오피스 데이터를 이용해 영화의 관객 변화를 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자 열을 숫자형으로 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()


# --------------------------------------------------
# 데이터 기본 정보
# --------------------------------------------------
st.divider()
st.header("📊 데이터 살펴보기")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("기록된 날짜 수", f"{df['날짜'].nunique()}일")

with col2:
    st.metric("영화 수", f"{df['영화명'].nunique()}편")

with col3:
    st.metric("전체 기록 수", f"{len(df):,}개")


# ==================================================
# 그래프 1
# ==================================================
st.divider()
st.header("1. 영화별 시간에 따른 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화가 날짜별로 얼마나 많은 관객을 모았는지 확인할 수 있습니다."
)

# 영화 목록
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "🎥 영화를 선택하세요",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")


# --------------------------------------------------
# 선 그래프
# --------------------------------------------------
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

fig.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,.0f}명"
    "<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# 그래프에서 알 수 있는 것
# --------------------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요",
    placeholder="예: 영화의 개봉 이후 일관객 수가 어떻게 변화했는지 알 수 있다.",
    height=80,
    key="graph1_note"
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()
st.header("2. 다음 그래프")

st.info(
    "앞으로 새로운 그래프를 추가할 공간입니다."
)

st.divider()
st.header("3. 다음 그래프")

st.info(
    # ==================================================
# 그래프 2
# ==================================================
st.divider()
st.header("2. 일관객 합계가 가장 큰 영화 5편의 날짜별 변화")

st.write(
    "전체 기간 동안의 일관객 합계를 기준으로 상위 5편을 골라 "
    "날짜별 일관객 변화를 비교합니다."
)

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

# 상위 5편의 데이터만 추출
top5_df = df[df["영화명"].isin(top5_movies)].copy()

# 날짜와 영화명 기준으로 정렬
top5_df = top5_df.sort_values(["날짜", "영화명"])


# --------------------------------------------------
# 여러 영화를 한 선 그래프에 표시
# --------------------------------------------------
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "영화명": True,
        "일관객": ":,.0f"
    }
)

fig2.update_traces(
    hovertemplate=
    "영화: %{fullData.name}<br>"
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,.0f}명"
    "<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=600,
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# --------------------------------------------------
# 그래프에서 알 수 있는 것
# --------------------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요",
    placeholder="예: 일관객 합계가 높은 영화들의 날짜별 관객 수 변화를 서로 비교할 수 있다.",
    height=80,
    key="graph2_note"
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()
st.header("3. 다음 그래프")

st.info(
    "앞으로 새로운 그래프를 추가할 공간입니다."
)

st.divider()
st.header("4. 다음 그래프")

st.info(
    "앞으로 새로운 그래프를 추가할 공간입니다."
)
)
