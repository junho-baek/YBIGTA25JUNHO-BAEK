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
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    # 구현하세요!
    strify: Callable[[str], list[str]] = lambda l: [name.strip() for name in l.split('\n') if name.strip()]

    lines: list[str] = sys.stdin.readlines()

    N = int(lines[0].strip())
    names: list[str] = strify('\n'.join(lines[1:]))

    def reduce_str(str1: str, str2: str) -> str:
        min_length = min(len(str1), len(str2))
        i = 0
        while i < min_length and str1[i] == str2[i]:
            i += 1
        return str1[:i+1]

    def reduce_str_list(sorted_list: list[str]) -> list[str]:
        if not sorted_list:
            return []
        
        n = len(sorted_list)
        result = []

        for i in range(n):
            if i == 0:
                prefix = reduce_str(sorted_list[i], sorted_list[i+1])
            elif i == n - 1:
                prefix = reduce_str(sorted_list[i], sorted_list[i-1])
            else:
                prefix1 = reduce_str(sorted_list[i], sorted_list[i-1])
                prefix2 = reduce_str(sorted_list[i], sorted_list[i+1])
                prefix = prefix1 if len(prefix1) > len(prefix2) else prefix2

            result.append(prefix)
        
        return result
    
    names.sort()
    names = reduce_str_list(names)
    
    trie: Trie[str] = Trie()
    for name in names:
        trie.push(name + "!")
    
    result = 1
    for trienode in trie:
        if len(trienode.children) > 1:
            for i in range(1, len(trienode.children)+1):
                result = result * i
    result = result % 1000000007

    print(result)


if __name__ == "__main__":
    main()