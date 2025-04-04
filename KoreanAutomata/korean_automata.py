# 구현을 위한 가이드라인
# 1. 데이터 정의 -> 초성, 중성, 종성, 복자음, 복모음
# 2. 상태 정의
# 3. 문자 판별 함수
# 4. 문자 처리 함수 (process() 함수)
# 5. 조합 함수 (combine() 함수)
# 6. 현재 완성된 글자를 결과 문자열에 저장
# 7. 실시간 문자 입력 처리
# 8. 결과 출력

import sys
import termios
import tty


class HangeulAutomata:
  def __init__(self):
    self.CHOSUNG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ',
                    'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    self.JUNGSUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
                     'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

    self.JONGSUNG = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ',
                     'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
                     'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    self.COMPLEX_CONSONANTS = {
      'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ',
      'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ',
      'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ'
    }

    # 상태 정의
    self.state = "START"
    self.cho = None
    self.jung = None
    self.jong = None
    self.buffer = None
    self.result = ""

  # 자음인지 확인하는 함수
  def is_consonant(self, char):
    # [1:]은 공백을 제거하기 위함임
    return char in self.CHOSUNG or char in self.JONGSUNG[1:]

  # 모음인지 확인하는 함수
  def is_vowel(self, char):
    return char in self.JUNGSUNG

  # 숫자 또는 특수문자인지 확인하는 함수
  def is_other(self, char):
    # consonant도 아니고 vowel도 아니라면 other로 설정
    return not self.is_consonant(char) and not self.is_vowel(char)

  # 문자를 상태별로 처리하는 함수
  def process(self, char):
    print(
        f"[입력: {char}] 상태: {self.state}, 초성: {self.cho}, 중성: {self.jung}, 종성: {self.jong}")
    if self.state == "START":
      if self.is_consonant(char):
        # 자음이 입력되면 초성으로 상태 전이
        self.cho = char
        self.state = "CHO"
      elif self.is_vowel(char):
        # 초성이 없는 모음 단독 입력은 바로 중성으로 처리
        self.jung = char
        self.flush()
      else:
        # 특수 문자라면 그대로 출력
        self.result += char

    # 초성 처리
    # 초성은 자음이 들어오면 그대로 저장하고, 모음이 들어오면 중성으로 전이
    elif self.state == "CHO":
      if self.is_vowel(char):
        self.jung = char
        self.state = "JUNG"
      elif self.is_consonant(char):
        self.flush()
        self.cho = char
      else:
        self.flush()
        self.result += char
        self.state = "START"

    # 중성 처리
    elif self.state == "JUNG":
      if self.is_vowel(char):
        self.flush()
        self.cho = None
        self.jung = None
        self.jong = None
        self.state = "START"
        self.result += char
      elif self.is_consonant(char):
        self.jong = char
        self.state = "JONG"
      else:
        self.flush()
        self.result += char
        self.state = "START"


    elif self.state == "JONG":
      if self.is_vowel(char):
        # 종성이 있는 상태에서 모음 입력 -> 새로운 글자
        temp = self.jong
        self.jong = None
        self.flush()  # 앞 글자 완성 (초성 + 중성)
        self.cho = temp  # 이전 종성을 새로운 초성으로 사용해서
        self.jung = char  # 현재 들어온 모음을 중성으로 사용해서
        self.state = "JUNG"  # 중성 상태로 전이
        # ex) ㄷ,ㅏ,ㄹ,ㄱ,ㅏ -> "달가"가 되도록 not 닭ㅏ

      elif self.is_consonant(char):
        combined = self.jong + char

        if combined in self.COMPLEX_CONSONANTS:
          # 복합 자음이 가능한 경우에는 앞과 뒤를 나눠서 처리해야함 (예: ㄹㅂ)
          self.buffer = char
          self.flush()  # 이전 글자를 완성
          self.cho = self.buffer  # 복합 자음의 뒷 부분을 초성으로 설정
          self.state = "CHO"
        else:
          # 복합 자음이 아니면 그냥 새 글자 시작
          self.flush()
          self.cho = char
          self.state = "CHO"

      else:
        self.flush()
        self.result += char
        self.state = "START"

  # 한글 자음 모음을 조합하는 함수
  def combine(self):
    if self.cho is None or self.cho not in self.CHOSUNG:
      return ""

    # 각각 초성, 중성, 종성의 인덱스를 구함 => 위의 list도 유니코드 순이여야 정상적으로 작동함
    cho_idx = self.CHOSUNG.index(self.cho)
    jung_idx = self.JUNGSUNG.index(self.jung) if self.jung else 0
    jong_idx = self.JONGSUNG.index(self.jong) if self.jong else 0

    # 완성형 한글 유니코드 = 0xAC00 + (초성 * 21 * 28) + (중성 * 28) + 종성
    return chr(0xAC00 + (cho_idx * 21 * 28) + (jung_idx * 28) + jong_idx)

  # 현재 조합된 초성, 중성, 종성을 출력하기 상태를 초기화시킴
  def flush(self):
    # 초성과 중성이 모두 존재한다면 combine() 함수를 통해 조합
    if self.cho and self.jung:
      self.result += self.combine()
    # 초성만 있다면 자음을 그대로 결과에 추가
    elif self.cho:
      self.result += self.cho
    # 중성이 존재한다면 모음을 그대로 결과에 추가
    elif self.jung:
      self.result += self.jung

    # 상태 초기화
    self.cho = None
    self.jung = None
    self.jong = None

  # 프로그램 종료 시 남은 문자를 처리하고 최종 결과를 반환해주는 함수
  def finalize(self):
    # 처리중이던 문자를 완성시키고 최종 결과를 반환
    self.flush()
    return self.result

  # 백스페이스 처리 함수
  def backspace(self):
    # 현재 조합중인 경우에는 조건에 따라 종성 -> 중성 -> 초성 순으로 삭제해야함.
    if self.state != "START":
      # 하지만 한글은 완성형 글자이기 때문에 종성일 때는 자동으로 삭제됨
      # 따라서 초성이 있을 때만 상태를 START로 바꿔주면 됨.
      if self.state == "CHO":
        self.cho = None
        self.state = "START"
      print("[백스페이스] 현재 남은 글자: " + self.result)

    # 조합이 아닌 경우에는 마지막 글자를 삭제하면 됨.
    elif self.result:
      # 마지막 글자
      last_char = self.result[-1]
      # 삭제했을 때 결과 문자열
      self.result = self.result[:-1]

      # 한글 범위 안에 있는 경우에는 START 상태로 바꾸면 됨.
      if 0xAC00 <= ord(last_char) <= 0xD7A3:
        self.state = "START"
      # 한글 범위가 아닌
      print(
          "[백스페이스] 한 글자 삭제됨, 남은 글자: " + self.result + "\t삭제한 글자: " + last_char)


