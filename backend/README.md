## todo

- [X] DB 설계
- [X] endpoint (/login , /register , /)
- [X] 프로필 이미지 업데이트 메소드 만들기.
- [ ] git action
- [ ] 업적 - (가입하고 첫 문제 풀이 ..등등)
- [ ] llm 결과 로딩 시간 (프로그레스바?)
- [ ] gpt-4o 업데이트
## 질문
- 하루에 한번만 할 수 있게 하는가.
- DB 저장 어떻게 ?
- 1주일 단위로 결과 점수 보여줄건가. 최근 1주일 기록을 남겨 원할 때 피드백도 볼수 있게 할것인가. 
- 주제를 본인이 선택 or 모든 사용자가 공통 문서(주제 랜덤)
- jwt 할건지?


## 고쳐야 되는 것
- 문서는 길어지는데 요약이 너무 짧음 수정 필요..
- 로컬 이미지 업로드 기능 만들어야함 지금은 웹에 올라가있는 url만 됨
- 문서 url이 해당 기사가 아닌 해당 기사가 포함된 기사 리스트 url임 수정 필요
- 현재는 크롤링한 문서중 조건을 만족하는 첫번째 기사를 가져옴 ,, 같은 문서가 있으면 크롤링한 문서중 다음 문서를 저장하도록 로직 수정
- history 불러올 때 날짜 오름차순으로 정렬해서 보내줘야 할듯 
- 자정에 크롤링 할때 날짜가 어제 날짜로 되는 경우가 있음 확인 해보셈
- 난이도 책정 (ex 몇글자 이상이면 .. 어려움.. 쉬우...)
- crud 124번째 줄 처음 들어온거 로직 추가
- 통신 에러 코드 수정.. 전부 400으로 되어있음
- teasdas

python = "^3.10"
fastapi = "^0.110.2"
uvicorn = "^0.29.0"
langchain = "^0.1.16"
langchain-community = "^0.0.34"
langchain-openai = "^0.1.3"
langchain-core = "^0.1.45"
loguru = "^0.7.2"
python-dotenv = "^1.0.1"
bs4 = "^0.0.2"
sqlalchemy = "^2.0.29"
psycopg2 = "^2.9.9"
passlib = "^1.7.4"
bcrypt = "^4.1.2"
apscheduler = "^3.10.4"
beautifulsoup4 = "^4.12.3"
requests = "^2.31.0"
pre-commit = "^3.7.1"
black = "^24.4.2"
pytest = "^8.2.1"
