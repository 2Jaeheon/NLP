# 구현 순서 및 과정

# 1. 데이터 읽기 및 전처리
# 2. 초기 vocab 구성
# 3. BPE 학습 루트 구현
# 4. 학습 결과(vocab, merge rules) 저장
# 5. merge_rules & vocab 불러오기
# 6. BPE 알고리즘을 통한 Tokenization
# 7. 실행 및 결과

import argparse  # 파이썬에서 명령행 옵션을 쉽게 파싱하기 위한 모듈
import re


# BPE 학습을 위한 클래스
class BPETrainer:
  def __init__(self, max_vocab_size: int):
    self.max_vocab_size = max_vocab_size
    self.vocab = {}
    self.merge_rules = []

  # 데이터 전처리 함수 -> re(정규화 도와주는 도구 -> 정규표현식 배웠으니 써먹어보자)를 이용해 특수문자 제거하고 단어 단위로 나눈 후 단어를 문자 단위로 분리
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
      # 문자 단위로 분리된 단어에 공백을 추가해서 문자열로 변환
      spaced_word = ' '.join(letters)
      processed.append(spaced_word)

    return processed

  # vocab 구성 함수
  # corpus: 각 단어를 문자 단위로 분리한 리스트
  def build_vocab(self, corpus):
    self.vocab = {}
    for word in corpus:
      if word in self.vocab:
        self.vocab[word] += 1
      else:
        self.vocab[word] = 1

  # 연속된 pair의 빈도를 각 단어를 문자 단위로 분리한 후, pair로 만들어서 등장 빈도만큼 누적시킴
  def get_pair_frequency(self):
    pair_freq = {}

    # word: 단어, freq: 빈도
    for word, freq in self.vocab.items():
      # 단어를 문자 단위로 분리
      symbols = word.split()

      # 연속된 pair의 빈도를 계산함.
      for i in range(len(symbols) - 1):
        pair = (symbols[i], symbols[i + 1])
        # pair_freq[pair] = freq + 1은 오류 -> 기존 값에 freq를 더해줘야함.
        if pair in pair_freq:
          pair_freq[pair] += freq
        else:
          pair_freq[pair] = freq

    return pair_freq

  # 가장 빈도가 높은 pair를 찾아내는 함수
  # best_pair: 가장 빈도가 높은 pair -> 얘를 찾아서 병합시키는 것.
  def merge_most_frequent_pair(self, best_pair):
    pattern = re.escape(' '.join(best_pair))

    # 병합해서 만든 new Token! -> 이제 이걸 vocab에서 찾아서 병합해야함
    replacement = ''.join(best_pair)
    target = list(best_pair)
    new_vocab = {}

    # pair을 찾아서 문자열로 바꿈.
    for word, freq in self.vocab.items():
      symbols = word.split()
      new_symbols = []
      i = 0

      # 현재 문자 symbols[i] 와 다음 문자 symbols[i+1]가 best_pair(다빈도 쌍)와 같으면 병합.
      # 즉, 연속된 pair를 찾아서 이를 vocab에 반영 및 merge_rules에 추가
      while i < len(symbols):
        # 병합 대상 문자쌍이 등장하는지 확인
        if i < len(symbols) - 1 and symbols[i] == target[0] and symbols[
          i + 1] == target[1]:
          new_symbols.append(replacement)  # 병합!
          # 2개 문자를 한꺼번에 처리했으므로 2칸 이동 (i += 1을 하면 안 됨)
          i += 2
        else:
          new_symbols.append(symbols[i])
          i += 1
      # while 끝

      # 병합된 결과(new_symbols)를 다시 문자열로 변환 -> t h e => th e
      new_word = ' '.join(new_symbols)
      new_vocab[new_word] = freq
    # for 끝
    self.vocab = new_vocab
    self.merge_rules.append(best_pair)

  # merge_most_frequent_pair 끝

  # 지금까지 만든 함수들을 통해 BPE 알고리즘을 수행
  # corpus_path: 학습 데이터 파일 경로 -> 경로만 제공하면 알아서 수행.
  # main에서 train() 함수 하나만 출력해서 사용할 수 있도록 함.
  def train(self, corpus_path):
    # 전처리 과정
    corpus = self.preprocess_text(corpus_path)
    # vocab 구성
    self.build_vocab(corpus)
    # 디버깅을 위해서 구현 -> 학습 진행 상황을 보기 위함.
    prev_vocab_size = len(self.vocab)

    # BPE 학습 루프
    initial_char_count = len(
        set(symbol for word in self.vocab for symbol in word.split()))

    # vocab의 크기가 max_vocab_size가 될 때까지 반복
    # 다음이 교재에서 다룬 BPE 학습 루프임 -> 계속 반복해서 병합해나가는 과정
    while len(self.merge_rules) + initial_char_count < self.max_vocab_size:
      # 문자쌍 빈도 계산
      pair_freq = self.get_pair_frequency()
      # pair_freq가 비어있으면 더 이상 병합할 pair가 없다는 의미
      if not pair_freq:
        break

      # 가장 빈도가 높은 pair 병합
      best_pair = max(pair_freq, key=pair_freq.get)

      # 병합된 pair로 vocab 업데이트
      self.merge_most_frequent_pair(best_pair)

      # 100번 진행할 때마다 진행 상황 출력 -> 디버깅을 위해서 구현
      if len(self.merge_rules) % 100 == 0:
        curr_vocab_size = len(self.vocab)
        print(f"\n[진행 상황: {len(self.merge_rules)}회 병합 완료]")
        print(f"최근 저장된 pair: {best_pair} → {pair_freq[best_pair]}회")
        prev_vocab_size = curr_vocab_size

  # save_vocab_and_rules 함수 구현 -> vocab.txt에 vocab과 merge rules 저장
  # 두 가지를 한 파일에 저장하기 위해서 구분을 사용하였음. (==== ~~~~ ====)
  def save_vocab_and_rules(self, vocab_path):
    with open(vocab_path, 'w', encoding='utf-8') as f:
      # vocab를 먼저 저장
      f.write("==== Vocabulary ====\n")
      for word, freq in self.vocab.items():
        f.write(f"{word} {freq}\n")

      # merge rules를 저장
      f.write("\n==== Merge Rules ====\n")
      for pair in self.merge_rules:
        f.write(f"{pair[0]} {pair[1]}\n")


