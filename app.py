import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Royal Vet Oncology Calculator", layout="centered")

# 2. 약물 마스터 데이터베이스 (첨부 인서트지 내용 100% 반영)
DRUG_MASTER = {
    "로이나제주 (L-Asparaginase)": {
        "recon": "주사용수 2~5ml (아닐 시 백탁부유물 발생)",
        "route": "IV (인서트 기준), IM/SC 가능",
        "diluent": "생리식염수 또는 5% 포도당액",
        "etc": "IM 투여 시 통증 유발 가능. 투여 후 30분간 아나필락시스 관찰.",
        "premed": "Diphenhydramine + Dexamethasone 필수 투여",
        "conc": 2000, "def_dose": 400.0, "unit": "IU", "d_unit": "IU/kg"
    },
    "벨바스틴주 (Vinblastine)": {
        "recon": "제품 내 첨부된 주사용수 10ml",
        "route": "IV 전용",
        "diluent": "생리식염수 (단, NaCl이 이미 첨가된 제품은 주사용수만 이용)",
        "etc": "1분 이내로 신속히 주입. 혈관외 유출 주의(Vesicant).",
        "premed": "필요 시 항히스타민 전처치",
        "conc": 1.0, "def_dose": 2.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "빈크란주 (Vincristine)": {
        "recon": "생리식염수",
        "route": "IV 전용",
        "diluent": "주사용 증류수 또는 생리식염수",
        "etc": "1분 이내로 주입. 신경독성(장마비 등) 주의.",
        "premed": "없음 (환자 상태에 따라 판단)",
        "conc": 1.0, "def_dose": 0.7, "unit": "mg", "d_unit": "mg/m2"
    },
    "아드리아마이신 (Doxorubicin)": {
        "recon": "주사용수",
        "route": "IV 전용 (IM, SC 절대금지 - 조직괴사 위험)",
        "diluent": "생리식염수 또는 주사용수",
        "etc": "헤파린 혼합 시 약효 저하. 심독성 주의. 20분 이상 저속 주입.",
        "premed": "Diphenhydramine + Dexamethasone 필수 투여",
        "conc": 2.0, "def_dose": 30.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "카보티놀주 (Carboplatin)": {
        "recon": "주사제 (주사용수)",
        "route": "IV 전용",
        "diluent": "주사용수, 5% 포도당, 생리식염수",
        "etc": "알루미늄 함유 기구 사용 금지(침전). 15~60분 이내 주입.",
        "premed": "항구토제 권장",
        "conc": 10.0, "def_dose": 300.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "시타라빈주 (Cytarabine)": {
        "recon": "주사용수",
        "route": "IV, SC, IM 가능",
        "diluent": "생리식염수 또는 5% 포도당",
        "etc": "Bolus 투여 시 20% 포도당 이용. 골수억제 주의.",
        "premed": "없음",
        "conc": 20.0, "def_dose": 100.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "엔독산주 (Cyclophosphamide)": {
        "recon": "주사용수 또는 생리식염수",
        "route": "IV, IM, IP, Intrapleural inj.",
        "diluent": "5% 포도당, 5% 포도당 생리식염수, 링거젖산 주사액 등",
        "etc": "장기 투여 시 방광종양/출혈성 방광염 위험. 투여 후 배뇨 유도 필수.",
        "premed": "Furosemide 병용 권장",
        "conc": 20.0, "def_dose": 250.0, "unit": "mg", "d_unit": "mg/m2"
    },
    "미트론주 (Mitoxantrone)": {
        "recon": "주사제 (주사용수)",
        "route": "IV 전용",
        "diluent": "생리식염수, 5% 포도당, 0.18% 염화나트륨 등",
        "etc": "간독성 및 신독성 강함. 소변색 변화(청록색) 보호자 상담 필수.",
        "premed": "없음",
        "conc": 2.0, "def_dose": 5.5, "unit": "mg", "d_unit": "mg/m2"
    },
    "카디옥산주 (Dexrazoxane)": {
        "recon": "주사용수",
        "route": "IV",
        "diluent": "링거젖산용액 또는 0.16M 락트산나트륨 용액",
        "etc": "Doxorubicin 투여 전 주입 완료 필수. 피부 접촉 주의.",
        "premed": "Doxorubicin 투여 15분 전 완료",
        "conc": 10.0, "def_dose": 10.0, "unit": "ratio (10:1)", "d_unit": "ratio"
    },
    "박스루킨15주 (IL-2)": {
        "recon": "없음 (액상 제품)",
        "route": "SC, 국소 투여",
        "diluent": "생리식염수",
        "etc": "수의 전용 면역요법제. 발열 및 오한 등 면역 반응 모니터링.",
        "premed": "없음",
        "conc": 100.0, "def_dose": 100.0, "unit": "ug", "d_unit": "ug/head"
    }
}

# 3. 메인 화면 구성
st.title("🩺 Royal Vet Oncology Calculator")
st.info("첨부해주신 약품 인서트지(Insert) 내용을 바탕으로 제작되었습니다.")

# 환자 정보 섹션
st.header("1. Patient Information")
breed = st.radio("종 선택", ["Dog", "Cat"], horizontal=True)
weight = st.number_input("체중 (kg) 입력", min_value=0.1, value=10.0, step=0.1)

# BSA 계산
k = 10.1 if breed == "Dog" else 10.0
bsa = (k * (weight ** (2/3))) / 100
st.write(f"**계산된 체표면적 (BSA): {bsa:.4f} m²**")

st.divider()

# 항암제 설정 섹션
st.header("2. Drug & Dose Setting")
drug_name = st.selectbox("사용할 항암제를 선택하세요", list(DRUG_MASTER.keys()))
drug = DRUG_MASTER[drug_name]

col1, col2 = st.columns(2)
with col1:
    # 로이나제, 카디옥산, 박스루킨은 기본 kg/head 기준, 나머지는 BSA 기준
    default_basis_idx = 1 if drug["d_unit"] in ["IU/kg", "ug/head", "ratio"] else 0
    basis = st.radio("계산 기준", ["체표면적(BSA) 기준", "체중(kg) 기준"], index=default_basis_idx)
    target_dose = st.number_input(f"목표 용량 ({drug['d_unit']})", value=float(drug["def_dose"]))

with col2:
    reduction = st.select_slider("환자 상태에 따른 감량 (%)", options=[50, 60, 70, 80, 90, 100], value=100)

# 최종 계산 실행
if "BSA" in basis:
    final_amt = bsa * target_dose * (reduction / 100)
    process = f"{bsa:.4f} m² x {target_dose} x {reduction}%"
else:
    final_amt = weight * target_dose * (reduction / 100)
    process = f"{weight} kg x {target_dose} x {reduction}%"

final_ml = final_amt / drug["conc"]

st.divider()

# 4. 결과 출력 (에러 방지를 위해 가장 단순하고 안전한 방식)
st.header("3. Preparation Result")
st.success(f"**최종 필요 용량: {final_amt:.3f} {drug['unit']}**")
st.warning(f"**주사기 조제 볼륨: {final_ml:.2f} ml**")
st.write(f"(계산 근거: {process} / 농도: {drug['conc']}{drug['unit']}/ml)")

st.divider()

# 5. 상세 프로토콜 출력
st.header("4. Administration Protocol")
st.write(f"🧪 **전처치 가이드:** {drug['premed']}")
st.write(f"💧 **제품 용해제:** {drug['recon']}")
st.write(f"💉 **희석액:** {drug['diluent']}")
st.write(f"🛣️ **투여 경로:** {drug['route']}")
st.write(f"⚠️ **상세 주의사항:** {drug['etc']}")

if breed == "Dog" and weight < 10 and "BSA" in basis:
    st.error("❗ 주의: 10kg 미만 소형견입니다. BSA 기준 투여 시 과용량 위험이 높으므로 mg/kg 환산을 권장합니다.")

st.write("---")
st.caption("Hospital: Royal Vet Center | Powered by AAHA & VCOG-CTCAE v2 Guidelines")
