# Naver Crawler

네이버 검색, 블로그, 플레이스 정보를 수집하는 크롤러 프로젝트입니다.

## 기능

### API 크롤러 (`api_crawler.py`)

- 네이버 검색 API를 사용한 블로그 URL 수집
- 블로그 포스트 내용 및 이미지 추출
- 네이버 플레이스 정보 수집 (카테고리, 전화번호, 리뷰 등)

### 셀레니움 크롤러 (`selenium_crawler.py`)

- 네이버 플레이스 URL 및 코드 수집
- 방문자 리뷰 텍스트 수집
- 블로그 리뷰 링크 수집
- 가게 상세 정보 크롤링 (영업시간, 메뉴, 주소 등)
- 텍스트 전처리 기능 (특수문자 제거, 띄어쓰기 보정)

## 설치 및 설정

### 필요 패키지 설치

```bash
pip install pandas numpy requests beautifulsoup4 selenium python-dotenv pykospacing openpyxl
```

### 환경 설정

1. `.env` 파일을 생성하고 네이버 API 키 설정

```
NAVER_CLIENT_ID_1=your_client_id_1
NAVER_CLIENT_SECRET_1=your_client_secret_1
NAVER_CLIENT_ID_2=your_client_id_2
NAVER_CLIENT_SECRET_2=your_client_secret_2
# 필요에 따라 추가 (최대 8개)
```

2. 셀레니움 사용을 위한 웹드라이버 설치 (Chrome 권장)

## 사용 방법

### API 크롤러 사용

```python
from api_crawler import NaverCrawler

# 크롤러 인스턴스 생성
crawler = NaverCrawler()

# 블로그 URL 가져오기
blog_urls, total_count = crawler.get_BlogURL("검색어", 10)  # 10개 URL 가져오기

# 블로그 내용 가져오기
content, images = crawler.get_BlogInfo(blog_urls[0], img=True)

# 네이버 플레이스 정보 가져오기
place_info = crawler.get_NaverPlace("서울 강남구", "맛집")
```

### 셀레니움 크롤러 사용

```python
from selenium_crawler import NaverPlaceUrlCollecter, NaverPlaceReviewCollector, DataPreprocessing
import pandas as pd

# 데이터프레임 생성
df = pd.DataFrame({'name': ['맛집1', '맛집2'], 'naverURL': ['', ''], 'naverCode': ['', ''], 'naverBlogURL': ['', '']})

# URL 수집
df = NaverPlaceUrlCollecter.UrlCollector(df)
df = NaverPlaceUrlCollecter.NaverCodeMaker(df)
df = NaverPlaceUrlCollecter.ReviewUrlMaker(df)

# 리뷰 수집
reviews = NaverPlaceReviewCollector.NaverPlaceReviewCollector(df)
blog_reviews = NaverPlaceReviewCollector.BlogReviewUrlCollector(df)

# 데이터 전처리
processed_reviews = DataPreprocessing.Preprocessing(reviews)
```

## 주의사항

- 네이버의 로봇 정책을 준수하고 과도한 요청을 피하세요
- API 호출 및 웹 스크래핑 시 적절한 시간 간격을 두세요
- 크롤링한 데이터는 저작권 및 개인정보 보호법을 준수하여 사용하세요

## 이 파일은 프로젝트 내 개인에게 할당된 파트만 분류하여 작성한 파일입니다.
