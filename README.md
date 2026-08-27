# AI News Anchor

뉴스 기사 URL을 입력하면 기사 내용을 분석하여 아나운서 대본, 음성, AI 앵커 영상을 자동으로 생성하는 멀티모달 AI 미니 프로젝트입니다.

## Task

뉴스 기사 URL 하나를 입력받아 다음 과정을 자동으로 수행합니다.

**뉴스 기사 → 대본 생성 → 음성 생성 → AI 앵커 영상 생성**

## Pipeline

### Step 1. News Scraping

뉴스 URL에서 기사 제목과 본문을 크롤링합니다.

- **Requests**: 웹 페이지 요청
- **BeautifulSoup**: 기사 제목 추출
- **Trafilatura**: 광고나 메뉴 등의 불필요한 내용을 제외하고 기사 본문 추출

### Step 2. Script Generation

추출한 기사를 바탕으로 실제 뉴스 아나운서가 읽을 수 있는 대본을 생성합니다.

- **Qwen2.5-3B-Instruct**
- Instruction Following 으로 기사 내용을 뉴스 대본 형태로 변환
- 비교적 작은 3B 모델로 T4 GPU 환경에서 실행하기 적합

### Step 3. TTS

생성된 아나운서 대본을 음성으로 변환합니다.

- **Edge TTS**
- 한국어 Neural Voice를 지원하며 별도의 TTS 모델 학습 없이 상대적으로 빠르게 자연스러운 음성을 생성할 수 있어 사용

### Step 4. AI Anchor Video

앵커 이미지와 생성된 음성을 이용하여 AI 앵커 영상을 생성합니다.

- **MuseTalk 1.5**
- 음성에 맞춰 얼굴과 입술 움직임을 생성하는 Talking Head 모델
- Anchor Image + Audio를 결합하여 뉴스 앵커 영상 생성

## Dashboard
gradio link: https://dbfa1fef5261d70a12.gradio.live
