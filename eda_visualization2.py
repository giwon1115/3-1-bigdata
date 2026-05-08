"""
CSIC Database EDA Dashboard
===========================
csic_database.csv 기반 웹 공격 탐색적 데이터 분석(EDA)

실행:
streamlit run eda_visualization.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.parse import unquote
import os
import re

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="CSIC Database EDA",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 CSIC Database 웹 공격 데이터 분석")
st.markdown("HTTP 요청 데이터에서 정상/공격 패턴을 분석합니다.")

# ============================================================
# 데이터 로드
# ============================================================
@st.cache_data
def load_data():

    data_path = os.path.join(
        os.path.dirname(__file__),
        "csic_database.csv"
    )

    df = pd.read_csv(data_path)

    # --------------------------------------------------------
    # 컬럼명 통일
    # --------------------------------------------------------
    df.columns = [c.strip().lower() for c in df.columns]

    # 예상 컬럼 매핑
    column_mapping = {
        "method": "method",
        "url": "url",
        "content": "body",
        "body": "body",
        "label": "label"
    }

    # 실제 존재하는 컬럼만 선택
    existing = {}
    for old, new in column_mapping.items():
        if old in df.columns:
            existing[old] = new

    df = df.rename(columns=existing)

    # --------------------------------------------------------
    # 누락 컬럼 처리
    # --------------------------------------------------------
    required_cols = ["method", "url", "body", "label"]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # --------------------------------------------------------
    # URL / Body 디코딩
    # --------------------------------------------------------
    df["url_decoded"] = df["url"].fillna("").apply(
        lambda x: unquote(str(x), encoding="latin-1")
    )

    df["body_decoded"] = df["body"].fillna("").apply(
        lambda x: unquote(str(x), encoding="latin-1")
    )

    # --------------------------------------------------------
    # 전체 텍스트
    # --------------------------------------------------------
    df["full_text"] = (
        df["url_decoded"] + " " + df["body_decoded"]
    )

    # --------------------------------------------------------
    # 길이 특징
    # --------------------------------------------------------
    df["url_length"] = df["url_decoded"].str.len()

    df["body_length"] = df["body_decoded"].str.len()

    # --------------------------------------------------------
    # 공격 여부 처리
    # --------------------------------------------------------
    df["label"] = df["label"].astype(str)

    attack_keywords = [
        "anomalous",
        "attack",
        "malicious",
        "1"
    ]

    df["is_attack"] = df["label"].str.lower().apply(
        lambda x: 1 if any(k in x for k in attack_keywords) else 0
    )

    # 라벨 이름 정리
    df["label_clean"] = df["is_attack"].map({
        0: "Normal",
        1: "Anomalous"
    })

    return df


df = load_data()

# ============================================================
# 사이드바
# ============================================================
st.sidebar.header("📊 데이터 기본 정보")

st.sidebar.metric(
    "전체 HTTP 요청",
    f"{len(df):,}건"
)

st.sidebar.metric(
    "정상 요청",
    f"{(df['is_attack']==0).sum():,}건"
)

st.sidebar.metric(
    "공격 요청",
    f"{(df['is_attack']==1).sum():,}건"
)

attack_ratio = df["is_attack"].mean() * 100

st.sidebar.metric(
    "공격 비율",
    f"{attack_ratio:.2f}%"
)

# HTTP 메서드 통계
st.sidebar.markdown("---")
st.sidebar.subheader("HTTP 메서드")

method_dist = df["method"].value_counts()

for method, count in method_dist.items():
    st.sidebar.text(f"{method}: {count:,}건")

# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 분포 분석",
    "📏 길이 분석",
    "🔑 공격 키워드",
    "📄 HTTP 요청 뷰어"
])

# ============================================================
# 탭 1 : 분포 분석
# ============================================================
with tab1:

    st.header("📊 정상 vs 공격 분포")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 파이 차트
    # --------------------------------------------------------
    with col1:

        fig = px.pie(
            values=df["label_clean"].value_counts().values,
            names=df["label_clean"].value_counts().index,
            hole=0.4,
            title="정상 vs 공격 비율",
            color_discrete_sequence=["#22d3ee", "#ef4444"]
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 메서드별 분석
    # --------------------------------------------------------
    with col2:

        cross = pd.crosstab(
            df["method"],
            df["label_clean"]
        ).reset_index()

        cross_melted = cross.melt(
            id_vars="method",
            var_name="label",
            value_name="count"
        )

        fig = px.bar(
            cross_melted,
            x="method",
            y="count",
            color="label",
            barmode="group",
            title="HTTP 메서드별 정상/공격 분포",
            color_discrete_map={
                "Normal": "#22d3ee",
                "Anomalous": "#ef4444"
            }
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# 탭 2 : 길이 분석
# ============================================================
with tab2:

    st.header("📏 URL / Body 길이 분석")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # URL 길이 히스토그램
    # --------------------------------------------------------
    with col1:

        fig = px.histogram(
            df,
            x="url_length",
            color="label_clean",
            nbins=100,
            opacity=0.7,
            barmode="overlay",
            title="URL 길이 분포",
            color_discrete_map={
                "Normal": "#22d3ee",
                "Anomalous": "#ef4444"
            }
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Box Plot
    # --------------------------------------------------------
    with col2:

        fig = px.box(
            df,
            x="label_clean",
            y="url_length",
            color="label_clean",
            title="URL 길이 Box Plot",
            color_discrete_map={
                "Normal": "#22d3ee",
                "Anomalous": "#ef4444"
            }
        )

        fig.update_layout(
            height=450,
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 통계 테이블
    # --------------------------------------------------------
    st.subheader("📊 길이 통계")

    stats_df = df.groupby("label_clean")[
        ["url_length", "body_length"]
    ].agg([
        "mean",
        "median",
        "max"
    ]).round(2)

    st.dataframe(
        stats_df,
        use_container_width=True
    )

# ============================================================
# 탭 3 : 공격 키워드
# ============================================================
with tab3:

    st.header("🔑 공격 키워드 분석")

    attack_categories = {
        "SQL Injection": [
            "select",
            "union",
            "drop",
            "insert",
            "delete",
            "1=1",
            "--"
        ],

        "XSS": [
            "<script",
            "alert(",
            "javascript:",
            "<iframe"
        ],

        "Path Traversal": [
            "../",
            "..\\",
            "/etc/passwd"
        ],

        "Command Injection": [
            "&&",
            "|",
            ";",
            "wget",
            "curl"
        ]
    }

    results = []

    for category, keywords in attack_categories.items():

        for kw in keywords:

            normal_count = df[
                df["is_attack"] == 0
            ]["full_text"].str.contains(
                re.escape(kw),
                case=False,
                na=False
            ).sum()

            attack_count = df[
                df["is_attack"] == 1
            ]["full_text"].str.contains(
                re.escape(kw),
                case=False,
                na=False
            ).sum()

            results.append({
                "카테고리": category,
                "키워드": kw,
                "정상 발견": normal_count,
                "공격 발견": attack_count
            })

    result_df = pd.DataFrame(results)

    # --------------------------------------------------------
    # 시각화
    # --------------------------------------------------------
    fig = px.bar(
        result_df,
        x="키워드",
        y="공격 발견",
        color="카테고리",
        title="공격 요청에서 발견된 키워드"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        result_df.sort_values(
            "공격 발견",
            ascending=False
        ),
        use_container_width=True
    )

# ============================================================
# 탭 4 : HTTP 요청 뷰어
# ============================================================
with tab4:

    st.header("📄 실제 HTTP 요청 보기")

    request_type = st.selectbox(
        "요청 유형 선택",
        ["Normal", "Anomalous"]
    )

    if request_type == "Normal":
        target_df = df[df["is_attack"] == 0]
    else:
        target_df = df[df["is_attack"] == 1]

    idx = st.number_input(
        "데이터 번호",
        min_value=0,
        max_value=max(len(target_df)-1, 0),
        value=0
    )

    row = target_df.iloc[int(idx)]

    st.subheader("HTTP 요청 정보")

    st.text(f"Method: {row['method']}")

    st.text("URL:")
    st.code(row["url_decoded"])

    if str(row["body_decoded"]).strip():
        st.text("Body:")
        st.code(row["body_decoded"])

    st.text("Label:")
    st.code(row["label"])

# ============================================================
# 하단 요약
# ============================================================
st.markdown("---")

st.header("📝 분석 핵심 요약")

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        "공격 요청은 URL 길이가 긴 경우가 많음"
    )

with col2:
    st.success(
        "SQL/XSS 키워드가 공격 요청에 집중됨"
    )

with col3:
    st.success(
        "HTTP 요청 텍스트만으로도 공격 패턴 탐지가 가능"
    )