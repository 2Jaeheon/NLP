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
    self.COMPLEX_VOELS = {'ㅗㅏ': 'ㅘ', 'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ', 'ㅜㅓ': 'ㅝ',
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
    pass

  # 한글 자음 모음을 조합하는 함수
  def combine(self):
    pass
