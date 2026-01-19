import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Royal Vet Oncology", layout="wide")

# 2. 블랙 & 네온 스타일 (안정성 최우선)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    .stSelectbox, .stNumberInput, .stSlider { background-color: #1e1e1e !important; color: #ffffff !important; }
    .result-card {
        background-color: #151515;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00FFC8;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #00FFC8 !important; }
    .label { color: #888888; font-size: 14px; }
    .value { color: #00FFC8; font-size: 35px; font-weight: bold; }
    .sub-value { color: #ffffff; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_all_html=True)

# 3. 약전 데이터베이스 (10종 완벽 반영)
DRUGS = {
    "로이나제주 (L-Asparaginase)": {
        "vial": "10,000 IU/Vial", "conc": 2000, "unit": "IU", "def_dose": 400.0, "d_unit": "IU/kg",
        "diluent": "0.9% NaCl (5ml 희석 시 2000IU/ml)", 
        "prot": "전처치: Diphen(IM). SC/IM 권장 (IV 시 쇼크 위험). 췌장염/응고부전 주의."
    },
    "벨바스틴주 (Vinblastine)": {
        "vial": "10mg/Vial", "conc": 1.0, "unit": "mg", "def_dose": 2.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "prot": "IV Bolus. Vesicant(조직괴사) 주의. Vincristine보다 골수독성 강함."
    },
    "빈크란주 (Vincristine)": {
        "vial": "1mg/Vial", "conc": 1.0, "unit": "mg", "def_dose": 0.7, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "prot": "IV Bolus (Side arm). Vesicant. 신경독성(장마비, 부전마비) 모니터링."
    },
    "아드리아마이신 (Doxorubicin)": {
        "vial": "10mg/5ml (2mg/ml)", "conc": 2.0, "unit": "mg", "def_dose": 30.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "prot": "전처치: Diphen+Dexa. 20분 저속 IV. 개(심독성), 고양이(신독성) 주의."
    },
    "카보티놀주 (Carboplatin)": {
        "vial": "150mg/15ml (10mg/ml)", "conc": 10.0, "unit": "mg", "def_dose": 300.0, "d_unit": "mg/m2",
        "diluent": "5% Dextrose (D5W) 필수", 
        "prot": "NaCl 혼합 절대 금지. IRIS Stage 3 이상 강력 감량. Nadir(2주차) 모니터링."
    },
    "시타라빈주 (Cytarabine)": {
        "vial": "100mg/5ml (20mg/ml)", "conc": 20.0, "unit": "mg", "def_dose": 100.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl 또는 D5W", 
        "prot": "SC(분할투여) 또는 CRI. 골수억제 강함. 주로 CNS 종양에 사용."
    },
    "박스루킨15주 (IL-2)": {
        "vial": "100μg/1ml", "conc": 100.0, "unit": "μg", "def_dose": 100.0, "d_unit": "μg/head",
        "diluent": "0.9% NaCl", 
        "prot": "면역요법제. 투여 후 발열, 오한 등 면역 반응 모니터링 필수."
    },
    "엔독산주 (Cyclophosphamide)": {
        "vial": "500mg/Vial", "conc": 20.0, "unit": "mg", "def_dose": 250.0, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl (25ml 희석 시 20mg/ml)", 
        "prot": "전처치: Furosemide 권장. 무균성 출혈성 방광염 주의. 충분한 음수 유도."
    },
    "미트론주 (Mitoxantrone)": {
        "vial": "20mg/10ml (2mg/ml)", "conc": 2.0, "unit": "mg", "def_dose": 5.5, "d_unit": "mg/m2",
        "diluent": "0.9% NaCl", 
        "prot": "15분 IV 주입. Doxorubicin 대체제. 소변색 변화(청록색) 가능성 고지."
    },
    "카디옥산주 (Dexrazoxane)": {
        "vial": "500mg/Vial", "conc": 10.0, "unit": "mg", "def_dose": 10.0, "d_unit": "ratio (10:1)",
        "diluent": "0.9% NaCl", 
        "prot": "목적: Dox 심독성 예방. Dox 용량의 10배 투여. Dox 투여 전 주입 완료."
    }
}

# 4. 사이드바 입력
st.sidebar.title("🐾 Patient Info")
species = st.sidebar.radio("종 선택", ["Dog", "Cat"])
weight = st.sidebar.number_input("체중 (kg)", min_value=0.1, value=10.0, step=0.1)

k = 10.1 if species == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100
st.sidebar.markdown(f"### BSA: **{bsa:.4f} m²**")

# 5. 메인 섹션
st.title("🩺 Veterinary Chemo Calculator")

drug_name = st.selectbox("항암제 선택", list(DRUGS.keys()))
drug = DRUGS[drug_name]

col1, col2 = st.columns(2)
with col1:
    basis = st.radio("계산 기준", ["BSA 기준", "체중 기준"], 
                    index=0 if "m2" in drug["d_unit"] else 1)
    target_dose = st.number_input(f"설정 용량 ({drug['d_unit']})", value=float(drug["def_dose"]))

with col2:
    reduction = st.select_slider("용량 조정 (%)", options=[50, 60, 70, 80, 90, 100], value=100)

# 계산 실행
if "BSA" in basis:
    final_val = bsa * target_dose * (reduction / 100)
    calc_str = f"{bsa:.4f}m² × {target_dose} × {reduction}%"
else:
    final_val = weight * target_dose * (reduction / 100)
    calc_str = f"{weight}kg × {target_dose} × {reduction}%"

final_ml = final_val / drug["conc"]

# 6. 결과 출력 (HTML 커스텀 카드로 에러 방지)
st.markdown("---")
res1, res2 = st.columns(2)

with res1:
    st.markdown(f"""
    <div class="result-card">
        <div class="label">최종 필요 용량 ({drug_name})</div>
        <div class="value">{final_val:.3f} {drug['unit']}</div>
        <br>
        <div class="label">실제 조제 볼륨 (Vial 농도 기준)</div>
        <div class="sub-value">{final_ml:.2f} ml</div>
        <div style="color:#666; font-size:12px; margin-top:15px;">산식: {calc_str}</div>
        <div style="color:#666; font-size:12px;">농도: {drug['conc']} {drug['unit']}/ml | {drug['vial']}</div>
    </div>
    """, unsafe_allow_all_html=True)

with res2:
    st.subheader("📋 Protocol & Admin")
    st.write(f"**권장 희석액:** {drug['diluent']}")
    st.markdown(f"""
    <div style="background-color:#111; padding:15px; border-radius:10px; border-left:5px solid #00FFC8; line-height:1.6;">
        {drug['prot']}
    </div>
    """, unsafe_allow_all_html=True)

if species == "Dog" and weight < 10 and "BSA" in basis:
    st.warning("⚠️ 10kg 미만 소형견입니다. BSA 기준 투여 시 과용량 위험이 있습니다.")

st.caption("Royal Vet Oncology Calculator v2.9 | 안정화 버전")


