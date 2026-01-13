import streamlit as st

# 페이지 설정 및 블랙 테마 적용
st.set_page_config(page_title="Vet Oncology Command Center", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stSelectbox, .stNumberInput, .stSlider { background-color: #1e1e1e !important; color: #ffffff !important; }
    h1, h2, h3 { color: #00FFC8 !important; }
    .stAlert { background-color: #111111; border: 1px solid #00FFC8; color: #ffffff; }
    .result-card { background-color: #151515; padding: 20px; border-radius: 10px; border: 1px dotted #00FFC8; }
    </style>
    """, unsafe_allow_all_html=True)

# 1. 병원 약물 데이터베이스
INVENTORY = {
    "로이나제주 (L-Asparaginase)": {
        "vial_mg": 10000, "unit": "IU", "concentration": 2000, "default_dose": 400, "dose_unit": "IU/kg",
        "diluent": "0.9% NaCl (Vial당 5ml 희석 시 2000IU/ml)", 
        "protocol": "전처치: Diphenhydramine (1mg/kg IM). \n경로: SC 또는 IM 권장 (IV 시 아나필락시스 위험 급증). \n주의: 응고부전, 췌장염 병력 확인."
    },
    "벨바스틴주 (Vinblastine)": {
        "vial_mg": 10, "unit": "mg", "concentration": 1.0, "default_dose": 2.0, "dose_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "전처치: 필요 시 항히스타민. \n경로: IV Bolus. \n주의: Vesicant (혈관외 유출 시 조직괴사), Vincristine보다 골수독성 강함."
    },
    "빈크란주 (Vincristine)": {
        "vial_mg": 1, "unit": "mg", "concentration": 1.0, "default_dose": 0.7, "dose_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "전처치: 필요 없음. \n경로: IV Bolus (Side arm). \n주의: Vesicant. 신경독성(장마비, 부전마비) 모니터링."
    },
    "아드리아마이신 (Doxorubicin)": {
        "vial_mg": 10, "unit": "mg", "concentration": 2.0, "default_dose": 30.0, "dose_unit": "mg/m2",
        "diluent": "0.9% NaCl (보통 1:1 희석하여 1mg/ml로 투여)", 
        "protocol": "전처치: Diphenhydramine + Dexamethasone. \n경로: 15~30분 저속 IV. \n주의: 개(심독성-Cardioxane 고려), 고양이(신독성-IRIS확인)."
    },
    "카보티놀주 (Carboplatin)": {
        "vial_mg": 150, "unit": "mg", "concentration": 10.0, "default_dose": 300.0, "dose_unit": "mg/m2",
        "diluent": "5% Dextrose (D5W) 필수", 
        "protocol": "전처치: 항구토제 권장. \n경로: 15~30분 IV. \n주의: NaCl과 혼합 금지 (침전 위험). IRIS Stage 3 이상 강력 감량."
    },
    "시타라빈주 (Cytarabine)": {
        "vial_mg": 100, "unit": "mg", "concentration": 20.0, "default_dose": 100.0, "dose_unit": "mg/m2",
        "diluent": "0.9% NaCl 또는 D5W", 
        "protocol": "경로: SC (보통 2-4일간 BID) 또는 CRI. \n주의: 골수억제 강함, 중추신경계 림프종/백혈병 투여."
    },
    "엔독산주 (Cyclophosphamide)": {
        "vial_mg": 500, "unit": "mg", "concentration": 20.0, "default_dose": 250.0, "dose_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "전처치: Furosemide (2.2mg/kg) 병용 권장. \n주의: 무균성 출혈성 방광염 주의. 투여 후 충분한 음수 및 배뇨 유도."
    },
    "미트론주 (Mitoxantrone)": {
        "vial_mg": 20, "unit": "mg", "concentration": 2.0, "default_dose": 5.5, "dose_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "경로: 15분 IV. \n주의: Doxorubicin 대체제. 투여 후 소변색 변화(청록색) 가능성 고지."
    },
    "카디옥산주 (Dexrazoxane)": {
        "vial_mg": 500, "unit": "mg", "concentration": 10.0, "default_dose": 10.0, "dose_unit": "ratio (10:1)",
        "diluent": "전용 희석액 후 0.9% NaCl", 
        "protocol": "목적: Doxorubicin 심독성 예방. \n투여: Doxorubicin 투여 15~30분 전 IV 완료. \n용량: Doxorubicin mg 용량의 10배 투여."
    },
    "박스루킨15주 (IL-2)": {
        "vial_mg": 0.1, "unit": "μg", "concentration": 100.0, "default_dose": 100.0, "dose_unit": "μg/head",
        "diluent": "0.9% NaCl", 
        "protocol": "면역요법제. 프로토콜에 따라 용량 상이. \n주의: 발열, 오한 등 면역 반응 모니터링."
    }
}

# 사이드바 환자 정보
st.sidebar.title("🐾 환자 정보")
breed_type = st.sidebar.radio("종 선택", ["Dog", "Cat"])
weight = st.sidebar.number_input("체중 (kg)", min_value=0.1, value=5.0, step=0.1)
k = 10.1 if breed_type == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100
st.sidebar.metric("체표면적 (BSA)", f"{bsa:.4f} m²")

# 메인 입력 섹션
st.title("🩺 주사용 항암제 계산기")
col1, col2 = st.columns(2)

with col1:
    drug_name = st.selectbox("항암제 선택", list(INVENTORY.keys()))
    drug = INVENTORY[drug_name]
    calc_basis = st.radio("계산 기준", ["체표면적(BSA) 기준", "체중(kg) 기준"], 
                         index=0 if drug["dose_unit"] == "mg/m2" else 1)

with col2:
    target_dose = st.number_input(f"목표 용량 ({drug['dose_unit']})", value=float(drug["default_dose"]))
    reduction = st.select_slider("용량 조정 (Condition)", options=[50, 60, 70, 80, 90, 100], value=100)

# 계산 실행
if calc_basis == "체표면적(BSA) 기준":
    total_mg = bsa * target_dose * (reduction / 100)
    formula = f"{bsa:.4f} m² × {target_dose} {drug['dose_unit']} × {reduction}%"
else:
    total_mg = weight * target_dose * (reduction / 100)
    formula = f"{weight} kg × {target_dose} {drug['dose_unit']} × {reduction}%"

needed_volume = total_mg / drug["concentration"]

# 결과 출력
st.markdown("---")
res_col1, res_col2 = st.columns([1, 1])

with res_col1:
    st.markdown(f"### 💉 {drug_name} 결과")
    st.markdown(f"""
    <div class="result-card">
        <h2 style='color:#00FFC8;'>필요 용량: {total_mg:.3f} {drug['unit']}</h2>
        <h3 style='color:#ffffff;'>조제 볼륨: {needed_volume:.2f} ml</h3>
        <p style='color:#888;'>계산식: {formula}</p>
    </div>
    """, unsafe_allow_all_html=True)

with res_col2:
    st.markdown("### 📋 투여 프로토콜")
    st.info(f"""
    **[희석 정보]**
    - 희석액: {drug['diluent']}
    
    **[상세 지침]**
    {drug['protocol']}
    """)

if breed_type == "Dog" and weight < 10 and "BSA" in calc_basis:
    st.warning("⚠️ 소형견(10kg 미만) 경고: BSA 기준 투여 시 독성이 강할 수 있습니다.")

st.caption("Veterinary Chemo Dose Calculator v2.0 | GY 전용")