# 한글을 입력받아 초성, 중성, 종성으로 분리하는 함수
# 한글은 완성형으로 입력돼서 분리시켜줘야함
# 예를 들어 강 -> ㄱ, ㅏ, ㅇ 으로 분리되어야 함 그래야 처리가 가능
def decompose_hangeul(char):
  '''
  완성형 한글 문자를 자모 단위로 분리하는 함수\n
  한글을 입력할 때는 완성된 글자로 입력되기 때문에
  초성, 중성, 종성으로 나누어주는 역할을 함
  '''
  CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ',
                  'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
  JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
                   'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
  JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ',
                   'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
                   'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

  code = ord(char)
  # 한글 범위인지 확인 (Unicode 0xAC00 ~ 0xD7A3)
  if 0xAC00 <= code <= 0xD7A3:
    # 한글 범위일 때만 초성, 중성, 종성으로 분리
    code -= 0xAC00
    cho = CHOSUNG_LIST[code // (21 * 28)]
    jung = JUNGSUNG_LIST[(code % (21 * 28)) // 28]
    jong = JONGSUNG_LIST[code % 28]
    return [cho, jung] + ([jong] if jong != ' ' else [])
  # 한글 범위가 아니라면 문자 그대로 반환
  else:
    return [char]


# 문자열을 입력받아 처리하는 함수
def getch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)  # 터미널을 raw 모드로 전환 -> 문자를 입력할 때마다 바로바로 처리
    char = sys.stdin.read(1)  # 문자를 입력받음
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return char


def main():
  automaton = HangeulAutomata()
  print("Korean Automata 시작! (종료: Ctrl+C)")

  # Ctrl+C를 누를 때까지 무한 반복
  while True:
    char = getch()

    # Ctrl+C를 누르면 종료
    if ord(char) == 3:  # Ctrl+C → 종료
      final_result = automaton.finalize()
      print("\n프로그램을 종료합니다.")
      print("최종 결과:", final_result)
      break
    # 백스페이스 키를 처리
    elif ord(char) == 127 or ord(char) == 8:
      automaton.backspace()
    # 입력된 문자가 한글이라면 자모 단위로 분리
    else:
      for c in decompose_hangeul(char):
        automaton.process(c)


if __name__ == "__main__":
  main()
