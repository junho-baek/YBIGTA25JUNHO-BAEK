from lib import Trie
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