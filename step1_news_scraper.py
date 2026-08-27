import requests
import trafilatura
from bs4 import BeautifulSoup


def get_news_article(url):
    """
    뉴스 URL에서 제목과 본문을 추출한다.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    }

    # --------------------------------------------------
    # 1. 웹 페이지 요청
    # --------------------------------------------------
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    html = response.text

    # --------------------------------------------------
    # 2. 제목 추출
    # --------------------------------------------------
    soup = BeautifulSoup(html, "lxml")

    title = soup.find("title")

    if title:
        title = title.get_text(strip=True)
    else:
        title = "제목을 찾을 수 없습니다."

    # --------------------------------------------------
    # 3. 기사 본문 추출
    # --------------------------------------------------
    article_text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        include_links=False,
        include_images=False
    )

    if not article_text:
        raise ValueError("기사 본문을 추출하지 못했습니다.")

    return title, article_text


if __name__ == "__main__":

    url = input("뉴스 기사 URL을 입력하세요: ").strip()

    try:

        title, article = get_news_article(url)

        print("\n" + "=" * 60)
        print("제목")
        print("=" * 60)
        print(title)

        print("\n" + "=" * 60)
        print("본문")
        print("=" * 60)
        print(article)

    except Exception as e:

        print(f"\n기사 추출 실패: {e}")