# 파일명: app.py

import streamlit as st
import google.generativeai as genai 

st.set_page_config(page_title="어르신 관찰일지 & 알림톡 봇", page_icon="📝", layout="centered")

st.title("📝 어르신 관찰일지 & 알림톡 자동 요약")
st.markdown("단어 몇 개만 툭툭 입력하세요. 공단 제출용 리포트와 보호자용 알림톡으로 자동 변환해 드립니다.")

# 사용자가 입력하는 창
user_input = st.text_area(
    label="오늘 어르신의 상태를 간단히 입력하세요", 
    placeholder="예: 오늘 김할머니 점심 반 공기 드심. 기침 3번 하심. 낮잠 1시간 주무심.",
    height=150
)

# ★ 수정된 부분: 버튼을 2개로 나누어 나란히 배치합니다.
col1, col2 = st.columns(2)
btn_official = col1.button("공단 제출용 리포트 생성", use_container_width=True)
btn_guardian = col2.button(" 보호자 전송용 알림톡 생성", use_container_width=True)

# 두 버튼 중 하나라도 눌렸을 때 실행됩니다.
if btn_official or btn_guardian:
    if user_input == "":
        st.warning(" 내용을 먼저 입력해 주세요!")
    else:
        with st.spinner("요청하신 양식으로 변환 중입니다... "):
            try:
                # ★ 핵심 보안 로직 (기존 코드 완벽 유지)
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                # ★ 눌린 버튼에 따라 프롬프트를 다르게 설정합니다.
                if btn_official:
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
                else: # btn_guardian이 눌렸을 경우
                    system_prompt = """
                    너는 노인장기요양기관에서 근무하는 친절하고 따뜻한 사회복지사야. 
                    입력된 관찰 메모를 바탕으로, 자녀분들이 부모님 걱정을 덜고 안심할 수 있도록 다정하고 예의 바른 카카오톡 메시지 톤으로 변환해 줘.
                    
                    [작성 규칙]
                    1. 보호자(자녀)에게 보내는 다정하고 예의 바른 존댓말(~해요, ~습니다, ~했어요)을 사용할 것.
                    2. 어르신이 센터에서 편안하고 즐겁게 지내고 계심이 잘 느껴지도록 긍정적이고 안심을 주는 톤을 유지할 것.
                    3. 딱딱한 전문 용어보다는 일상적이고 부드러운 표현을 사용할 것.
                    4. 문장 끝에 상황에 맞는 이모티콘(😊, 💕 등)을 자연스럽게 섞어서 친근함을 더해줄 것(3번이하사용).
                    """
                
                # ★ 기존 모델 생성 및 호출 로직 (기존 코드 완벽 유지)
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



