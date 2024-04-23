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
from fastapi import FastAPI


# 네이버 뉴스기사 주소

"""summary_of_function
    1. 요약할 문서 제시
    2. 문서를 사용자가 요약
    3. 사용자의 입력을 gpt input에 넣고 gpt가 요약한 결과와 비교
    4. 점수나 결과를 반환
"""


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
    "원문 요약": ,
    "사용자의 요약": ,
    "평가": ,
    "점수": ,
    "총평": ,
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

app = FastAPI()

@app.post("/literacy_test")
async def literacy_test(doc_url:str,user_input:str)->dict:
    
    #! 사용자가 선택한 웹 문서 주소를 바탕으로 크롤링 
    #! 다음은 문서 예시
    docs = "나의 이름은 윤성훈이다. 나는 어렸을 때부터 게임하는 것을 좋아했다. 그러나 내 꿈은 프로그래머이다."
    result = review_chain.invoke({"docs":docs,"input":"윤성훈은 게임하는 것을 좋아했다.","form":form})
    print("this is the llm's answer",result)   
    
    result = eval(result)
    
    
    print("LLM 요약: ",result["원문 요약"])
    print("사용자의 요약: ",result["사용자의 요약"])
    print("비교 평가: ",result["평가"])
    print("점수: ",result["점수"]," 점")
    print("총평: ",result["총평"])
    
    
    return result
    # overall_chain.run(docs=docs, input=user_input)
    
    # 요약 문 입력(user_input) -> 원문에 대한 llm 요약 결과 -> 두개 요약본을 가지고 평가
    # 원문과 사용자 요약을 같이 받나?
    
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
