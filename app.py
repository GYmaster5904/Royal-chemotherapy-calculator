import streamlit as st

# 1. 에러 유발 가능성이 있는 set_page_config와 CSS 스타일을 모두 제거했습니다.
# 2. 오직 표준 위젯만 사용하여 파이썬 3.13 충돌을 피합니다.

# 데이터베이스 (10종 약물 데이터 완벽 복구)
DRUG_DATA = {
    "로이나제주 (L-Asparaginase)": {"conc": 2000, "dose": 400.0, "unit": "IU/kg", "vial": "10,000 IU/Vial", "diluent": "0.9% NaCl", "prot": "전처치: Diphen(IM). SC 또는 IM 권장. 췌장염 주의."},
    "벨바스틴주 (Vinblastine)": {"conc": 1.0, "dose": 2.0, "unit": "mg/m2", "vial": "10mg/Vial", "diluent": "0.9% NaCl", "prot": "IV Bolus. Vesicant(조직괴사) 주의. Vincristine보다 골수독성 강함."},
    "빈크란주 (Vincristine)": {"conc": 1.0, "dose": 0.7, "unit": "mg/m2", "vial": "1mg/Vial", "diluent": "0.9% NaCl", "prot": "IV Bolus. Vesicant. 신경독성(장마비, 부전마비) 모니터링."},
    "아드리아마이신 (Doxorubicin)": {"conc": 2.0, "dose": 30.0, "unit": "mg/m2", "vial": "10mg/5ml", "diluent": "0.9% NaCl", "prot": "전처치: Diphen+Dexa. 20분 저속 IV. 개(심독성), 고양이(신독성) 주의."},
    "카보티놀주 (Carboplatin)": {"conc": 10.0, "dose": 300.0, "unit": "mg/m2", "vial": "150mg/15ml", "diluent": "5% Dextrose (D5W) 필수", "prot": "NaCl 혼합 금지. IRIS Stage 3 이상 강력 감량."},
    "시타라빈주 (Cytarabine)": {"conc": 20.0, "dose": 100.0, "unit": "mg/m2", "vial": "100mg/5ml", "diluent": "0.9% NaCl 또는 D5W", "prot": "SC 또는 CRI 투여. 골수억제 주의."},
    "엔독산주 (Cyclophosphamide)": {"conc": 20.0, "dose": 250.0, "unit": "mg/m2", "vial": "500mg/Vial", "diluent": "0.9% NaCl", "prot": "전처치: Furosemide. 방광염 주의. 충분한 음수 유도."},
    "미트론주 (Mitoxantrone)": {"conc": 2.0, "dose": 5.5, "unit": "mg/m2", "vial": "20mg/10ml", "diluent": "0.9% NaCl", "prot": "15분 IV 주입. Doxorubicin 대체제. 소변색 변화 가능성."},
    "카디옥산주 (Dexrazoxane)": {"conc": 10.0, "dose": 10.0, "unit": "ratio (10:1)", "vial": "500mg/Vial", "diluent": "0.9% NaCl", "prot": "Dox 심독성 예방. Dox 주입 전 투여 완료."},
    "박스루킨15주 (IL-2)": {"conc": 100.0, "dose": 100.0, "unit": "μg/head", "vial": "100μg/1ml", "diluent": "0.9% NaCl", "prot": "면역요법제. 발열/오한 반응 모니터링."}
}

st.title("Vet Oncology Calculator")
st.write("---")

# 환자 정보 입력
species = st.radio("종 선택", ["Dog", "Cat"])
weight = st.number_input("체중 (kg)", min_value=0.1, value=10.0, step=0.1)

# BSA 계산
k = 10.1 if species == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100
st.info(f"계산된 체표면적 (BSA): {bsa:.4f} m²")

st.write("---")

# 항암제 설정
drug_name = st.selectbox("항암제 선택", list(DRUG_DATA.keys()))
drug = DRUG_DATA[drug_name]

# 계산 기준 선택
basis = st.radio("계산 기준", ["BSA 기준", "체중 기준"], 
                index=0 if "m2" in drug["unit"] else 1)

# 용량 조정
target_dose = st.number_input(f"설정 용량 ({drug['unit']})", value=float(drug["dose"]))
reduction = st.select_slider("감량 조정 (%)", options=[50, 60, 70, 80, 90, 100], value=100)

# 최종 계산
if "BSA" in basis:
    total_val = bsa * target_dose * (reduction / 100)
    process = f"{bsa:.4f} m² x {target_dose} x {reduction}%"
else:
    total_val = weight * target_dose * (reduction / 100)
    process = f"{weight} kg x {target_dose} x {reduction}%"

final_ml = total_val / drug["conc"]

st.write("---")

# 결과 출력 (st.metric 대신 일반 text와 success 박스 사용)
st.subheader("계산 결과")
st.success(f"필요 용량: {total_val:.3f} {drug['unit'].split('/')[0]}")
st.warning(f"조제 볼륨: {final_ml:.2f} ml")

st.write(f"**희석액:** {drug['diluent']}")
st.write(f"**프로토콜:** {drug['prot']}")
st.caption(f"산식: {process} | 농도: {drug['conc']} / ml")

if species == "Dog" and weight < 10 and "BSA" in basis:
    st.error("⚠️ 10kg 미만 소형견입니다. mg/kg 환산을 권장합니다.")

st.write("---")
st.caption("Royal Vet Oncology v3.0 | Python 3.13 Safe Mode")

