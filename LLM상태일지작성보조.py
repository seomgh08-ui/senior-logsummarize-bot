
import streamlit as st
import google.generativeai as genai 

st.set_page_config(page_title="어르신 관찰일지 & 알림톡 봇", page_icon="📝", layout="centered")

st.title("어르신 관찰일지 & 알림톡 자동 요약")
st.markdown("단어 몇 개만 툭툭 적어주세요. 공단 제출용과 보호자님꼐 보낼 알림톡으로 자동으로 바꿔 써 드립니다.")

# 사용자가 입력하는 창
user_input = st.text_area(
    label="오늘 어르신의 상태를 간단히 적어주세요", 
    placeholder="예: 오늘 김할머니 점심 반 공기 드심. 기침 3번 하심. 운동 30분 함(신체상태, 정신상태 꼭 기재!)",
    height=150
)

# ★ 수정된 부분: 버튼을 2개로 나누어 나란히 배치합니다.
col1, col2 = st.columns(2)
btn_official = col1.button("공단 제출용 생성", use_container_width=True)
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
                    너는 노인장기요양기관의 요양보호사야.
                    사용자가 어르신의 오늘 상태 메모를 입력하면, 국민건강보험공단 제공기록지에 빠르고 간편하게 옮겨 적을 수 있도록 '핵심만 딱 3줄'로 요약해 줘.
                    
                    [작성 규칙]
                    1. 분량 엄수: 장황한 설명은 모두 빼고, 반드시 핵심 내용만 담아 '딱 4줄'로 출력할 것.
                    2. 간결한 말투: 지나치게 전문적인 단어보다는 현장에서 쓰는 깔끔한 서술형(~함, ~임)을 사용할 것. (예: '드심' -> '섭취함', '주무심' -> '수면을 취함')
                    3. 팩트 중심: 사용자가 입력한 내용(식사, 수면, 활동 등)은 꼭 포함, 구체적으로 적지 못한 내용에 한해서는 내용을 더 만들어 꾸며도 됨, 단 맥락을 과하게 벗어나는 내용으로 날조하지 말것.
                    
                    [출력 포맷]
                    ■ 일일 상태 관찰 기록
                    [출력 포맷]
                    1. 식사 및 영양: (입력된 식사 관련 내용)
                    2. 신체 및 수면: (입력된 수면, 기침 등 신체 상태)
                    3. 활동 및 특이사항: (기타 활동이나 특이사항 간략히, 없으면 '특이사항 없음' 처리)
                    4. 종합 관찰 소견: (위 내용을 종합하여 신체 상태, 정신상태 포함해 요양 전문가의 시선으로 한 줄 요약)
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










