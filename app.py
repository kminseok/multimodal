import gradio as gr
import subprocess
from pathlib import Path

from step1_news_scraper import get_news_article
from step2_script_generator import generate_script
from step3_tts import create_audio


# ============================================================
# 경로 설정
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# STEP 4는 별도의 가상환경 사용
STEP4_PYTHON = "/home/ubuntu/miniforge3/envs/step4/bin/python"

STEP4_SCRIPT = PROJECT_ROOT / "step4_video_generator.py"

# 생성되는 파일
AUDIO_FILE = PROJECT_ROOT / "news_audio.mp3"
VIDEO_FILE = PROJECT_ROOT / "news_anchor.mp4"


# ============================================================
# STEP 4 실행
# ============================================================

def run_step4():
    """
    step4 가상환경의 Python을 이용해서
    MuseTalk 영상 생성을 실행한다.
    """

    result = subprocess.run(
        [
            STEP4_PYTHON,
            str(STEP4_SCRIPT)
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        error_message = result.stderr

        raise RuntimeError(
            "MuseTalk 실행 실패\n\n"
            + error_message
        )

    return result.stdout


# ============================================================
# 전체 뉴스 영상 생성 Pipeline
# ============================================================

def generate_news_video(url):
    """
    뉴스 URL 하나를 입력받아

    URL
     ↓
    기사 추출
     ↓
    Qwen 대본 생성
     ↓
    Edge TTS
     ↓
    MuseTalk
     ↓
    뉴스 앵커 영상

    전체 pipeline을 실행한다.
    """

    try:

        # ====================================================
        # 입력 확인
        # ====================================================

        if not url or not url.strip():

            raise ValueError(
                "뉴스 기사 URL을 입력해주세요."
            )

        url = url.strip()


        # ====================================================
        # STEP 1
        # ====================================================

        status = (
            "[STEP 1/4]\n"
            "뉴스 기사 본문을 추출하고 있습니다..."
        )

        yield (
            status,
            "",
            None,
            None
        )

        title, article = get_news_article(url)


        # ====================================================
        # STEP 2
        # ====================================================

        status = (
            "[STEP 1/4] 기사 추출 완료\n"
            f"기사 제목: {title}\n\n"
            "[STEP 2/4]\n"
            "Qwen으로 아나운서 대본을 생성하고 있습니다..."
        )

        yield (
            status,
            "",
            None,
            None
        )

        script = generate_script(
            title,
            article
        )


        # ====================================================
        # STEP 3
        # ====================================================

        status = (
            "[STEP 1/4] 기사 추출 완료\n"
            "[STEP 2/4] 아나운서 대본 생성 완료\n\n"
            "[STEP 3/4]\n"
            "Edge TTS로 뉴스 음성을 생성하고 있습니다..."
        )

        yield (
            status,
            script,
            None,
            None
        )

        create_audio(
            text=script,
            output_file=str(AUDIO_FILE)
        )


        # ====================================================
        # STEP 4
        # ====================================================

        status = (
            "[STEP 1/4] 기사 추출 완료\n"
            "[STEP 2/4] 아나운서 대본 생성 완료\n"
            "[STEP 3/4] TTS 음성 생성 완료\n\n"
            "[STEP 4/4]\n"
            "MuseTalk으로 뉴스 앵커 영상을 생성하고 있습니다...\n\n"
            "※ 영상 생성에는 시간이 걸릴 수 있습니다."
        )

        yield (
            status,
            script,
            str(AUDIO_FILE),
            None
        )

        run_step4()


        # ====================================================
        # 결과 확인
        # ====================================================

        if not VIDEO_FILE.exists():

            raise FileNotFoundError(
                "MuseTalk 실행은 완료되었지만 "
                "최종 영상 파일을 찾을 수 없습니다.\n\n"
                f"확인 경로:\n{VIDEO_FILE}"
            )


        # ====================================================
        # 완료
        # ====================================================

        status = (
            "[STEP 1/4] 기사 추출 완료 ✓\n"
            "[STEP 2/4] 아나운서 대본 생성 완료 ✓\n"
            "[STEP 3/4] TTS 음성 생성 완료 ✓\n"
            "[STEP 4/4] MuseTalk 영상 생성 완료 ✓\n\n"
            "🎉 뉴스 앵커 영상 생성 완료!"
        )

        yield (
            status,
            script,
            str(AUDIO_FILE),
            str(VIDEO_FILE)
        )


    # ========================================================
    # 오류 처리
    # ========================================================

    except Exception as e:

        yield (
            f"❌ 오류 발생\n\n{str(e)}",
            "",
            None,
            None
        )


# ============================================================
# Gradio UI
# ============================================================

with gr.Blocks(
    title="AI News Anchor"
) as app:


    # ========================================================
    # 제목
    # ========================================================

    gr.Markdown(
        """
        # 📰 AI News Anchor

        뉴스 기사 URL을 입력하면

        **기사 → 아나운서 대본 → 음성 → AI 앵커 영상**

        을 자동으로 생성합니다.
        """
    )


    # ========================================================
    # URL 입력
    # ========================================================

    url_input = gr.Textbox(
        label="뉴스 기사 URL",
        placeholder="https://news.example.com/article...",
        lines=1
    )


    # ========================================================
    # 생성 버튼
    # ========================================================

    generate_button = gr.Button(
        "🎬 뉴스 영상 생성",
        variant="primary"
    )


    # ========================================================
    # Pipeline 상태
    # ========================================================

    status_output = gr.Textbox(
        label="현재 상태",
        lines=8,
        interactive=False
    )


    # ========================================================
    # 아나운서 대본
    # ========================================================

    script_output = gr.Textbox(
        label="📝 아나운서 대본",
        lines=12,
        interactive=False
    )


    # ========================================================
    # TTS 음성
    # ========================================================

    audio_output = gr.Audio(
        label="🔊 뉴스 음성",
        type="filepath"
    )


    # ========================================================
    # 최종 영상
    # ========================================================

    video_output = gr.Video(
        label="🎥 뉴스 앵커 영상",
        width=600
    )


    # ========================================================
    # 버튼 이벤트
    # ========================================================

    generate_button.click(
        fn=generate_news_video,
        inputs=url_input,
        outputs=[
            status_output,
            script_output,
            audio_output,
            video_output
        ]
    )


# ============================================================
# 실행
# ============================================================

if __name__ == "__main__":

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )