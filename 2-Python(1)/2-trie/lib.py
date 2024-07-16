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

