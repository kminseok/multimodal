import subprocess
import sys
from pathlib import Path

from step1_news_scraper import get_news_article
from step2_script_generator import generate_script
from step3_tts import create_audio


# ============================================================
# 경로 설정
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

STEP4_PYTHON = "/home/ubuntu/miniforge3/envs/step4/bin/python"
STEP4_SCRIPT = PROJECT_ROOT / "step4_video_generator.py"

AUDIO_FILE = PROJECT_ROOT / "news_audio.mp3"
VIDEO_FILE = PROJECT_ROOT / "news_anchor.mp4"


# ============================================================
# STEP 4 실행
# ============================================================

def run_step4():
    """
    step4 가상환경에서 MuseTalk 영상 생성
    """

    print("\n" + "=" * 60)
    print("[STEP 4/4] MuseTalk으로 앵커 영상 생성")
    print("=" * 60)

    result = subprocess.run(
        [
            STEP4_PYTHON,
            str(STEP4_SCRIPT)
        ],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(
            "STEP 4 실행에 실패했습니다."
        )


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("\n" + "=" * 60)
    print("          AI NEWS ANCHOR")
    print("=" * 60)

    # --------------------------------------------------------
    # URL 입력
    # --------------------------------------------------------

    url = input("\n뉴스 기사 URL을 입력하세요: ").strip()

    if not url:
        print("URL이 입력되지 않았습니다.")
        return

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("[STEP 1/4] 뉴스 기사 추출")
    print("=" * 60)

    title, article = get_news_article(url)

    print("\n기사 제목:")
    print(title)

    print("\n기사 본문:")
    print(article[:1000])

    if len(article) > 1000:
        print("\n... (본문 일부만 표시)")


    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("[STEP 2/4] Qwen으로 아나운서 대본 생성")
    print("=" * 60)

    script = generate_script(
        title,
        article
    )

    print("\n아나운서 대본:")
    print("-" * 60)
    print(script)
    print("-" * 60)


    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("[STEP 3/4] Edge TTS 음성 생성")
    print("=" * 60)

    audio_file = create_audio(
        text=script,
        output_file=str(AUDIO_FILE)
    )

    print(f"\n음성 생성 완료!")
    print(f"저장 위치: {audio_file}")


    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    run_step4()


    # --------------------------------------------------------
    # 최종 결과
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    if VIDEO_FILE.exists():

        print("🎉 AI 뉴스 앵커 영상 생성 완료!")
        print()
        print(f"최종 영상:")
        print(VIDEO_FILE)

    else:

        print("⚠ 영상 파일을 찾지 못했습니다.")
        print(f"예상 위치: {VIDEO_FILE}")

    print("=" * 60)


# ============================================================
# 실행
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\n\n작업이 취소되었습니다.")

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ 오류 발생")
        print("=" * 60)
        print(e)