# BPE 토크나이저 클래스
class BPETokenizer:
  def __init__(self, merge_path: str):
    self.merge_rules = self.load_merge_rules(merge_path)

  # vocab.txt 파일에서 merge_rules를 읽어오는 함수
  def load_merge_rules(self, merge_path: str):

    merge_rules = []
    # 파일 오픈
    with open(merge_path, 'r', encoding='utf-8') as f:
      lines = f.readlines()

    # 현재 읽고 있는 섹션이 merge_rules인지 여부를 확인하기 위한 flag
    in_merge_section = False

    for line in lines:
      line = line.strip()

      # "==== Merge Rules ====" 라인을 찾으면 flag를 True로 변경 => 병합 규칙을 parsing
      if line == "==== Merge Rules ====":
        in_merge_section = True
        continue

      # 병합 규칙 줄만 parsing
      if in_merge_section and line:
        parts = line.split()
        # 공백으로 split 해서 두 개의 토큰인 경우만 merge_rules에 추가
        # 이는 에러 방지 + 유효한 병합 규칙만 필터링을 위함임
        if len(parts) == 2:
          merge_rules.append((parts[0], parts[1]))
    # 최종적으로 병합 규칙 리스트를 반환 (ex: [('t', 'h'), ('h', 'e'), ...])
    return merge_rules

  # 단어에 대해 BPE merge rule을 적용하는 함수
  def apply_BPE(self, word: str):
    tokens = list(word)

    # 병합 규칙을 순서대로 적용
    for merge_rule in self.merge_rules:
      i = 0

      while i < len(tokens) - 1:
        # merge_rule[0]과 merge_rule[1]이 연속적으로 나오는 경우 병합
        if tokens[i] == merge_rule[0] and tokens[i + 1] == merge_rule[1]:
          # 병합 대상이 되는 pair를 하나로 묶어서 token에 추가
          tokens = tokens[:i] + [''.join(merge_rule)] + tokens[i + 2:]
          # 0보다 작아지지 않도록 max 함수 사용
          # i를 1 줄여서 병합된 subword 이전 인덱스로 이동
          # 따라서 병합된 subword에 대해 다시 한 번 더 병합을 시도할 수 있도록 함
          i = max(i - 1, 0)
        else:
          i += 1

    # 첫 토큰 제외하고 앞에 ## 붙이기
    # 과제에서 요구하는 형식 -> white space와 구분을 하기 위함임.
    if not tokens:
      return []
    return [tokens[0]] + [f"##{t}" for t in tokens[1:]]

  # input_path에 있는 텍스트 파일을 읽고, BPE 토큰화를 적용하여 output_path에 저장하는 함수
  # main 함수에서는 tokenize_file 함수 하나만 사용할 수 있도록 함.
  def tokenize_file(self, input_path, output_path):
    # 파일 열기 (infile: 입력 파일, outfile: 출력 파일)
    with (open(input_path, 'r', encoding='utf-8') as infile,
          open(output_path, 'w', encoding='utf-8') as outfile):
      # 한 줄씩 읽어서 처리
      for line in infile:
        # 전처리 과정
        words = line.strip().lower().split()
        tokenized_line = []
        # 각 단어에 대해 BPE 토큰화 적용 -> tokenized_line에 추가
        for word in words:
          tokens = self.apply_BPE(word)
          tokenized_line.extend(tokens)

        # tokenized_line을 outfile에 씀.
        outfile.write(' '.join(tokenized_line) + '\n')


