# 구현 순서 및 과정

# 1. 데이터 읽기 및 전처리
# 2. 초기 vocab 구성
# 3. BPE 학습 루트 구현
# 4. 학습 결과(vocab, merge rules) 저장
# 5. 병합 규칙 읽어오기
# 6. 토큰화 알고리즘 구현
# 7. 실행 제어 로직 구성

import argparse  # 파이썬에서 명령행 옵션을 쉽게 파싱하기 위한 모듈
import re


# BPE 학습을 위한 클래스
class BPETrainer:
  def __init__(self, max_vocab_size: int):
    self.max_vocab_size = max_vocab_size
    self.vocab = {}
    self.merge_rules = []

  # 데이터 전처리 함수 -> re를 이용해 특수문자 제거, 단어 단위로 나눈 뒤, 각 단어를 문자 단위로 분리
  def preprocess_text(self, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
      text = f.read().lower()

    # 특수문자 제거 (a-z와 공백만 남기기)
    text = re.sub(r'[^a-z\s]', '', text)

    # 단어 단위로 나눈 뒤, 각 단어를 문자 단위로 분리
    words = text.strip().split()  # split()을 통해 공백을 기준으로 단어를 분리

    # 각 단어를 문자 단위로 분리함. 예) 'hello' -> ['h', 'e', 'l', 'l', 'o']
    # BPE 알고리즘은 문자 쌍을 반복적으로 병합하여 subword를 만드는 방식이기 때문에,
    # 초기에는 단어를 문자 단위로 나누는 것이 필요함
    processed = []
    for word in words:
      letters = list(word)
      spaced_word = ' '.join(letters)  # 문자 단위로 분리된 단어를 공백을 추가하여 문자열로 변환
      processed.append(spaced_word)

    return processed


# BPE 토크나이저 클래스
class BPETokenizer:
  def __init__(self, merge_path: str):
    self.merge_rules = self.load_merge_rules(merge_path)

  def load_merge_rules(self, merge_path: str):
    # 추후 구현 예정
    return {}


if __name__ == '__main__':
  # 임시 테스트용 코드
  trainer = BPETrainer(max_vocab_size=30000)
  corpus = trainer.preprocess_text('pg100.txt')
  print("전처리된 결과 예시:")
  for i in range(10000):  # 앞에서 10개만 출력
    print(corpus[i])

# if __name__ == '__main__':
#   print("Hello, BPE!")
#   parser = argparse.ArgumentParser()
#   # 학습 관련 옵션
#   parser.add_argument('--train')
#   parser.add_argument('--max_vocab', type=int)
#   parser.add_argument('--vocab')
#   parser.add_argument('--merge')
#
#   # 추론 관련 옵션
#   parser.add_argument('--infer')
#   parser.add_argument('--input')
#   parser.add_argument('--output')
#
#   # 파싱
#   args = parser.parse_args()
#
#   # 학습 또는 추론에 따른 분기
#   if args.train:
#     trainer = BPETrainer(args.max_vocab)
#     # 추후 구현할 함수들
#
#   elif args.infer:
#     tokenizer = BPETokenizer(args.merge)
#     # 추후 구현할 함수들
