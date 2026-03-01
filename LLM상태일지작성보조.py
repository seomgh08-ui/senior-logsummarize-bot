# 파일명: app.py

import streamlit as st
import google.generativeai as genai 

st.set_page_config(page_title="어르신 관찰일지 자동 요약 봇", page_icon="👴", layout="centered")

st.title(" 어르신 상태 관찰일지 자동 요약 ")
st.markdown("단어 몇 개만 툭툭 입력하세요. 공단 제출용 전문 리포트로 자동 변환해 드립니다.")

# 사용자가 입력하는 창
user_input = st.text_area(
    label="오늘 어르신의 상태를 간단히 입력하세요", 
    placeholder="예: 오늘 김할머니 점심 반 공기 드심. 기침 3번 하심. 낮잠 1시간 주무심.",
    height=150
)

if st.button("전문 용어로 변환하기"):
    if user_input == "":
        st.warning("⚠️ 내용을 먼저 입력해 주세요!")
    else:
        with st.spinner("전문 용어로 변환 중입니다... 🍳"):
            try:
                # ★ 핵심 보안 로직: 서버의 비밀 금고(secrets)에서 API 키를 몰래 꺼내옵니다.
                # 복지사님들은 화면에서 API 키를 입력할 필요가 전혀 없습니다.
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                system_prompt = """
                너는 노인장기요양기관에서 10년 이상 근무한 최고 전문가(사회복지사/요양보호사)야.
                사용자가 어르신의 오늘 하루 상태를 메모 형식의 단어나 짧은 문장으로 입력할 거야.
                너의 임무는 이 메모를 '국민건강보험공단 장기요양급여 제공기록지'에 
                바로 복사해서 붙여넣을 수 있도록 전문적이고 정제된 문장으로 바꾸는 거야.
                
                [규칙]
                1. 주관적인 감정표현은 배제하고, 객관적인 사실 기반으로 작성할 것.
                2. '드심' -> '섭취함', '주무심' -> '수면을 취함' 등 요양기관 공식 용어를 사용할 것.
                3. 문장은 "~하였음", "~관찰됨" 등의 개조식 또는 정중한 평어체로 마무리할 것.
                4. 환각현상(사용자가 입력하지 않은 증상이나 사실)을 절대 지어내지 말 것.
                5. 결과물은 인사말 없이 변환된 내용만 딱 출력할 것.
                """
                
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_prompt
                )
                
                generation_config = genai.types.GenerationConfig(temperature=0.3)
                
                response = model.generate_content(
                    user_input, 
                    generation_config=generation_config
                )
                
                st.success(" 변환이 완료되었습니다!")
                st.write(response.text)

            except Exception as e:
                st.error(f"🚨 상세 에러 로그: {e}")

               
