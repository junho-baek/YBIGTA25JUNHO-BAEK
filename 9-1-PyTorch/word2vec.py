import torch
from torch import nn, Tensor, LongTensor
from torch.optim import Adam
from transformers import PreTrainedTokenizer
from typing import Literal, List

class Word2Vec(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        window_size: int,
        method: Literal["cbow", "skipgram"]
    ) -> None:
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, d_model)  # 단어 임베딩 레이어
        self.weight = nn.Linear(d_model, vocab_size, bias=False)  # 출력 레이어
        self.window_size = window_size  # 문맥 윈도우 크기
        self.method = method  # 학습 방법 (cbow 또는 skipgram)

        # 가중치 초기화
        nn.init.xavier_uniform_(self.embeddings.weight)  # Xavier 초기화
        nn.init.xavier_uniform_(self.weight.weight)  # Xavier 초기화

    def embeddings_weight(self) -> Tensor:
        return self.embeddings.weight.detach()  # 임베딩 가중치를 반환

    def fit(
        self,
        corpus: list[str],
        tokenizer: PreTrainedTokenizer,
        lr: float,
        num_epochs: int
    ) -> None:
        criterion = nn.CrossEntropyLoss()  # 손실 함수 설정
        optimizer = Adam(self.parameters(), lr=lr)  # 옵티마이저 설정
        
        # 말뭉치를 토큰화
        tokenized_corpus = [tokenizer.encode(sentence, add_special_tokens=True) for sentence in corpus]

        for epoch in range(num_epochs):
            total_loss = 0
            # 말뭉치의 각 문장을 처리
            for sentence in tokenized_corpus:
                # 문장의 각 단어를 처리
                for i, target_word in enumerate(sentence):
                    # 문맥 단어의 인덱스를 생성
                    context_indices = (
                        list(range(max(0, i - self.window_size), i)) +
                        list(range(i + 1, min(len(sentence), i + self.window_size + 1)))
                    )
                    # 문맥 단어들을 추출
                    context_words = [sentence[idx] for idx in context_indices]

                    # CBOW 방식 학습
                    if self.method == "cbow":
                        # 문맥 단어들을 텐서로 변환
                        context_tensor = torch.tensor(context_words, dtype=torch.long).to(self.embeddings.weight.device)
                        # 타겟 단어를 텐서로 변환
                        target_tensor = torch.tensor(target_word, dtype=torch.long).to(self.embeddings.weight.device)
                        # 손실 계산 및 가중치 업데이트
                        loss = self._train_cbow(context_tensor, target_tensor, criterion, optimizer)
                    # Skip-gram 방식 학습
                    else:
                        # 문맥 단어들을 텐서로 변환
                        context_tensor = torch.tensor(context_words, dtype=torch.long).to(self.embeddings.weight.device)
                        # 타겟 단어를 텐서로 변환
                        target_tensor = torch.tensor(target_word, dtype=torch.long).to(self.embeddings.weight.device)
                        # 각 문맥 단어에 대해 타겟 단어를 예측하도록 설정
                        for context_word in context_tensor:
                            loss = self._train_skipgram(context_word.view(1), target_tensor, criterion, optimizer)
                            total_loss += loss.item()
                        continue
                    
                    # 총 손실을 업데이트
                    total_loss += loss.item()

            # 에포크별 손실 출력
            print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss:.4f}")

    def _train_cbow(
        self,
        context: LongTensor,
        target: LongTensor,
        criterion: nn.CrossEntropyLoss,
        optimizer: Adam
    ) -> Tensor:
        optimizer.zero_grad()  # 기울기 초기화
        context_embeddings = self.embeddings(context)  # 문맥 단어 임베딩
        context_mean = context_embeddings.mean(dim=0).view(1, -1)  # 문맥 단어 임베딩 평균 계산
        output = self.weight(context_mean)  # 출력 레이어 통과
        loss = criterion(output, target.view(-1))  # 손실 계산
        loss.backward()  # 역전파
        optimizer.step()  # 가중치 업데이트
        return loss

    def _train_skipgram(
        self,
        context: LongTensor,
        target: LongTensor,
        criterion: nn.CrossEntropyLoss,
        optimizer: Adam
    ) -> Tensor:
        optimizer.zero_grad()  # 기울기 초기화
        context_embedding = self.embeddings(context)  # 문맥 단어 임베딩
        output = self.weight(context_embedding)  # 출력 레이어 통과
        loss = criterion(output, target.view(-1))  # 손실 계산
        loss.backward()  # 역전파
        optimizer.step()  # 가중치 업데이트
        return loss

    # 추가 메소드 구현
    def save_model(self, path: str) -> None:
        """모델 가중치를 파일에 저장하는 메소드"""
        torch.save(self.state_dict(), path)

    def load_model(self, path: str) -> None:
        """파일에서 모델 가중치를 불러오는 메소드"""
        self.load_state_dict(torch.load(path))