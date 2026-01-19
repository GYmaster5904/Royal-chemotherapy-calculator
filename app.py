import streamlit as st

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="Royal Vet Oncology Center", layout="wide")

# 2. 블랙 & 네온 그린 테마 강제 적용 (안정적인 표준 문법)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    .stSelectbox, .stNumberInput, .stSlider { background-color: #1e1e1e !important; color: #ffffff !important; }
    h1, h2, h3 { color: #00FFC8 !important; }
    .protocol-box {
        background-color: #111; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #00FFC8;
        line-height: 1.6;
    }
    .result-box {
        background-color: #151515;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00FFC8;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_all_html=True)

# 3. 항암제 마스터 데이터베이스 (10종 완벽 반영)
DRUG_DB = {
    "로이나제주 (L-Asparaginase)": {
        "vial": "10,000 IU/Vial", "unit": "IU", "conc": 2000, "def_dose": 400.0, "d_unit": "IU/kg",
        "diluent": "0.9% NaCl (Vial당 5ml 희석 시 2,000IU/ml)", 
        "protocol": "💉 <b>전처치:</b> Diphenhydramine (1mg/kg IM) 필수.<br>💉 <b>경로:</b> SC 또는 IM 권장 (IV 시 아나필락시스 쇼크 위험 급증).<br>⚠️ <b>주의:</b> 응고부전, 췌장염 병력 확인. 투여 후 30분간 과민반응 모니터링."
    },
    "벨바스틴주 (Vinblastine)": {
        "vial": "10mg/Vial", "unit": "mg", "conc": 1.0, "def_dose": 2.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "💉 <b>전처치:</b> 비만세포종(MCT) 환자는 항히스타민/스테로이드 전처치 권장.<br>💉 <b>경로:</b> IV Bolus.<br>⚠️ <b>주의:</b> Vesicant (혈관외 유출 시 심각한 조직괴사). Vincristine보다 골수독성(Neutropenia)이 더 강력함."
    },
    "빈크란주 (Vincristine)": {
        "vial": "1mg/Vial", "unit": "mg", "conc": 1.0, "def_dose": 0.7, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "💉 <b>경로:</b> IV Bolus (Side arm 방식 권장).<br>⚠️ <b>주의:</b> Vesicant. 신경독성(장마비에 의한 변비, 부전마비) 주의. 간수치 상승 시 용량 감량 검토."
    },
    "아드리아마이신 (Doxorubicin)": {
        "vial": "10mg/5ml (2mg/ml)", "unit": "mg", "conc": 2.0, "def_dose": 30.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl (보통 1:1 희석하여 1mg/ml 농도로 투여 권장)", 
        "protocol": "💉 <b>전처치:</b> Diphenhydramine + Dexamethasone.<br>💉 <b>경로:</b> 15~30분간 매우 천천히 저속 IV.<br>⚠️ <b>주의:</b> 개(심독성 - Echo 필수), 고양이(신독성 - IRIS 단계 확인). 카디옥산 전처치 적극 권장."
    },
    "카보티놀주 (Carboplatin)": {
        "vial": "150mg/15ml (10mg/ml)", "unit": "mg", "conc": 10.0, "def_dose": 300.0, "d_unit": "mg/m2",
        "diluent": "5% Dextrose (D5W) 필수 (Saline과 혼합 금지)", 
        "protocol": "💉 <b>경로:</b> 15~30분 IV 주입.<br>⚠️ <b>주의:</b> 신장 배설 약물. IRIS Stage 3 이상 강력 감량. 혈소판 감소증(Nadir)이 2주차에 나타나므로 CBC 모니터링 필수."
    },
    "시타라빈주 (Cytarabine)": {
        "vial": "100mg/5ml (20mg/ml)", "unit": "mg", "conc": 20.0, "def_dose": 100.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl 또는 D5W", 
        "protocol": "💉 <b>경로:</b> SC (보통 2~4일간 분할 투여) 또는 8~24시간 CRI 주입.<br>⚠️ <b>주의:</b> 골수억제 강함. 주로 중추신경계(GME, 림프종) 침범 시 혈뇌장벽 통과를 목적으로 사용."
    },
    "엔독산주 (Cyclophosphamide)": {
        "vial": "500mg/Vial", "unit": "mg", "conc": 20.0, "def_dose": 250.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl (Vial당 25ml 희석 시 20mg/ml)", 
        "protocol": "💉 <b>전처치:</b> Furosemide (2.2mg/kg) 병용 권장.<br>⚠️ <b>주의:</b> 무균성 출혈성 방광염(SHC) 주의. 투여 당일 충분한 음수 유도 및 빈번한 배뇨 필요. 혈뇨 관찰 시 즉시 중단."
    },
    "미트론주 (Mitoxantrone)": {
        "vial": "20mg/10ml (2mg/ml)", "unit": "mg", "conc": 2.0, "def_dose": 5.5, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "💉 <b>경로:</b> 15분 IV 주입.<br>⚠️ <b>주의:</b> Doxorubicin 대체제(심독성 낮음). 투여 후 1~2일간 소변색이 청록색으로 변할 수 있음을 보호자에게 미리 고지."
    },
    "카디옥산주 (Dexrazoxane)": {
        "vial": "500mg/Vial", "unit": "mg", "conc": 10.0, "def_dose": 10.0, "d_unit": "ratio (10:1)",
        "diluent": "전용 희석액 후 0.9% NaCl", 
        "protocol": "💉 <b>목적:</b> Doxorubicin 심독성 예방 및 혈관외 유출 시 해독.<br>💉 <b>용량:</b> Doxorubicin mg 용량의 10배 투여.<br>💉 <b>투여:</b> Dox 주입 완료 15~30분 전 완료 권장."
    },
    "박스루킨15주 (IL-2)": {
        "vial": "100μg/1ml", "unit": "μg", "conc": 100.0, "def_dose": 100.0, "d_unit": "μg/head",
        "diluent": "0.9% NaCl", 
        "protocol": "💉 <b>주의:</b> 수의 전용 면역요법제. 투여 후 일시적인 발열, 오한, 식욕부진 등 면역 반응 모니터링. 환자 상태에 따라 용량 가감."
    }
}

# 4. 사이드바 - 환자 정보
st.sidebar.title("🐾 Patient Information")
species = st.sidebar.radio("종 선택", ["Dog", "Cat"])
weight = st.sidebar.number_input("체중 (kg)", min_value=0.1, value=10.0, step=0.1)

# BSA 공식 계산
k = 10.1 if species == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100

st.sidebar.markdown("---")
st.sidebar.markdown(f"### 체표면적 (BSA)")
st.sidebar.title(f"{bsa:.4f} m²")

# 5. 메인 설정 화면
st.title("🩺 Royal Veterinary Oncology Calculator")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Drug selection")
    drug_name = st.selectbox("약물 선택", list(DRUG_DB.keys()))
    drug = DRUG_DB[drug_name]
    
    # 로이나제는 기본 kg 기준, 나머지는 BSA 기준 자동 세팅
    default_index = 1 if "kg" in drug["d_unit"] or "head" in drug["d_unit"] else 0
    basis = st.radio("계산 기준 선택", ["체표면적(BSA) 기준", "체중(kg) 기준"], index=default_index)

with col2:
    st.header("2. Dose & Reduction")
    target_dose = st.number_input(f"목표 용량 설정 ({drug['d_unit']})", value=float(drug["def_dose"]))
    reduction = st.select_slider("용량 조정 (환자 상태 반영)", options=[50, 60, 70, 80, 90, 100], value=100)

# 6. 핵심 계산 실행
if "BSA" in basis:
    total_val = bsa * target_dose * (reduction / 100)
    calc_process = f"{bsa:.4f} m² × {target_dose} × {reduction}%"
else:
    total_val = weight * target_dose * (reduction / 100)
    calc_process = f"{weight} kg × {target_dose} × {reduction}%"

needed_ml = total_val / drug["conc"]

# 7. 최종 결과 및 프로토콜 출력
st.write("---")
res_c1, res_c2 = st.columns([1, 1])

with res_c1:
    st.header("3. Result")
    st.markdown(f"""
    <div class="result-box">
        <p style='color:#888;'>최종 필요 용량 ({drug_name})</p>
        <p style='color:#00FFC8; font-size:42px; font-weight:bold;'>{total_val:.3f} {drug['unit']}</p>
        <br>
        <p style='color:#888;'>실제 주사기 조제 볼륨</p>
        <p style='color:#ffffff; font-size:38px; font-weight:bold;'>{needed_ml:.2f} ml</p>
        <p style='color:#555; font-size:13px; margin-top:15px;'>산식: {calc_process}</p>
        <p style='color:#555; font-size:13px;'>Vial 농도: {drug['conc']} {drug['unit']}/ml | 규격: {drug['vial']}</p>
    </div>
    """, unsafe_allow_all_html=True)

with res_c2:
    st.header("4. Administration Protocol")
    st.warning(f"**권장 희석액:** {drug['diluent']}")
    st.markdown(f"""
    <div class="protocol-box">
        {drug['protocol']}
    </div>
    """, unsafe_allow_all_html=True)

# 8. 소형견 및 특정 약물 경고
if species == "Dog" and weight < 10 and "BSA" in basis:
    st.error("⚠️ [Small Dog Warning] 10kg 미만 소형견입니다. BSA 기준 투여 시 독성 위험이 크므로 mg/kg 환산을 권장합니다.")

if "아드리아마이신" in drug_name:
    st.error("❗ [Doxorubicin Warning] 개 심초음파 필수. 고양이 신장수치 확인. Cardioxane 전처치를 고려하세요.")

st.write("---")
st.caption("Hospital: Royal Vet Center | Powered by AAHA & VCOG-CTCAE v2 Guidelines")


