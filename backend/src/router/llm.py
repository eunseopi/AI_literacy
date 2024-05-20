from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from langchain.agents import AgentExecutor, create_react_agent, Tool, load_tools,create_tool_calling_agent
from langchain_core.output_parsers import StrOutputParser
import os
import uvicorn
from dotenv import load_dotenv
from langchain.tools import tool
from langchain import hub
from fastapi import FastAPI,APIRouter,Depends,HTTPException,BackgroundTasks
from src.models import models
from src.database import crud
from src.database.conn import get_db
from src.database import db_models
from sqlalchemy.orm import Session

from src.components import scheduler
from datetime import datetime,timedelta,timezone

scheduler

# test
    

# 네이버 뉴스기사 주소

"""summary_of_function
    1. 요약할 문서 제시
    2. 문서를 사용자가 요약
    3. 사용자의 입력을 gpt input에 넣고 gpt가 요약한 결과와 비교
    4. 점수나 결과를 반환
"""
KST = timezone(timedelta(hours=9))


# main 배포시 사용
env = os.getenv("ENV", "")
load_dotenv(f'.env{env}')

OPEN_AI_APIKEY = os.getenv("OPEN_AI_APIKEY")

# url = 'https://n.news.naver.com/article/437/0000361628?cds=news_media_pc'

# # 웹 문서 크롤링
# loader = WebBaseLoader(url)

# # 뉴스기사의 본문을 Chunk 단위로 쪼갬
# text_splitter = CharacterTextSplitter(        
#     separator="\n\n",
#     chunk_size=3000,     # 쪼개는 글자수
#     chunk_overlap=300,   # 오버랩 글자수
#     length_function=len,
#     is_separator_regex=False,
# )

# # 웹사이트 내용 크롤링 후 Chunk 단위로 분할
# docs = WebBaseLoader(url).load_and_split(text_splitter)


# # LLM 객체 생성
llm = ChatOpenAI(temperature=0, 
                 model_name='gpt-4-turbo',openai_api_key=OPEN_AI_APIKEY,verbose=True)

form = """{
    "llm_summary": ,
    "user_summary": ,
    "score": ,
    "comment": ,
}"""



template = """너는 평가 전문가야. 문제를 해결하기 위해 다음 단계를 수행합니다.
    - 먼저 원문에 대한 자신만의 요약을 합니다.
    - 그런 다음 자신의 요약을 사용자의 입력과 비교합니다.
이후 사용자의 요약이 얼마나 정확한지 1부터 10까지 점수로 평가합니다 .
사용자의 요약이 얼마나 정확한지 직접 요약하기 전에는 결정하지 마세요.

docs: {docs}
input: {input}
다음 형식에 맞춰 대답하세요.
{form}



"""
prompt_template = PromptTemplate(input_variables=["docs","input","form"], template=template)

output_parser = StrOutputParser()

review_chain = prompt_template | llm | output_parser




# result = review_chain.invoke({"docs":"나의 이름은 윤성훈이다. 나는 어렸을 때부터 게임하는 것을 좋아했다. 그러나 내 꿈은 프로그래머이다.","input":"윤성훈의 꿈은 프로그래머이다.","form":form})
# print(result)

# r = eval(result)
# print(r["점수"])

llm_router = APIRouter()


@llm_router.post("/literacy")
async def literacy_test(user_input:str,user_email:str,db: Session = Depends(get_db))->dict:
    """_summary_

    input:
    
        {
            # 사용자가 요약한 문장
            "user_input" : str,
            # 사용자의 이메일
            "user_email" : str 
        }

    Returns:
    
        {
            "llm_summary": str,
            "user_summary": str,
            "score": int, # 1~10
            "comment": str,
            "docurl": url ,
        }
    """
    
    content = crud.get_contents(db)[0].content
    
    
    if content is None:
        # raise HTTPException(status_code=400,detail="서버 오류 관리자에게 문의.")
        return {"message":"서버에서 데이터를 가져오는 중입니다. 새로고침을 해주세요!"}
    print("\nthis is the llm part !!!!!!!!!!!!!!!!!!!!!!!!!!!\n",content)

    played_dates = crud.get_scores_by_user(db, user_email)
    
    for i in range(len(played_dates)):
        played_dates[i] = played_dates[i].played_date
    played_dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    
    if datetime.now(KST).date().strftime("%Y-%m-%d") == played_dates[-1]:
        raise HTTPException(status_code=400,detail="하루에 한번만 가능합니다.")
        
    
    #! 사용자가 선택한 웹 문서 주소를 바탕으로 크롤링 
    #! 다음은 문서 예시
    
    # docs = "나의 이름은 윤성훈이다. 나는 어렸을 때부터 게임하는 것을 좋아했다. 그러나 내 꿈은 프로그래머이다."
    result = review_chain.invoke({"docs":content,"input":user_input,"form":form})
    # print("this is the llm's answer",result)   
    
    result = eval(result)
    print("this is the result: ",result)
    #! 해당 글에 대한 docurl 수정필요 지금은 리스트 페이지로 이동
    result["docurl"] = "https://news.sbs.co.kr/news/newsPlusList.do?themeId=10000000134&plink=SITEMAP&cooper=SBSNEWS"
    
    # print("LLM 요약: ",result["원문 요약"])
    # print("사용자의 요약: ",result["사용자의 요약"])
    # print("비교 평가: ",result["평가"])
    # print("점수: ",result["점수"]," 점")
    # print("총평: ",result["총평"])

    #! 결과를 DB에 저장하는 코드 추가
    try:
        score = crud.save_score(db, models.ScoreCreate(**result),user_email)
        crud.increase_continuous_days(db, user_email)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400,detail="하루에 한번 가능합니다.")
    
    return result
    # overall_chain.run(docs=docs, input=user_input)
    
    # 요약 문 입력(user_input) -> 원문에 대한 llm 요약 결과 -> 두개 요약본을 가지고 평가
    # 원문과 사용자 요약을 같이 받나?
    

@llm_router.get("/get_contents")
async def get_contents(db: Session = Depends(get_db)):
    """_summary_
    
    Returns:
        
        {
            "content": str
        }
    """
    content = crud.get_contents(db)
    return {"content":content[0].content}
    