# main 함수 -> 학습(train) 모드와 추론(infer) 모드를 구분지어서 실행하도록 함.
if __name__ == '__main__':
  # argparse를 이용한 인자를 받아옴 -> 이렇게 하면 터미널에서 실행할 때 인자를 넘겨줄 수 있음. 완전 편함.
  parser = argparse.ArgumentParser()

  # 학습 모드 (train) 인자
  parser.add_argument('--train', help='학습 데이터 경로 (예: pg100.txt)')
  parser.add_argument('--max_vocab', type=int, help='최대 vocab 크기')
  parser.add_argument('--vocab', help='학습된 vocab 및 merge rules 저장 경로')

  # 추론 모드 (infer) 인자
  parser.add_argument('--infer', help='merge rules가 포함된 vocab 파일 경로')
  parser.add_argument('--input', help='토큰화할 입력 파일 경로')
  parser.add_argument('--output', help='토큰화된 결과 저장 경로')

  # 인자 parsing
  args = parser.parse_args()

  # 학습 모드
  if args.train and args.max_vocab and args.vocab:
    print("학습 모드 실행")
    trainer = BPETrainer(args.max_vocab)
    trainer.train(args.train)
    trainer.save_vocab_and_rules(args.vocab)
    print("학습 완료!")

  # 추론 모드
  elif args.infer and args.input and args.output:
    print("추론 모드 실행 중...")
    tokenizer = BPETokenizer(args.infer)
    tokenizer.tokenize_file(args.input, args.output)
    print("추론 완료! 결과가 저장되었습니다.")

  # 문제가 발생하는 경우 (인자 오류)
  else:
    print("잘못된 인자입니다. 다음 예시를 참고하세요:\n")
    print(
        "학습: python 202246116_hw1.py --train pg100.txt --max_vocab 30000 --vocab vocab.txt")
    print(
        "추론: python 202246116_hw1.py --infer vocab.txt --input infer.txt --output output.txt")
