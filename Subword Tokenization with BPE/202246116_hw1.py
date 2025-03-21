# 구현 순서 및 과정

# 1. 데이터 읽기 및 전처리
# 2. 초기 vocab 구성
# 3. BPE 학습 루트 구현
# 4. 학습 결과(vocab, merge rules) 저장
# 5. 병합 규칙 읽어오기
# 6. 토큰화 알고리즘 구현
# 7. 실행 제어 로직 구성

import argparse  # 파이썬에서 명령행 옵션을 쉽게 파싱하기 위한 모듈


# BPE 학습을 위한 클래스
class BPETrainer:
  def __init__(self, max_vocab_size: int):
    self.max_vocab_size = max_vocab_size
    self.vocab = {}
    self.merge_rules = []


# BPE 토크나이저 클래스
class BPETokenizer:
  def __init__(self, merge_path: str):
    self.merge_rules = self.load_merge_rules(merge_path)

  def load_merge_rules(self, merge_path: str):
    # 추후 구현 예정
    return {}


if __name__ == '__main__':
  print("Hello, BPE!")
  parser = argparse.ArgumentParser()
  # 학습 관련 옵션
  parser.add_argument('--train')
  parser.add_argument('--max_vocab', type=int)
  parser.add_argument('--vocab')
  parser.add_argument('--merge')

  # 추론 관련 옵션
  parser.add_argument('--infer')
  parser.add_argument('--input')
  parser.add_argument('--output')

  # 파싱
  args = parser.parse_args()

  # 학습 또는 추론에 따른 분기
  if args.train:
    trainer = BPETrainer(args.max_vocab)
    # 추후 구현할 함수들

  elif args.infer:
    tokenizer = BPETokenizer(args.merge)
    # 추후 구현할 함수들
