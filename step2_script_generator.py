import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from step3_tts import create_audio

from step1_news_scraper import get_news_article


# ============================================================
# 1. 모델 설정
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"


# ============================================================
# 2. 모델 로드
# ============================================================

print("Qwen 모델을 불러오는 중...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)

print("모델 로드 완료!")


# ============================================================
# 3. 아나운서 대본 생성
# ============================================================

def generate_script(title, article):
    """
    뉴스 기사 제목과 본문을 받아
    TV 뉴스 아나운서용 대본을 생성한다.
    """

    prompt = f"""
당신은 전문적인 한국어 뉴스 아나운서입니다.

다음 뉴스 기사를 바탕으로 TV 뉴스에서 실제 아나운서가
읽을 수 있는 자연스러운 뉴스 대본을 작성하세요.

[작성 규칙]

1. 기사에 명시된 사실만 사용하세요.
2. 기사에 없는 사실을 임의로 추가하지 마세요.
3. 핵심 내용을 중심으로 간결하게 작성하세요.
4. 문어체 기사 문장을 자연스러운 구어체 뉴스 진행 문장으로 바꾸세요.
5. 아나운서가 실제로 읽었을 때 자연스럽게 들리도록 작성하세요.
6. 숫자, 날짜, 기관명, 인명 등 중요한 정보는 정확하게 유지하세요.
7. 개인적인 의견이나 감정을 추가하지 마세요.
8. "안녕하세요", "지금까지 ○○였습니다" 등의 인사말과 맺음말은 작성하지 마세요.
9. TTS로 읽을 예정이므로 특수문자, 이모지, 마크다운을 사용하지 마세요.
10. 약 40~60초 정도 분량의 대본으로 작성하세요.

[기사 제목]
{title}

[기사 본문]
{article}

위 기사를 바탕으로 최종 뉴스 아나운서 대본만 작성하세요.
"""

    messages = [
        {
            "role": "system",
            "content": "당신은 정확하고 전문적인 한국어 뉴스 아나운서입니다."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer(
        [text],
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    # 입력 prompt 부분 제거
    generated_ids = generated_ids[:, model_inputs.input_ids.shape[1]:]

    script = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return script.strip()


# ============================================================
# 4. 실행
# ============================================================

if __name__ == "__main__":

    url = input("뉴스 기사 URL을 입력하세요: ").strip()

    try:

        print("\n[1/2] 뉴스 기사 추출 중...")

        title, article = get_news_article(url)

        print("\n기사 제목:")
        print(title)

        print("\n[2/2] Qwen으로 아나운서 대본 생성 중...")

        script = generate_script(
            title,
            article
        )

        print("\n" + "=" * 60)
        print("아나운서 대본")
        print("=" * 60)

        print(script)
        print("\n[3/3] Edge TTS로 음성 생성 중...")

        audio_file = create_audio(
            text=script,
            output_file="news_audio.mp3"
        )

        print(f"음성 생성 완료!")
        print(f"저장 위치: {audio_file}")

    except Exception as e:

        print("\n대본 생성 실패:")
        print(e)