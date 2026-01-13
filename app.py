import streamlit as st

# 1. 페이지 설정 (최상단)
st.set_page_config(page_title="Royal Vet Oncology Center", layout="wide")

# 2. 블랙 & 네온 테마 스타일 정의
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    
    /* 입력창 스타일 */
    .stSelectbox, .stNumberInput, .stSlider { background-color: #1e1e1e !important; color: #ffffff !important; }
    
    /* 결과 카드 디자인 */
    .result-card {
        background-color: #151515;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00FFC8;
        box-shadow: 0 0 15px rgba(0, 255, 200, 0.2);
        margin-bottom: 20px;
    }
    
    /* 텍스트 색상 */
    h1, h2, h3 { color: #00FFC8 !important; font-family: 'Inter', sans-serif; }
    .label-text { color: #888888; font-size: 14px; margin-bottom: 5px; }
    .value-text { color: #ffffff; font-size: 32px; font-weight: bold; margin-bottom: 15px; }
    
    /* 경고창 스타일 커스텀 */
    .stAlert { background-color: #1a1a1a; border: 1px solid #ff4b4b; color: #ffffff; }
    </style>
    """, unsafe_allow_all_html=True)

# 3. 병원 사용 약물 마스터 데이터 (Vial 규격 및 농도 포함)
INVENTORY = {
    "로이나제주 (L-Asparaginase)": {
        "vial": "10,000 IU/Vial", "unit": "IU", "conc": 2000, "def_dose": 400, "d_unit": "IU/kg",
        "diluent": "0.9% NaCl (Vial당 5ml 희석 시 2000IU/ml)", 
        "protocol": "<b>전처치:</b> Diphenhydramine (1mg/kg IM).<br><b>경로:</b> SC 또는 IM 권장 (IV 시 아나필락시스 위험).<br><b>주의:</b> 응고부전, 췌장염 병력 확인."
    },
    "벨바스틴주 (Vinblastine)": {
        "vial": "10mg/Vial", "unit": "mg", "conc": 1.0, "def_dose": 2.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>전처치:</b> 필요 시 항히스타민.<br><b>경로:</b> IV Bolus.<br><b>주의:</b> Vesicant (조직괴사 주의). Vincristine보다 골수독성 강함."
    },
    "빈크란주 (Vincristine)": {
        "vial": "1mg/Vial", "unit": "mg", "conc": 1.0, "def_dose": 0.7, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>전처치:</b> 필요 없음.<br><b>경로:</b> IV Bolus (Side arm).<br><b>주의:</b> Vesicant. 신경독성(장마비, 부전마비) 모니터링."
    },
    "아드리아마이신 (Doxorubicin)": {
        "vial": "10mg/5ml", "unit": "mg", "conc": 2.0, "def_dose": 30.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl (보통 1:1 희석하여 1mg/ml로 투여)", 
        "protocol": "<b>전처치:</b> Diphenhydramine + Dexamethasone.<br><b>경로:</b> 15~30분 저속 IV.<br><b>주의:</b> 개(심독성-Cardioxane 고려), 고양이(신독성-IRIS확인)."
    },
    "카보티놀주 (Carboplatin)": {
        "vial": "150mg/15ml", "unit": "mg", "conc": 10.0, "def_dose": 300.0, "d_unit": "mg/m2",
        "diluent": "5% Dextrose (D5W) 필수", 
        "protocol": "<b>전처치:</b> 항구토제 권장.<br><b>경로:</b> 15~30분 IV.<br><b>주의:</b> NaCl과 혼합 금지. IRIS Stage 3 이상 강력 감량."
    },
    "시타라빈주 (Cytarabine)": {
        "vial": "100mg/5ml", "unit": "mg", "conc": 20.0, "def_dose": 100.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl 또는 D5W", 
        "protocol": "<b>경로:</b> SC (보통 2-4일간 BID) 또는 CRI.<br><b>주의:</b> 골수억제 강함, CNS 종양 시 주로 사용."
    },
    "박스루킨15주 (IL-2)": {
        "vial": "100μg/1ml", "unit": "μg", "conc": 100.0, "def_dose": 100.0, "d_unit": "μg/head",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>면역요법제:</b> 프로토콜에 따라 용량 상이.<br><b>주의:</b> 발열, 오한 등 면역 반응 모니터링."
    },
    "엔독산주 (Cyclophosphamide)": {
        "vial": "500mg/Vial", "unit": "mg", "conc": 20.0, "def_dose": 250.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>전처치:</b> Furosemide (2.2mg/kg) 병용 권장.<br><b>주의:</b> 무균성 출혈성 방광염 주의. 투여 후 배뇨 유도 필수."
    },
    "미트론주 (Mitoxantrone)": {
        "vial": "20mg/10mL", "unit": "mg", "conc": 2.0, "def_dose": 5.5, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>경로:</b> 15분 IV.<br><b>주의:</b> Doxorubicin 대체제. 소변색 변화(청록색) 가능성 고지."
    },
    "카디옥산주 (Dexrazoxane)": {
        "vial": "500mg/Vial", "unit": "mg", "conc": 10.0, "def_dose": 10.0, "d_unit": "ratio (10:1)",
        "diluent": "전용 희석액 후 0.9% NaCl", 
        "protocol": "<b>목적:</b> Doxorubicin 심독성 예방.<br><b>투여:</b> Dox 투여 15~30분 전 IV 완료.<br><b>용량:</b> Dox mg 용량의 10배 투여."
    }
}

# 4. 사이드바 - 환자 정보 입력
st.sidebar.title("🐾 Patient Profile")
species = st.sidebar.radio("종 선택", ["Dog", "Cat"])
weight = st.sidebar.number_input("체중 (kg)", min_value=0.1, value=10.0, step=0.1)

# BSA 계산 (개 10.1, 고양이 10.0)
k = 10.1 if species == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100

st.sidebar.markdown(f"---")
st.sidebar.markdown(f"### 체표면적 (BSA)")
st.sidebar.title(f"{bsa:.4f} m²")

# 5. 메인 화면 - 항암제 설정
st.title("🩺 Veterinary Chemo Dose Calculator")

col1, col2 = st.columns(2)

with col1:
    drug_name = st.selectbox("항암제 선택", list(INVENTORY.keys()))
    drug = INVENTORY[drug_name]
    
    # 약물별 기본 계산 기준 자동 설정
    basis = st.radio("계산 기준", ["BSA (m2) 기준", "체중 (kg) 기준"], 
                    index=0 if drug["d_unit"] == "mg/m2" else 1)

with col2:
    target_dose = st.number_input(f"목표 용량 ({drug['d_unit']})", value=float(drug["def_dose"]))
    reduction = st.select_slider("용량 조정 (Reduction %)", options=[50, 60, 70, 80, 90, 100], value=100)

# 계산 로직
if "BSA" in basis:
    total_val = bsa * target_dose * (reduction / 100)
    process_str = f"{bsa:.4f} m² × {target_dose} × {reduction}%"
else:
    total_val = weight * target_dose * (reduction / 100)
    process_str = f"{weight} kg × {target_dose} × {reduction}%"

needed_ml = total_val / drug["conc"]

# 6. 최종 결과 표시 (HTML 카드 방식)
st.markdown("---")
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.markdown(f"""
    <div class="result-card">
        <div class="label-text">최종 필요 용량</div>
        <div class="value-text" style="color:#00FFC8;">{total_val:.3f} {drug['unit']}</div>
        <div class="label-text">실제 조제 볼륨 (Vial 농도 기준)</div>
        <div class="value-text">{needed_ml:.2f} ml</div>
        <div style="color:#666; font-size:12px;">계산식: {process_str}</div>
        <div style="color:#666; font-size:12px; margin-top:5px;">Vial 규격: {drug['vial']}</div>
    </div>
    """, unsafe_allow_all_html=True)

with res_col2:
    st.subheader("📋 Administration Protocol")
    st.write(f"**희석액 정보:** {drug['diluent']}")
    st.markdown(f"""
    <div style="background-color:#111; padding:15px; border-radius:10px; border-left:5px solid #00FFC8;">
        {drug['protocol']}
    </div>
    """, unsafe_allow_all_html=True)

# 7. 예외 경고 처리
if species == "Dog" and weight < 10 and "BSA" in basis:
    st.warning("⚠️ Small Dog Warning: 10kg 미만 소형견은 BSA 기준 시 독성이 강할 수 있습니다.")

if "아드리아마이신" in drug_name:
    st.error("❗ Doxorubicin 경고: 개(심초음파), 고양이(신장수치) 확인 필수. 카디옥산 전처치를 고려하십시오.")

st.markdown("---")
st.caption(f"Veterinary Chemo Dose Calculator v2.5 | Hospital: Royal Vet Center | Guided by AAHA & VCOG-CTCAE v2")
