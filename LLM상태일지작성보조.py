# 파일명: app.py

import streamlit as st
import google.generativeai as genai 

st.set_page_config(page_title="어르신 관찰일지 자동 요약 봇", page_icon="📝", layout="centered")

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
        st.warning("내용을 먼저 입력해 주세요!")
    else:
        with st.spinner("전문 용어로 변환 중입니다... "):
            try:
                # ★ 핵심 보안 로직: 서버의 비밀 금고(secrets)에서 API 키를 몰래 꺼내옵니다.
                # 복지사님들은 화면에서 API 키를 입력할 필요가 전혀 없습니다.
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                system_prompt = """
                너는 노인장기요양기관에서 10년 이상 근무한 최고 전문가(사회복지사/요양보호사)야.
                사용자가 어르신의 오늘 하루 상태를 메모 형식의 단어나 짧은 문장으로 입력할 거야.
                너의 임무는 이 짧은 메모를 바탕으로, 국민건강보험공단 장기요양급여 제공기록지에 
                바로 복사해서 붙여넣을 수 있도록 '풍부하고 전문적인 서술형 리포트'로 작성하는 거야.
                
                [작성 규칙]
                1. 단순 1:1 단어 변환을 넘어, 요양기관에서 실제로 쓰는 자연스러운 서술형 문장으로 살을 붙여서 작성할 것.
                2. '드심' -> '섭취함', '주무심' -> '수면을 취함' 등 요양기관 공식 용어를 반드시 사용할 것.
                3. 사용자가 입력하지 않은 심각한 질병(치매 발작, 응급실 이송 등)을 지어내서는 안 되지만, 문맥을 부드럽게 만들기 위한 일상적인 요양 묘사는 추가해도 좋음.
                4. 결과물은 반드시 아래의 [출력 포맷] 양식을 지켜서 세련되게 정리해 줄 것.
                
                [출력 포맷]
                ■ 일일 상태 관찰 기록
                - 신체 및 건강 상태: (기침, 수면 등 신체 관련 입력 내용을 바탕으로 전문적으로 서술)
                - 식사 및 영양 상태: (식사량 등 영양 관련 내용을 바탕으로 서술)
                - 활동 및 프로그램: (운동, 프로그램 참여 등 활동 관련 내용을 바탕으로 서술)
                - 종합 관찰 소견: (위 내용을 종합하여 요양 전문가의 시선으로 한 줄 요약)
                """
            
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
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
                st.error(f"에러발생, 센터장에게 문의해주세요. 상세 에러 로그: {e}")

               



