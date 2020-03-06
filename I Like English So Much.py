

#####===============UI 및 기능
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from enum import Enum

#####===============파이어 베이스와 연동
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#사용자 인증 키
cred = credentials.Certificate("D:\git_private\win_to_lin\i-like-english-so-much-firebase-adminsdk-nps54-3820e79745.json")

#데이터베이스에 접근
db_url = 'https://i-like-english-so-much.firebaseio.com/'
voca_db = firebase_admin.initialize_app(cred, {'databaseURL' : db_url})

#UI파일 연결
main_class = uic.loadUiType("voca_main.ui")[0]
memo_class = uic.loadUiType("voca_memorizing.ui")[0]
list_class = uic.loadUiType("voca_list.ui")[0]

class Category(Enum):
    EIGHT = 0
    NINE = 1
    BASIC = 2
    MAIN = 3
    ELSE = 4

#첫 화면 띄울 때 사용하는 기본 class 선언
class MainClass(QMainWindow, main_class):
    def __init__(self):
        global Category
        
        super().__init__()
        self.title = '하하! 신나게 단어나 외우자고!'
        self.icon = self.style().standardIcon(getattr(QStyle, 'SP_FileDialogDetailedView'))
        self.setupUi(self)
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

        self.arr = [[self.option1_800_button, self.option1_800_input_kor, self.option1_800_input_eng],
               [self.option1_900_button, self.option1_900_input_kor, self.option1_900_input_eng],
               [self.option1_basic_button, self.option1_basic_input_kor, self.option1_basic_input_eng],
               [self.option1_main_button, self.option1_main_input_kor, self.option1_main_input_eng],
               [self.option1_else_button, self.option1_else_input_kor, self.option1_else_input_eng]]

        #UI 객체에 연결
        self.option1_800_button.clicked.connect(lambda:self.get_input(Category.EIGHT))
        self.option1_900_button.clicked.connect(lambda:self.get_input(Category.NINE))
        self.option1_main_button.clicked.connect(lambda:self.get_input(Category.MAIN))
        self.option1_basic_button.clicked.connect(lambda:self.get_input(Category.BASIC))
        self.option1_else_button.clicked.connect(lambda:self.get_input(Category.ELSE))

        self.greeting_text.mousePressEvent = self.start_memorizing
        self.list_button.clicked.connect(self.show_voca_list)
        
    #하하! 단어 좀 외워볼까!?
    def start_memorizing(self, event):
        self.main = MemoPage()
        self.main.show()
        self.close()
        return

    #단어 리스트 관리
    def show_voca_list(self):
        dlg = ListDialog()
        dlg.exec_()

    #파이어베이스에 단어 저장
    def add_directly(self, eng, kor, category):
        #파이어베이스 데이터베이스 접근 및 중복체크
        ref = db.reference()
        new_kor = kor
        if ref.child(category).child(eng).get() != None: #이미 있는 경우
            old_kor = ref.child(category).child(eng).get()
            new_kor = old_kor + '; ' + kor
        else: #새롭게 추가하는 경우
            old_numbering = ref.child('NUMBERING').child(category).get()
            ref.child('NUMBERING').child(category).set(old_numbering + 1)
        
        ref.child(category).child(eng).set(new_kor)
        return

    #################### 중복 단어 체크 기능 필요!! 현재: 넘버링 추, 뜻 덮어쓰기.
    #단어 바로 등록하기!
    #category: STRING type
    def get_input(self, category):
        idx = category.value

        #get input
        kor = self.arr[idx][1].toPlainText()
        eng = self.arr[idx][2].toPlainText()

        self.add_directly(eng, kor, category.name)
        return

    #파일로 단어 등록하기
    def add_file(file_name):
        return

class MemoPage(QMainWindow, memo_class):
    def __init__(self):
        super().__init__()
        self.title = '하하! 신나게 단어나 외우자고!'
        self.icon = self.style().standardIcon(getattr(QStyle, 'SP_FileDialogDetailedView'))
        self.setupUi(self)
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

        self.greeting_text.mousePressEvent = self.go_back
        self.list_button.clicked.connect(self.show_voca_list)

    def go_back(self, event):
        self.main = MainClass()
        self.main.show()
        self.close()
        return
    
    #단어 리스트 관리
    def show_voca_list(self):
        dlg = ListDialog()
        dlg.exec_()
        
class ListDialog(QDialog, list_class):
    def __init__(self):
        super().__init__()
        self.title = '하하! 아직 이만큼이나 더 남았다고!'
        self.icon = self.style().standardIcon(getattr(QStyle, 'SP_FileDialogDetailedView'))
        self.setupUi(self)
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

if __name__ == "__main__":
    #QApplication: 프로그램 실행 시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 객체 생성
    main_window = MainClass()

    #프로그램 화면 보여주기!
    main_window.show()

    #프로그램을 작동시키는 (=프로그램을 이벤트 루프로 진입시키는) 코드
    app.exec_()

    #프로그램 종료
    sys.exit()
