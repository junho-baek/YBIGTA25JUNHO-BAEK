from datasets import load_dataset

def load_corpus() -> list[str]:
    corpus: list[str] = []
    # Hugging Face의 datasets 라이브러리에서 poem_sentiment 데이터셋을 로드합니다.
    dataset = load_dataset('google-research-datasets/poem_sentiment')
    
    # 데이터셋의 구조를 확인하기 위해 예제 하나를 출력합니다.
    print(dataset['train'][0])  # 데이터셋 예제 출력

    # train, validation, test 데이터셋의 텍스트를 모두 corpus에 추가합니다.
    for split in ['train', 'validation', 'test']:
        for example in dataset[split]:
            corpus.append(example['verse_text'])  # 'verse_text' 키를 사용하여 텍스트 데이터 가져오기
    
    return corpus

