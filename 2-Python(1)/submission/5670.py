from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=list)
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        curr_node_idx = 0

        for char in seq:
            found = False
            for child_idx in self[curr_node_idx].children:
                if self[child_idx].body == char:
                    curr_node_idx = child_idx
                    found = True
                    break

            if not found:
                char_idx = len(self)
                self.append(TrieNode(body=char))
                self[curr_node_idx].children.append(char_idx)
                curr_node_idx = char_idx
        
        self[curr_node_idx].is_end = True

    def search(self, seq: Iterable[T]) -> bool:
        """
        trie에서 seq 찾기

        Args:
            seq (Iterable[T]): T의 열

        Returns:
            bool: seq의 존재 여부
        """
        current_node_idx = 0

        for char in seq:
            found = False
            for child_idx in self[current_node_idx].children:
                if self[child_idx].body == char:
                    current_node_idx = child_idx
                    found = True
                    break
            
            if not found:
                return False
            
        return self[current_node_idx].is_end




import sys


"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = None
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == ord(element):
                new_index = child_idx
                break
        
        if new_index is None:
            break
        
        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    # 구현하세요!
    input = sys.stdin.read
    data = input().splitlines()
    i = 0
    while i < len(data):
        t = Trie[int]()
        words = []
        try:
            N = int(data[i])
            i += 1
        except:
            break

        for _ in range(N):
            s = data[i].rstrip()
            t.push(map(ord, s))
            words.append(s)
            i += 1

        result = 0
        for word in words:
            result += count(t, word)

        avg_presses = result / N
        print(f"{avg_presses:.2f}")


if __name__ == "__main__":
    main()