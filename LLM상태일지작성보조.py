
import streamlit as st
import google.generativeai as genai 

st.set_page_config(page_title="어르신 관찰일지 & 알림톡 봇", page_icon="📝", layout="centered")

st.title("어르신 관찰일지 & 알림톡 자동 요약")
st.markdown("단어 몇 개만 툭툭 적어주세요. 공단 제출용과 보호자님꼐 보낼 알림톡으로 자동으로 바꿔 써 드립니다.")

# 사용자가 입력하는 창
user_input = st.text_area(
    label="오늘 어르신의 상태를 간단히 적어주세요", 
    placeholder="예: 오늘 점심 반 공기 드심. 기침 3번 하심. 운동 30분 함(신체상태, 정신상태 꼭 기재、!!!어르신 실명 절대 적지 말것!!!)",
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
                    너는 국민건강보험공단 규정을 엄격히 준수하는 '방문요양 관찰일지 문체 교정 보조 AI'야.
                    너의 유일한 목적은 요양보호사가 입력한 파편화된 단어나 짧은 문장을 '공단 제출용 공식 문어체(객관적, 3인칭 관찰자 시점)'로 변환하는 것뿐이야.

                    아래의 [작성 규칙]을 반드시 지켜서 응답해.
                    
                    [작성 규칙]
                    1. 사실 창조 금지 (Zero Hallucination): 사용자가 입력한 단어와 사실 외에는 절대 어떤 증상, 식사량, 배변 상태, 기분, 처치 내용도 임의로 덧붙이거나 지어내지 마라. (위반 시 법적 허위 기록에 해당함)
                    2. 객관적 문체 사용: 감정적인 표현은 배제하고, "~하심", "~관찰됨", "~호소하심", "~도움을 제공함" 등 요양 실무 표준 용어와 건조한 문어체로만 작성하라.
                    3. 정보 부족 시 거절: 사용자의 입력이 너무 짧거나 사실관계를 알 수 없는 경우(예: "오늘 좋았음"), 문장을 지어내지 말고 "어르신의 식사량, 인지 상태, 신체 상태 등에 대한 구체적인 단어를 더 입력해 주세요."라고 정중히 요청하라.
                       익명성 유지: 특정 어르신의 이름이 입력되더라도 출력할 때는 항상 "수급자 어르신" 또는 "어르신"으로 대체하여 개인정보를 보호하라.
                    
                    [출력 포맷]
                    ■ 일일 상태 관찰 기록
                    [출력 포맷]
                    1. 식사 및 영양: (입력된 식사 관련 내용)
                    2. 신체 및 수면: (입력된 수면, 기침 등 신체 상태)
                    3. 활동 및 특이사항: (기타 활동이나 특이사항 간략히, 없으면 '특이사항 없음' 처리)
                    4. 종합 관찰 소견: (위 내용을 종합하여 신체 상태, 정신상태 포함해 요양 전문가의 시선으로 한 줄 요약)
                    
                    [변환 예시]
                    사용자 입력: "점심에 밥 반공기 먹음. 기침 약간 함. 낮잠 1시간 잠."
                    출력: "중식 시 밥을 반 공기 정도 섭취하심. 일과 중 간헐적인 기침 증상이 관찰되어 수분 섭취를 돕고 상태를 관찰함. 식후 약 1시간가량 주간 수면을 취하심."
                    """
                    
                else: # btn_guardian이 눌렸을 경우
                    system_prompt = """
                    너는 노인장기요양기관에서 근무하는 친절하고 따뜻한 사회복지사야. 
                    입력된 관찰 메모를 바탕으로, 자녀분들이 부모님 걱정을 덜고 안심할 수 있도록 다정하고 예의 바른 카카오톡 메시지 톤으로 변환해 줘.
                    
                    [작성 규칙]
                    1. 보호자(자녀)에게 보내는 다정하고 예의 바른 존댓말(~해요, ~습니다, ~했어요)을 사용할 것.
                    2. 어르신이 센터에서 편안하고 즐겁게 지내고 계심이 잘 느껴지도록 긍정적이고 안심을 주는 톤을 유지할 것. 단、 날조는 절대 하지 말 것。
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












