import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Royal Vet Oncology Center", layout="wide")

# 2. 블랙 테마 및 네온 그린 스타일 강제 적용 (안정적인 표준 문법)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    .stSelectbox, .stNumberInput, .stSlider { background-color: #1e1e1e !important; color: #ffffff !important; }
    h1, h2, h3 { color: #00FFC8 !important; }
    .result-box {
        background-color: #151515;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00FFC8;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #111; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #00FFC8;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_all_html=True)

# 3. 인서트지(Insert) 기반 약물 마스터 데이터베이스 (10종 완벽 누락 없음)
DRUG_MASTER = {
    "로이나제주 (L-Asparaginase)": {
        "recon": "주사용수 2~5ml (아닐 시 백탁부유물 발생)",
        "route": "IV (인서트 기준), IM/SC 가능",
        "diluent": "생리식염수 또는 5% 포도당액",
        "etc": "IM 투여 시 통증 유발 가능. 투여 후 30분간 아나필락시스 관찰.",
        "premed": "Diphenhydramine + Dexamethasone 필수",
        "conc": 2000, "def_dose": 400.0, "unit": "IU", "d_unit": "IU/kg"
    },
    "벨바스틴주 (Vinblastine)": {
        "recon": "제품 내 첨부된 주사용수 10ml",
        "route": "IV 전용",
        "diluent": "생리식염수 (NaCl 포함 제품은 주사용수만 이용)",
        "etc": "1분 이내로 신속히 주입. 혈관외 유출 주의(Vesicant).",
        "premed": "필요 시 항히스타민",
        "conc": 1.0, "def_dose": 2.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "빈크란주 (Vincristine)": {
        "recon": "생리식염수",
        "route": "IV 전용",
        "diluent": "주사용 증류수 또는 생리식염수",
        "etc": "1분 이내로 주입. 신경독성(장마비 등) 주의.",
        "premed": "없음",
        "conc": 1.0, "def_dose": 0.7, "unit": "mg", "d_unit": "mg/m2"
    },
    "아드리아마이신 (Doxorubicin)": {
        "recon": "주사용수 (10mg/5ml 제품)",
        "route": "IV 전용 (IM, SC 절대금지)",
        "diluent": "생리식염수 또는 주사용수",
        "etc": "헤파린 혼합 시 약효 저하. 심독성 주의(개).",
        "premed": "Diphenhydramine + Dexamethasone 필수",
        "conc": 2.0, "def_dose": 30.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "카보티놀주 (Carboplatin)": {
        "recon": "주사용수 (150mg/15ml 제품)",
        "route": "IV",
        "diluent": "주사용수, 5% 포도당, 생리식염수",
        "etc": "알루미늄 함유 기구 사용 금지(침전). 15~60분 이내 투여.",
        "premed": "항구토제 권장",
        "conc": 10.0, "def_dose": 300.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "시타라빈주 (Cytarabine)": {
        "recon": "주사용수 (100mg/5ml 제품)",
        "route": "IV, SC, IM",
        "diluent": "생리식염수 또는 5% 포도당",
        "etc": "Bolus 투여 시 20% 포도당 이용. 골수억제 주의.",
        "premed": "없음",
        "conc": 20.0, "def_dose": 100.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "엔독산주 (Cyclophosphamide)": {
        "recon": "주사용수 또는 생리식염수 (500mg/Vial)",
        "route": "IV, IM, IP, Intrapleural",
        "diluent": "5% 포도당, 링거액, Saline 등 가능",
        "etc": "장기 투여 시 방광염 위험. 투여 후 배뇨 유도 필수.",
        "premed": "Furosemide 권장",
        "conc": 20.0, "def_dose": 250.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "미트론주 (Mitoxantrone)": {
        "recon": "주사용수 (20mg/10ml 제품)",
        "route": "IV 전용",
        "diluent": "생리식염수, 5% 포도당 등",
        "etc": "간독성 및 신독성 강함. 소변색 변화(청록색) 고지.",
        "premed": "없음",
        "conc": 2.0, "def_dose": 5.5, "unit": "mg", "d_unit": "mg/m2"
    },
    "카디옥산주 (Dexrazoxane)": {
        "recon": "주사용수 (500mg/Vial)",
        "route": "IV",
        "diluent": "링거젖산용액 또는 0.16M 락트산나트륨",
        "etc": "Doxorubicin 투여 전 주입. 피부 접촉 시 피부반응 주의.",
        "premed": "Doxorubicin 투여 15분 전 완료",
        "conc": 10.0, "def_dose": 10.0, "unit": "ratio(10:1)", "label": "mg"
    },
    "박스루킨15주 (IL-2)": {
        "recon": "없음 (액상 100μg/1ml)",
        "route": "SC, 국소",
        "diluent": "생리식염수",
        "etc": "면역요법제. 발열 및 오한 모니터링.",
        "premed": "없음",
        "conc": 100.0, "def_dose": 100.0, "unit": "μg", "d_unit": "μg/head"
    }
}

# 4. 사이드바 - 환자 정보
st.sidebar.title("🐾 Patient Info")
species = st.sidebar.radio("종 선택", ["Dog", "Cat"])
weight = st.sidebar.number_input("체중 (kg)", min_value=0.1, value=5.0, step=0.1)

k = 10.1 if species == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100
st.sidebar.markdown(f"### 체표면적 (BSA): **{bsa:.4f} m²**")

# 5. 메인 설정 화면
st.title("🩺 Royal Veterinary Oncology Center")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 약물 및 기준 선택")
    drug_name = st.selectbox("사용 항암제 선택", list(DRUG_MASTER.keys()))
    drug = DRUG_MASTER[drug_name]
    
    # 단위 기준 자동 선택
    basis = st.radio("계산 기준", ["체표면적(BSA) 기준", "체중(kg) 기준"], 
                    index=1 if "kg" in drug["d_unit"] or "head" in drug["d_unit"] else 0)

with col2:
    st.subheader("2. 투여량 및 감량")
    target_dose = st.number_input(f"설정 용량 ({drug['d_unit']})", value=float(drug["def_dose"]))
    reduction = st.select_slider("용량 조정 (%)", options=[50, 60, 70, 80, 90, 100], value=100)

# 계산 로직
if "BSA" in basis:
    final_amt = bsa * target_dose * (reduction / 100)
    logic_txt = f"{bsa:.4f} m² × {target_dose} × {reduction}%"
else:
    final_amt = weight * target_dose * (reduction / 100)
    logic_txt = f"{weight} kg × {target_dose} × {reduction}%"

final_ml = final_amt / drug["conc"]

# 6. 최종 결과 표시
st.write("---")
res_c1, res_c2 = st.columns(2)

with res_c1:
    st.markdown(f"""
    <div class="result-box">
        <p style='color:#888; font-size:16px; margin-bottom:5px;'>최종 필요 용량 ({drug_name})</p>
        <p style='color:#00FFC8; font-size:40px; font-weight:bold; margin-bottom:15px;'>{final_amt:.3f} {drug['unit']}</p>
        <p style='color:#888; font-size:16px; margin-bottom:5px;'>주사기 조제 볼륨</p>
        <p style='color:#ffffff; font-size:40px; font-weight:bold;'>{final_ml:.2f} ml</p>
        <p style='color:#555; font-size:12px; margin-top:10px;'>산식: {logic_txt}</p>
    </div>
    """, unsafe_allow_all_html=True)

with res_c2:
    st.subheader("📋 Administration Protocol")
    st.markdown(f"""
    <div class="info-box"><b>[전처치 가이드]</b><br>{drug['premed']}</div>
    <div class="info-box"><b>[제품 용해 및 희석]</b><br>용해제: {drug['recon']}<br>희석액: {drug['diluent']}</div>
    <div class="info-box"><b>[투여 경로]</b><br>{drug['route']}</div>
    """, unsafe_allow_all_html=True)

# 7. 기타 상세 주의사항
st.info(f"**상세 주의사항:** {drug['etc']}")

# 8. 경고 메시지
if species == "Dog" and weight < 10 and "BSA" in basis:
    st.error("⚠️ [Small Dog Warning] 10kg 미만 소형견입니다. BSA 기준 투여 시 독성이 강할 수 있으니 mg/kg 환산을 권장합니다.")

st.write("---")
st.caption("Veterinary Chemo Dose Calculator v4.0 | Created for Royal Vet Center | Data based on Drug Inserts")

