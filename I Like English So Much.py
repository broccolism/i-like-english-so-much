
#####===============파이어 베이스와 연동
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#사용자 인증 키
cred = credentials.Certificate("D:\git_private\win_to_lin\i-like-english-so-much-firebase-adminsdk-nps54-3820e79745.json")

#데이터베이스에 접근
db_url = 'https://i-like-english-so-much.firebaseio.com/'
voca_db = firebase_admin.initialize_app(cred, {'databaseURL' : db_url})

#####===============UI 및 기능
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

#UI파일 연결
#memo_class = uic.loadUiType("memorizing.ui")[0]
main_class = uic.loadUiType("vocabulary.ui")[0]

#단어 암기 시 사용하는 class 선언
'''
class MemorizeClass(QMainWindow, form_class):
    def __init(self):
        super().__init__()
        self.setupUi(self)'''

#첫 화면 띄울 때 사용하는 기본 class 선언
class MainClass(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.title = '하하! 신나게 단어나 외우자고!'
        self.icon = self.style().standardIcon(getattr(QStyle, 'SP_FileDialogDetailedView'))
        self.setupUi(self)
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

        #UI 객체에 연결
        self.option1_800_button.clicked.connect(lambda:self.get_input("800"))
        self.option1_900_button.clicked.connect(lambda:self.get_input("900"))
        self.option1_main_button.clicked.connect(lambda:self.get_input("main"))
        self.option1_basic_button.clicked.connect(lambda:self.get_input("basic"))
        self.option1_else_button.clicked.connect(lambda:self.get_input("else"))
        
    #하하! 단어 좀 외워볼까!?
    def start_memorizing():
        return

    #파이어베이스에 단어 저장
    def add_directly(self, eng, kor, category):
        #파이어베이스 데이터베이스 접근
        ref = db.reference()
        
        ref.child(category).child(eng).set(kor)
        
        old_numbering = ref.child('numbering').child(category).get()
        ref.child('numbering').child(category).set(old_numbering + 1)
        return

    #################### 중복 단어 체크 기능 필요!! 현재: 넘버링 추, 뜻 덮어쓰기.
    #단어 바로 등록하기!
    #category: STRING type
    def get_input(self, category):
        arr = [[self.option1_800_button, self.option1_800_input_kor, self.option1_800_input_eng],
               [self.option1_900_button, self.option1_900_input_kor, self.option1_900_input_eng],
               [self.option1_basic_button, self.option1_basic_input_kor, self.option1_basic_input_eng],
               [self.option1_main_button, self.option1_main_input_kor, self.option1_main_input_eng],
               [self.option1_else_button, self.option1_else_input_kor, self.option1_else_input_eng]]

        idx = 0
        if category == '900':
            idx = 1
        elif category == 'basic':
            idx = 2
        elif category == 'main':
            idx = 3
        elif category == 'else':
            idx = 4
        
        #get input
        kor = arr[idx][1].toPlainText()
        eng = arr[idx][2].toPlainText()

        self.add_directly(eng, kor, category)
        return


    #파일로 단어 등록하기
    def add_file(file_name):
        return

if __name__ == "__main__":
    #QApplication: 프로그램 실행 시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 객체 생성
    main_window = MainClass()

    #프로그램 화면 보여주기!
    main_window.show()

    #프로그램을 작동시키는 (=프로그램을 이벤트 루프로 진입시키는) 코드
    app.exec_()
