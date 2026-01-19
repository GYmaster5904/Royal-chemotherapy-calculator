import streamlit as st

# 1. 페이지 설정 및 브라우저 탭 이름
st.set_page_config(page_title="Royal Vet Oncology Center", layout="wide")

# 2. 블랙 & 네온 그린 테마 (CSS) - 에러를 방지하기 위해 최적화된 문법
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    
    /* 입력 위젯 스타일 */
    .stSelectbox, .stNumberInput, .stSlider { background-color: #1e1e1e !important; color: #ffffff !important; }
    
    /* 결과 박스 (Neon Green 포인트) */
    .result-container {
        background-color: #151515;
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #00FFC8;
        box-shadow: 0 0 20px rgba(0, 255, 200, 0.15);
        margin-bottom: 20px;
    }
    
    /* 텍스트 스타일 */
    h1, h2, h3 { color: #00FFC8 !important; }
    .label { color: #888888; font-size: 14px; margin-bottom: 5px; }
    .main-value { color: #00FFC8; font-size: 40px; font-weight: bold; }
    .sub-value { color: #ffffff; font-size: 35px; font-weight: bold; }
    </style>
    """, unsafe_allow_all_html=True)

# 3. 병원 사용 약물 마스터 데이터 (농도 및 프로토콜 상세 반영)
# conc: ml당 mg/IU/ug 수치
DRUG_MASTER = {
    "로이나제주 (L-Asparaginase)": {
        "vial": "10,000 IU/Vial", "unit": "IU", "conc": 2000, "def_dose": 400.0, "d_unit": "IU/kg",
        "diluent": "0.9% NaCl (Vial당 5ml 희석 시 2,000IU/ml)", 
        "protocol": "<b>전처치:</b> Diphenhydramine (1mg/kg IM).<br><b>경로:</b> SC 또는 IM 권장 (IV 시 아나필락시스 위험 급증).<br><b>주의:</b> 응고부전, 췌장염 병력 환자 주의."
    },
    "벨바스틴주 (Vinblastine)": {
        "vial": "10mg/Vial", "unit": "mg", "conc": 1.0, "def_dose": 2.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>전처치:</b> 필요 시 항히스타민.<br><b>경로:</b> IV Bolus.<br><b>주의:</b> Vesicant (혈관외 유출 시 조직괴사 주의). Vincristine보다 골수독성 강함."
    },
    "빈크란주 (Vincristine)": {
        "vial": "1mg/Vial", "unit": "mg", "conc": 1.0, "def_dose": 0.7, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>경로:</b> IV Bolus (Side arm).<br><b>주의:</b> Vesicant. 신경독성(장마비, 부전마비) 모니터링 필수."
    },
    "아드리아마이신 (Doxorubicin)": {
        "vial": "10mg/5ml (2mg/ml)", "unit": "mg", "conc": 2.0, "def_dose": 30.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl (보통 1:1 희석하여 1mg/ml로 투여 권장)", 
        "protocol": "<b>전처치:</b> Diphenhydramine + Dexamethasone.<br><b>경로:</b> 15~30분 저속 IV.<br><b>주의:</b> 개(심독성), 고양이(신독성). 카디옥산 전처치 고려."
    },
    "카보티놀주 (Carboplatin)": {
        "vial": "150mg/15ml (10mg/ml)", "unit": "mg", "conc": 10.0, "def_dose": 300.0, "d_unit": "mg/m2",
        "diluent": "5% Dextrose (D5W) 필수 (NaCl 혼합 금지)", 
        "protocol": "<b>경로:</b> 15~30분 IV.<br><b>주의:</b> 신장 배설 약물. IRIS Stage 3 이상 강력 감량. 혈소판 감소증(Nadir) 모니터링."
    },
    "시타라빈주 (Cytarabine)": {
        "vial": "100mg/5ml (20mg/ml)", "unit": "mg", "conc": 20.0, "def_dose": 100.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl 또는 D5W", 
        "protocol": "<b>경로:</b> SC (보통 2-4일간 BID) 또는 CRI 투여.<br><b>주의:</b> 골수억제 매우 강함, 중추신경계 종양 시 사용."
    },
    "박스루킨15주 (IL-2)": {
        "vial": "100μg/1ml", "unit": "μg", "conc": 100.0, "def_dose": 100.0, "d_unit": "μg/head",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>주의:</b> 면역요법제. 발열, 오한 등 면역 매개 반응 모니터링."
    },
    "엔독산주 (Cyclophosphamide)": {
        "vial": "500mg/Vial", "unit": "mg", "conc": 20.0, "def_dose": 250.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl (Vial당 25ml 희석 시 20mg/ml)", 
        "protocol": "<b>전처치:</b> Furosemide (2.2mg/kg) 병용 권장.<br><b>주의:</b> 무균성 출혈성 방광염 주의. 투여 후 충분한 음수 및 배뇨 유도."
    },
    "미트론주 (Mitoxantrone)": {
        "vial": "20mg/10mL (2mg/ml)", "unit": "mg", "conc": 2.0, "def_dose": 5.5, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "protocol": "<b>경로:</b> 15분 IV 주입.<br><b>주의:</b> Doxorubicin 대체제. 투여 후 소변색 변화(청록색) 가능성 보호자 상담."
    },
    "카디옥산주 (Dexrazoxane)": {
        "vial": "500mg/Vial", "unit": "mg", "conc": 10.0, "def_dose": 10.0, "d_unit": "ratio (10:1)",
        "diluent": "전용 희석액 사용 후 0.9% NaCl", 
        "protocol": "<b>목적:</b> Doxorubicin 심독성 예방.<br><b>용량:</b> Doxorubicin 용량(mg)의 10배 투여 (10:1).<br><b>투여:</b> Dox 주입 전 완료."
    }
}

# 4. 사이드바 - 환자 정보 입력부
st.sidebar.title("🐾 Patient Profile")
species = st.sidebar.radio("종 선택", ["Dog", "Cat"])
weight = st.sidebar.number_input("체중 (kg)", min_value=0.1, value=10.0, step=0.1)

# BSA 계산 (개 10.1, 고양이 10.0)
k = 10.1 if species == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='color:#888;'>계산된 체표면적</p>", unsafe_allow_all_html=True)
st.sidebar.title(f"{bsa:.4f} m²")

# 5. 메인 화면 - 설정부
st.title("🩺 Veterinary Chemo Dose Calculator")

# 약물 선택 레이아웃
c1, c2 = st.columns(2)

with c1:
    selected_name = st.selectbox("항암제 선택", list(DRUG_MASTER.keys()))
    drug = DRUG_MASTER[selected_name]
    
    # 단위 선택 (기본값 설정 로직)
    basis = st.radio("계산 기준", ["체표면적(BSA) 기준", "체중(kg) 기준"], 
                    index=0 if "m2" in drug["d_unit"] else 1)

with c2:
    # 목표 용량 및 감량
    target_val = st.number_input(f"설정 용량 ({drug['d_unit']})", value=float(drug["def_dose"]))
    reduction = st.select_slider("용량 조절 (Condition %)", options=[50, 60, 70, 80, 90, 100], value=100)

# 계산 로직
if "BSA" in basis:
    final_dose = bsa * target_val * (reduction / 100)
    process_txt = f"{bsa:.4f} m² × {target_val} × {reduction}%"
else:
    final_dose = weight * target_val * (reduction / 100)
    process_txt = f"{weight} kg × {target_val} × {reduction}%"

final_ml = final_dose / drug["conc"]

# 6. 최종 결과 및 프로토콜 출력
st.markdown("---")
res_c1, res_c2 = st.columns([1, 1])

with res_c1:
    st.markdown(f"""
    <div class="result-container">
        <div class="label">최종 필요 용량 ({selected_name})</div>
        <div class="main-value">{final_dose:.3f} {drug['unit']}</div>
        <br>
        <div class="label">실제 조제 볼륨 (Vial 농도 기준)</div>
        <div class="sub-value">{final_ml:.2f} ml</div>
        <div style="color:#666; font-size:12px; margin-top:15px;">산식: {process_txt}</div>
        <div style="color:#666; font-size:12px;">Vial 정보: {drug['vial']} | 농도: {drug['conc']}{drug['unit']}/ml</div>
    </div>
    """, unsafe_allow_all_html=True)

with res_c2:
    st.subheader("📋 Administration Protocol")
    st.write(f"**희석액:** {drug['diluent']}")
    st.markdown(f"""
    <div style="background-color:#111; padding:15px; border-radius:10px; border-left:5px solid #00FFC8; line-height:1.6;">
        {drug['protocol']}
    </div>
    """, unsafe_allow_all_html=True)

# 7. 추가 경고 알림
if species == "Dog" and weight < 10 and "BSA" in basis:
    st.warning("⚠️ Small Dog Warning: 10kg 미만 소형견은 BSA 기준 시 독성 위험이 큽니다. mg/kg 환산을 고려하세요.")

if "아드리아마이신" in selected_name:
    st.error("❗ Doxorubicin 경고: 개(심초음파 필수), 고양이(신장수치 확인). Cardioxane 병용을 권장합니다.")

st.markdown("---")
st.caption("Hospital: Royal Vet Center | Powered by AAHA Oncology Guidelines & VCOG-CTCAE v2")


