# 구현을 위한 가이드라인
# 1. 데이터 정의 -> 초성, 중성, 종성, 복자음, 복모음
# 2. 상태 정의
# 3. 문자 판별 함수
# 4. 문자 처리 함수 (process() 함수)
# 5. 조합 함수 (combine() 함수)
# 6. 현재 완성된 글자를 결과 문자열에 저장
# 7. 실시간 문자 입력 처리
# 8. 결과 출력

class HangeulAutomata:
  def __init__(self):
    self.CHOSUNG = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ',
                    'ㅍ', 'ㅎ', 'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ']
    self.JUNGSUNG = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ',
                     'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
    self.JONGSUNG = [' ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ',
                     'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
                     'ㄿ', 'ㅀ', 'ㅄ', 'ㅆ']
    self.COMPLEX_CONSONANTS = {'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ',
                               'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ',
                               'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ'}
    self.COMPLEX_VOWELS = {'ㅗㅏ': 'ㅘ', 'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ', 'ㅜㅓ': 'ㅝ',
                           'ㅜㅔ': 'ㅞ', 'ㅜㅣ': 'ㅟ', 'ㅡㅣ': 'ㅢ'}

    # 상태 정의
    self.state = "START"
    self.cho = None
    self.jung = None
    self.jong = None
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
    if self.state == "START":
      if self.is_consonant(char):
        # 자음이 입력되면 초성으로 상태 전이
        self.cho = char
        self.state = "CHO"
      elif self.is_vowel(char):
        # 모음만 입력하면 복모음일 수 있음
        self.jung = char
        self.state = "START_CHK"
        # START_CHK는 복모음인지를 확인하는 것
      else:
        # 특수 문자라면 그대로 출력
        self.result += char

    # 현재 상태가 START_CHK일 때
    elif self.state == "START_CHK":
      if self.is_vowel(char):
        combined = self.jung + char
        if combined in self.COMPLEX_VOWELS:
          self.jung = self.COMPLEX_VOWELS[combined]
          self.state = "START"
        else:
          # 복합 모음이 아니라면 다시 처음의 상태로 복귀
          self.state = "START"
          self.process_input(char);

    # 초성 처리
    elif self.state == "CHO":
      if self.is_vowel(char):
        self.jung = char
        self.state = "JUNG"
      elif self.is_consonant(char):
        self.cho = char
      else:
        self.result += self.cho
        self.process(char)

    # 중성 처리
    elif self.state == "JUNG":
      if self.is_vowel(char):
        # 복모음인 경우에는 처리
        combined = self.jung + char
        if combined in self.COMPLEX_CONSONANTS:
          self.jung = self.COMPLEX_CONSONANTS[combined]

        # 복모음이 아니라면 다시 최초의 상태로 돌아가야함.
        else:
          self.result += self.cho + self.jung
          self.cho = None
          self.jung = None
          self.state = "START"
          self.process(char)

      # 자음일 때는 바로 종성의 상태로 전이
      elif self.is_consonant(char):
        self.jong = char
        self.state = "JONG"

      else:
        self.result += self.cho + self.jung
        self.cho = None
        self.jung = None
        self.state = "START"
        self.process(char)

    # 종성 처리
    elif self.state == "JONG":
      # 종성인 상태에서 모음이 입력되면 중성의 상태로 넘어가야함.
      if self.is_vowel(char):
        self.cho = self.jong
        self.jong = None
        self.jung = char
        self.state = "JONG"

      elif self.is_consonant(char):
        combined = self.jong + char
        if combined in self.COMPLEX_CONSONANTS:
          self.jong = combined
        else:
          # 겹받침이 불가능한 것
          self.cho = self.jong
          self.jong = None
          self.state = "CHO"
          self.process(char)

      else:
        self.result += self.cho + self.jung + self.jong
        self.cho = None
        self.jung = None
        self.jong = None
        self.state = "START"
        self.process(char)

  # 한글 자음 모음을 조합하는 함수
  def combine(self):
    pass
