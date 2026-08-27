import asyncio
import edge_tts


# ============================================================
# 설정
# ============================================================

VOICE = "ko-KR-HyunsuNeural"
OUTPUT_FILE = "news_audio.mp3"


# ============================================================
# TTS 생성 함수
# ============================================================

async def generate_tts(text, output_file=OUTPUT_FILE):
    """
    뉴스 대본을 Edge TTS를 이용해 음성 파일로 변환한다.

    Args:
        text (str):
            TTS로 변환할 뉴스 아나운서 대본

        output_file (str):
            생성할 음성 파일 경로
    """

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(output_file)

    return output_file


# ============================================================
# 동기 방식으로 사용할 수 있는 wrapper
# ============================================================

def create_audio(text, output_file=OUTPUT_FILE):
    """
    일반 Python 코드에서 쉽게 사용할 수 있도록
    asyncio를 내부에서 처리한다.
    """

    return asyncio.run(
        generate_tts(
            text=text,
            output_file=output_file
        )
    )