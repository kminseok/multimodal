import os
import shutil
import subprocess
from pathlib import Path


# ============================================================
# 설정
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# 입력
IMAGE_PATH = PROJECT_ROOT / "assets" / "anchor.png"
AUDIO_PATH = PROJECT_ROOT / "news_audio.mp3"

# MuseTalk
MUSETALK_DIR = PROJECT_ROOT / "MuseTalk"

# 임시 설정 파일
CONFIG_PATH = MUSETALK_DIR / "configs" / "inference" / "mvp_test.yaml"

# 결과
RESULT_DIR = MUSETALK_DIR / "results" / "mvp"

# 최종 영상
OUTPUT_PATH = PROJECT_ROOT / "news_anchor.mp4"


# ============================================================
# 입력 파일 확인
# ============================================================

def check_input_files():

    if not IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"앵커 이미지를 찾을 수 없습니다:\n{IMAGE_PATH}"
        )

    if not AUDIO_PATH.exists():
        raise FileNotFoundError(
            f"뉴스 음성을 찾을 수 없습니다:\n{AUDIO_PATH}"
        )

    if not MUSETALK_DIR.exists():
        raise FileNotFoundError(
            f"MuseTalk 폴더를 찾을 수 없습니다:\n{MUSETALK_DIR}"
        )


# ============================================================
# MuseTalk용 임시 YAML 생성
# ============================================================

def create_config():

    CONFIG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # MuseTalk은 상대 경로를 사용하므로
    # 프로젝트 기준 경로를 상대 경로로 변환한다.
    image_relative = os.path.relpath(
        IMAGE_PATH,
        MUSETALK_DIR
    )

    audio_relative = os.path.relpath(
        AUDIO_PATH,
        MUSETALK_DIR
    )

    config_text = f"""task_0:
 video_path: "{image_relative}"
 audio_path: "{audio_relative}"
 bbox_shift: 0
"""

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(config_text)

    print("\n[1/3] MuseTalk 설정 파일 생성")
    print(f"      image : {image_relative}")
    print(f"      audio : {audio_relative}")


# ============================================================
# MuseTalk 실행
# ============================================================

def run_musetalk():

    RESULT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n[2/3] MuseTalk 1.5 실행")
    print("      앵커 이미지 + 뉴스 음성을 영상으로 변환합니다.")
    print("      시간이 조금 걸릴 수 있습니다.\n")

    command = [
        "/home/ubuntu/miniforge3/envs/step4/bin/python",
        "-m",
        "scripts.inference",

        "--inference_config",
        str(CONFIG_PATH),

        "--result_dir",
        str(RESULT_DIR),

        "--unet_model_path",
        "./models/musetalkV15/unet.pth",

        "--unet_config",
        "./models/musetalkV15/musetalk.json",

        "--version",
        "v15",
    ]

    subprocess.run(
        command,
        cwd=MUSETALK_DIR,
        check=True
    )


# ============================================================
# 결과 영상 찾기
# ============================================================

def find_result_video():

    mp4_files = list(
        RESULT_DIR.rglob("*.mp4")
    )

    if not mp4_files:
        raise FileNotFoundError(
            f"MuseTalk 결과 영상을 찾을 수 없습니다:\n{RESULT_DIR}"
        )

    # 가장 최근에 생성된 파일
    result = max(
        mp4_files,
        key=lambda p: p.stat().st_mtime
    )

    return result


# ============================================================
# 최종 결과 복사
# ============================================================

def save_output():

    result_video = find_result_video()

    print("\n[3/3] 최종 영상 저장")

    shutil.copy2(
        result_video,
        OUTPUT_PATH
    )

    print(f"\n완료!")
    print(f"영상: {OUTPUT_PATH}")


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("       NEWS ANCHOR VIDEO GENERATOR")
    print("=" * 60)

    check_input_files()

    create_config()

    run_musetalk()

    save_output()

    print("=" * 60)


if __name__ == "__main__":
    main()