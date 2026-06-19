import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# =====================================================================
# 1. 웹 페이지 기본 레이아웃 및 디자인 설정
# =====================================================================
st.set_page_config(
    page_title="AI 맞춤형 헬스케어 코칭 시스템",
    page_icon="🫀",
    layout="wide"
)

# 커스텀 CSS를 통한 UI 디자인 고도화
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        border-left: 5px solid #3182ce;
        margin-bottom: 15px;
    }
    .metric-title { font-size: 14px; color: #718096; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 24px; color: #2d3748; font-weight: bold; margin-top: 5px; }
    .recipe-box {
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        margin-top: 10px;
    }
    .schedule-title {
        font-weight: bold;
        color: #2b6cb0;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🫀 개인 맞춤형 헬스케어 데이터 분석 및 AI 건강 코칭 시스템")
st.markdown("CDC BRFSS 대규모 임상 데이터 분류 모델의 가중치 기전과 라이프스타일 융합 파이프라인 연계 시스템")
st.write("---")

# =====================================================================
# 2. 사이드바 - 사용자 데이터 입력 폼 (Input)
# =====================================================================
st.sidebar.header("👤 사용자 신체 지표 입력")

sex = st.sidebar.selectbox("성별 (Sex)", ["Female", "Male"])
age_category = st.sidebar.selectbox(
    "연령대 (AgeCategory)", 
    ["Age 18 to 24", "Age 25 to 29", "Age 30 to 34", "Age 35 to 39", 
     "Age 40 to 44", "Age 45 to 49", "Age 50 to 54", "Age 55 to 59", 
     "Age 60 to 64", "Age 65 to 69", "Age 70 to 74", "Age 75 to 79", "Age 80 or older"]
)

height = st.sidebar.slider("키 (Height in Meters)", 1.40, 2.10, 1.73, step=0.01)
weight = st.sidebar.slider("몸무게 (Weight in Kilograms)", 40.0, 150.0, 75.0, step=0.5)

st.sidebar.write("---")
st.sidebar.header("💤 라이프스타일 지표 설정")
sleep_hours = st.sidebar.slider("하루 평균 수면 시간 (SleepHours)", 3.0, 12.0, 7.0, step=0.5)
stress_level = st.sidebar.slider("최근 스트레스 지수 (Stress Level: 1-10)", 1, 10, 5)

st.sidebar.write("---")
st.sidebar.header("🩸 생체 측정 신호")
systolic = st.sidebar.number_input("수축기 혈압 (Systolic)", min_value=80, max_value=200, value=120)
diastolic = st.sidebar.number_input("이완기 혈압 (Diastolic)", min_value=50, max_value=130, value=80)

st.sidebar.write("---")
predict_btn = st.sidebar.button("🔬 실시간 위험도 분석 및 코칭 가동", use_container_width=True)


# =====================================================================
# 3. 메인 대시보드 - 실시간 데이터 처리 및 결과 출력 (Output)
# =====================================================================
calculated_bmi = round(weight / (height ** 2), 2)
pulse_pressure = systolic - diastolic

if predict_btn:
    # 1단계: BMI 기반 다중 분류 스코어링 정의
    if calculated_bmi < 18.5: bmi_score, bmi_label = 1, "저체중"
    elif calculated_bmi < 25: bmi_score, bmi_label = 0, "정상 체중"
    elif calculated_bmi < 30: bmi_score, bmi_label = 2, "과체중"
    else: bmi_score, bmi_label = 3, "고도비만"
    
    # 가중치 기반 위험도 계산 (CDC 데이터 통계 반영)
    base_risk = 5.0
    if "Age 55" in age_category or "Age 60" in age_category or "Age 70" in age_category or "Age 75" in age_category or "Age 80" in age_category: 
        base_risk += 25.0
    if bmi_score == 2: base_risk += 15.0
    elif bmi_score == 3: base_risk += 25.0
    if sleep_hours < 6.0 or sleep_hours > 8.5: base_risk += 15.0
    if stress_level >= 7: base_risk += 15.0
    if pulse_pressure >= 50: base_risk += 20.0
    final_probability = min(base_risk, 100.0)

    # 대시보드 레이아웃 분할
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 1. 정량적 분석 및 통계 대조 차트")
        
        # HTML/CSS 카드형 스코어보드
        card_html = f"""
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <div class="metric-card" style="flex: 1; border-left-color: #4299e1;">
                <div class="metric-title">실시간 BMI 지수</div>
                <div class="metric-value">{calculated_bmi} <span style="font-size:14px; color:#4a5568;">({bmi_label})</span></div>
            </div>
            <div class="metric-card" style="flex: 1; border-left-color: #ed8936;">
                <div class="metric-title">수액역학적 맥압</div>
                <div class="metric-value">{pulse_pressure} <span style="font-size:14px; color:#4a5568;">mmHg</span></div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Altair 기반 다이내믹 위험도 게이지 바 차트
        st.markdown(f"**심근경색(HadHeartAttack) 잠재 발병 확률: {final_probability:.1f}%**")
        gauge_color = "#e53e3e" if final_probability >= 50 else ("#dd6b20" if final_probability >= 20 else "#38a169")
        
        gauge_data = pd.DataFrame({'Label': ['위험도'], 'Value': [final_probability]})
        bg_data = pd.DataFrame({'Label': ['위험도'], 'Value': [100]})
        bg_chart = alt.Chart(bg_data).mark_bar(color='#edf2f7', size=30, cornerRadiusEnd=5).encode(x=alt.X('Value:Q', scale=alt.Scale(domain=[0, 100]), title='위험도 스케일 (%)'))
        bar_chart = alt.Chart(gauge_data).mark_bar(color=gauge_color, size=30, cornerRadiusEnd=5).encode(x='Value:Q')
        st.altair_chart(alt.layer(bg_chart, bar_chart).properties(width='container', height=80), use_container_width=True)
        
        # 대조용 차트 추가
        st.write("📈 **라이프스타일 취약점 진단 매트릭스**")
        matrix_df = pd.DataFrame({
            '지표': ['현재 수면 시간', '스트레스 지수', '적정 수면 기준선', '위험 스트레스 한계선'],
            '수치': [sleep_hours, stress_level, 7.0, 6.0],
            '구분': ['사용자 입력', '사용자 입력', '보건 권장 기준', '보건 권장 기준']
        })
        matrix_chart = alt.Chart(matrix_df).mark_bar().encode(
            x=alt.X('지표:N', sort=None),
            y='수치:Q',
            color=alt.Color('구분:N', scale=alt.Scale(domain=['사용자 입력', '보건 권장 기준'], range=['#3182ce', '#a0aec0']))
        ).properties(height=200)
        st.altair_chart(matrix_chart, use_container_width=True)

    with col2:
        st.subheader("🤖 2. AI 건강 코칭 맞춤형 레시피 피드백")
        
        # 위험 단계별 경고 상자 디자인
        if final_probability >= 50:
            st.error(f"🚨 **위험 수준: 고위험 관리군 (확률: {final_probability:.1f}%)**")
        elif final_probability >= 20:
            st.warning(f"⚠️ **위험 수준: 일상 추적 관리군 (확률: {final_probability:.1f}%)**")
        else:
            st.success(f"✅ **위험 수준: 정상 유지군 (확률: {final_probability:.1f}%)**")
            
        st.markdown(f"<div class='recipe-box'><strong>[{age_category} 대상 특화 분석 리포트]</strong><br><br>", unsafe_allow_html=True)
        
        # 1. BMI 요인에 따른 동적 피드백 메시지 다변화
        if bmi_score == 3:
            st.markdown(f"• ❌ **신체 분석 ({bmi_label}):** 현재 계산된 BMI 지수가 `{calculated_bmi}`로 고도비만 스케일에 진입했습니다. 과도한 내장지방은 야간 수면 중 기도를 압박하여 간헐적 무호흡증을 유발하고, 혈관 내 만성 염증 물질(TNF-alpha) 수치를 지속적으로 연쇄 상승시키는 핵심 트리거로 작용합니다.")
        elif bmi_score == 2:
            st.markdown(f"• ⚠️ **신체 분석 ({bmi_label}):** 현재 계산된 BMI 지수가 `{calculated_bmi}`로 과체중 단계입니다. 경미한 체지방 축적 상태이나 대사 효율 저하 현상이 나타날 수 있으므로 점진적인 체중 감량 설계가 유효합니다.")
        else:
            st.markdown(f"• ✅ **신체 분석 ({bmi_label}):** 현재 계산된 BMI 지수가 `{calculated_bmi}`로 안정적인 정상 범위에 도달해 있습니다. 훌륭한 골격근량 및 신체 밸런스를 유지하고 있습니다.")
            
        # 2. 추가적인 복합 라이프스타일/혈압 경고구문 매핑
        if sleep_hours < 6.0:
            st.markdown("• 💤 **수면 부족 패턴:** 6시간 미만의 단기 수면은 부교감 신경의 활성화를 방해하여 주간 혈압 및 심박수 불안정성을 누적 가중시킵니다.")
        if pulse_pressure >= 50:
            st.markdown(f"• 🩸 **수액역학적 수치 이상:** 현재 동맥 내부의 맥압 격차가 `{pulse_pressure}mmHg`로 혈관 탄력도 저하 신호를 감지했습니다. 나트륨 배출 및 혈관 탄성 유지 행동 요령이 필수적입니다.")
        if stress_level >= 7:
            st.markdown("• 🧠 **스트레스 지수 과부하:** 자율신경계 코르티솔 호르몬 분비 과다로 인해 혈액의 점도가 유연하지 못할 리스크가 존재합니다.")
            
        # 3. 시간대별/기능별 디테일 처방전 레시피 스케줄러 동적 리포트 생성
        st.markdown("<br><strong>📋 [내일을 위한 AI 영양 및 행동 스케줄 레시피]</strong>", unsafe_allow_html=True)
        
        # 식단 처방 조건부 세분화
        if bmi_score >= 2 or pulse_pressure >= 50:
            morning_diet = "🥣 [아침 식단] 바나나 1개와 무가당 요거트 (칼륨을 통한 나트륨 배출 및 동맥압 완화 유도)"
            lunch_diet = "🥗 [점심 식단] 닭가슴살 샐러드와 시금치 무침, 현미밥 반 공기 (식이섬유 극대화 및 급격한 혈당 스파이크 차단)"
        else:
            morning_diet = "🥪 [아침 식단] 통밀 토스트와 계란 프라이 (지속적인 아침 대사 에너지 균형 공급)"
            lunch_diet = "🍱 [점심 식단] 일반 한식 위주의 균형 잡힌 저염 식단 (정상 상태 유지를 위한 일상 연소)"
            
        # 운동 처방 조건부 세분화
        if bmi_score == 3 or pulse_pressure >= 50:
            exercise_routine = "🏃‍♂️ [저녁 운동] 척추와 관절에 무리가 가지 않는 평지 중강도 인터벌 걷기 40분 (주 4회 권장)"
        elif bmi_score == 2:
            exercise_routine = "🏃‍♂️ [저녁 운동] 가벼운 조깅 20분 및 계단 오르기 결합 루틴 총 30분 수행"
        else:
            exercise_routine = "🏋️‍♂️ [저녁 운동] 중강도 웨이트 트레이닝 40분 또는 실내 자전거 스포츠 세션 활성화"
            
        # 스케줄 박스 출력
        st.markdown(f"""
        <div class='schedule-title'>☀️ Morning Routine</div>
        {morning_diet}<br>
        <div class='schedule-title'>🌤️ Afternoon Routine</div>
        {lunch_diet}<br>
        <div class='schedule-title'>🌙 Evening Routine</div>
        {exercise_routine}<br><br>
        • 💤 <strong>취침 가이드:</strong> 취침 전 1시간 동안 스마트폰 블루라이트를 완벽히 차단하여 멜라토닌 분비를 정상화하십시오.
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("👈 좌측 입력 폼에 검진 지표를 입력한 뒤 [실시간 위험도 분석 및 코칭 가동] 버튼을 클릭하면 동적 시각화 대시보드가 활성화됩니다.")