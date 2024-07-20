from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARTICLES = [
    "0번째 글: 블로그를 시작했다! FastAPI를 사용해서 직접 만들고 배포했다. 앞으로가 정말 기대된다. 조회수가 늘면 광고도 달아야지 히힛.",
    "1번째 글: 아침에 시리얼을 먹다가 우유를 쏟아서 주방이 엉망이 됐다. 슬프지만 어쩔 수 없지. 흑흑. 그래도 내 소중한 오레오 오즈는 쏟지 않아서 정말 다행이야.",
    "2번째 글: 큰일이다. 지난주에 GitHub에 올린 소스에 AWS 키가 포함되어 있었던 모양이다. 얼리버드 기상을 하고 보니 AWS에서 4580283940200달러가 청구되었다는 메일이 왔다. 이거 어떻게 환불 안 되려나. 진짜 큰일났다.",
    "3번째 글: 결국 환불에 실패했다. 제프 베조스가 너구리 암살단을 풀어 나를 쫓고 있다. 이런 글 쓸 시간도 없지만... 도피용 열차에 탑승하기 전 나의 흔적을 남겨본다.",
    "4번째 글: 마침내 그들이 도착했다. 세상과 작별할 시간이다..."
]

@app.get("/api/articles/{article_id}")
def read_article(article_id: int):
    print(f"new request!: {article_id}")
    return {"article": ARTICLES[article_id]}