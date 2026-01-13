import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Royal Vet Oncology", layout="wide")

# 2. 스타일 정의 (에러 방지를 위해 간단하게 수정)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; }
    .result-card {
        background-color: #151515;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00FFC8;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #00FFC8 !important; }
    </style>
    """, unsafe_allow_all_html=True)

# 3. 약물 데이터베이스
INVENTORY = {
    "로이나제주 (L-Asparaginase)": {"conc": 2000, "def_dose": 400, "d_unit": "IU/kg", "unit": "IU", "diluent": "0.9% NaCl (5ml 희석 시 2000IU/ml)", "protocol": "전처치: Diphenhydramine (1mg/kg IM). SC/IM 권장."},
    "벨바스틴주 (Vinblastine)": {"conc": 1.0, "def_dose": 2.0, "d_unit": "mg/m2", "unit": "mg", "diluent": "0.9% NaCl", "protocol": "IV Bolus. Vesicant 주의."},
    "빈크란주 (Vincristine)": {"conc": 1.0, "def_dose": 0.7, "d_unit": "mg/m2", "unit": "mg", "diluent": "0.9% NaCl", "protocol": "IV Bolus. Vesicant, 신경독성 주의."},
    "아드리아마이신 (Doxorubicin)": {"conc": 2.0, "def_dose": 30.0, "d_unit": "mg/m2", "unit": "mg", "diluent": "0.9% NaCl", "protocol": "전처치: Diphen+Dexa. 15-30분 저속 IV."},
    "카보티놀주 (Carboplatin)": {"conc": 10.0, "def_dose": 300.0, "d_unit": "mg/m2", "unit": "mg", "diluent": "5% Dextrose (D5W) 필수", "protocol": "NaCl 혼합 금지. 15-30분 IV."},
    "시타라빈주 (Cytarabine)": {"conc": 20.0, "def_dose": 100.0, "d_unit": "mg/m2", "unit": "mg", "diluent": "0.9% NaCl/D5W", "protocol": "SC 또는 CRI. 골수억제 주의."},
    "박스루킨15주 (IL-2)": {"conc": 100.0, "def_dose": 100.0, "d_unit": "μg/head", "unit": "μg", "diluent": "0.9% NaCl", "protocol": "면역요법제. 모니터링 필수."},
    "엔독산주 (Cyclophosphamide)": {"conc": 20.0, "def_dose": 250.0, "d_unit": "mg/m2", "unit": "mg", "diluent": "0.9% NaCl", "protocol": "전처치: Furosemide 권장. 방광염 주의."},
    "미트론주 (Mitoxantrone)": {"conc": 2.0, "def_dose": 5.5, "d_unit": "mg/m2", "unit": "mg", "diluent": "0.9% NaCl", "protocol": "15분 IV. 소변색 변화 가능."},
    "카디옥산주 (Dexrazoxane)": {"conc": 10.0, "def_dose": 10.0, "d_unit": "ratio (10:1)", "unit": "mg", "diluent": "0.9% NaCl", "protocol": "Dox 투여 15분 전 완료. Dox 용량의 10배."}
}

# 4. 사이드바
st.sidebar.title("🐾 Patient Info")
species = st.sidebar.radio("종 선택", ["Dog", "Cat"])
weight = st.sidebar.number_input("체중 (kg)", min_value=0.1, value=10.0)
k = 10.1 if species == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100
st.sidebar.write(f"### BSA: {bsa:.4f} m²")

# 5. 메인
st.title("🩺 Chemo Dose Calculator")
c1, c2 = st.columns(2)

with c1:
    drug_name = st.selectbox("항암제 선택", list(INVENTORY.keys()))
    drug = INVENTORY[drug_name]
    basis = st.radio("계산 기준", ["BSA(m2)", "Weight(kg)"], index=0 if drug["d_unit"] == "mg/m2" else 1)

with c2:
    target = st.number_input(f"목표 용량 ({drug['d_unit']})", value=float(drug["def_dose"]))
    reduction = st.select_slider("용량 조정 (%)", options=[50, 60, 70, 80, 90, 100], value=100)

# 계산
if "BSA" in basis:
    total_val = bsa * target * (reduction / 100)
else:
    total_val = weight * target * (reduction / 100)
needed_ml = total_val / drug["conc"]

# 결과 표시
st.markdown("---")
res1, res2 = st.columns(2)
with res1:
    st.markdown(f"""
    <div class="result-card">
        <h3>최종 필요 용량</h3>
        <h1 style="color:#00FFC8;">{total_val:.3f} {drug['unit']}</h1>
        <h3>실제 조제 볼륨</h3>
        <h1 style="color:#ffffff;">{needed_ml:.2f} ml</h1>
    </div>
    """, unsafe_allow_all_html=True)

with res2:
    st.subheader("📋 Protocol")
    st.write(f"**희석액:** {drug['diluent']}")
    st.info(drug['protocol'])

st.caption("Royal Vet Oncology v2.6 | Python 3.11 Mode")
