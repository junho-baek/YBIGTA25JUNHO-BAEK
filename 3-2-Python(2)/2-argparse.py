import argparse
import logging


def create_parser() -> argparse.ArgumentParser:
    # 구현하세요!
    parser = argparse.ArgumentParser(description="2번 문제 구현 과제")
    parser.add_argument('start', type=int, help='Start value')
    parser.add_argument('end', type=int, help='End value')
    parser.add_argument('--verbose', action='store_true', help='불리언으로 verbose를 받음. if로 나눠서 출력을 바꿀 수 있음.')
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    start: int = args.start
    end: int = args.end
    verbose: bool = args.verbose

    print(start, end, verbose)

