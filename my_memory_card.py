from random import shuffle
from PyQt5.QtCore import Qt
# все виджеты (элементы интерфейса) - Q + название на инглише
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QRadioButton,
    QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup)


ANSWER_BTN = 'Ответить'
NEXT_BTN = 'Следующий вопрос'
QU = "вопрос"
RIGHT = "верно"
WRONG = "неверно"

Q1 = {
    QU:'Какой национальности не существует?',
    RIGHT:'Скуфы',
    WRONG:['Бразики','Русские','Чеченцы']
}

Q2 = {
    QU:'как правильно?',
    RIGHT:'Обаюдно',
    WRONG:['Тумба Юмба','Умба тумба','Чиназес']
}
Q3 = {
    QU:'кто должен стродать в русской литературе?',
    RIGHT:'все',
    WRONG:['читатель','персонаж','писатель']
}

QS = [Q1, Q2, Q3]

class Stats:
    def __init__(self, questions):
        self.questions = questions
        self.total = len(questions)
        self.atmoment = 0
        self.right = 0

    def raiting(self):
        rait = int(self.right / self.total * 100)
        return f'{rait}%'

    def progress(self):
        return f'{self.atmoment + 1} из {self.total}'

    def plus_raiting(self):
        if self.atmoment == 0:
            self.right += 1
        else:
            self.right += 0.25
        

def show_result():
    raiting_txt.setText(stats.raiting())
    question_group.hide()
    answer_group.show()
    sabmit_btn.setText(NEXT_BTN)
    

def show_question():
    progress_txt.setText(stats.progress())
    answer_group.hide()
    question_group.show()
    sabmit_btn.setText(ANSWER_BTN)
    btn_group.setExclusive(False)
    for btn in btns:
        btn.setChecked(False)
    btn_group.setExclusive(True)

def test(txt):
    iswrong_txt.setText(txt)
    if sabmit_btn.text() == ANSWER_BTN:
        show_result()
    else:
        next_question()

def ask(question):
    shuffle(btns)
    question_txt.setText(question[QU])
    right_txt.setText(question[RIGHT])
    btns[0].setText(question[RIGHT])
    for i in range(1,4):
        btns[i].setText(question[WRONG][i-1])
    show_question()

def check_answer():
    if btns[0].isChecked():
        stats.plus_raiting()
        test('верно')
    else:   
        if btns[1].isChecked() or btns[2].isChecked() or btns[3].isChecked():
            test('неверно')

def next_question():
    stats.atmoment += 1
    if stats.atmoment >= stats.total:
        stats.atmoment = 0
        stats.right = 0
    q = stats.questions[stats.atmoment]
    ask(q)
# создание элементов интерфейса: самого приложения и главного окна
# без главного окна ничего не запустится
app = QApplication([])
main_window = QWidget()
# задать название окну (по умолчанию - python)
main_window.setWindowTitle('Memary Card')
main_window.resize(400, 400)

stats = Stats(QS)

progress_txt = QLabel('прогресс')

question_txt = QLabel('Какой национальности не существует?')
btn1 = QRadioButton('Бразики')
btn2 = QRadioButton('Русские')
btn3 = QRadioButton('Чеченцы')
btn4 = QRadioButton('Скуфы')
btns = [btn1, btn2, btn3, btn4]

btn_group = QButtonGroup()
for btn in btns:
    btn_group.addButton(btn)

question_group = QGroupBox('Варианты ответов')
sabmit_btn = QPushButton(ANSWER_BTN)

sabmit_btn.clicked.connect(check_answer)

iswrong_txt = QLabel('Правильно/Неправильно')
right_txt = QLabel('Правильный ответ')
raiting_txt = QLabel('рейтинг')
answer_group = QGroupBox('Результат теста')

answer_line = QVBoxLayout()
answer_line.addWidget(iswrong_txt, alignment=Qt.AlignLeft)
answer_line.addWidget(right_txt, alignment=Qt.AlignHCenter)
answer_line.addWidget(raiting_txt, alignment=Qt.AlignHCenter)
answer_group.setLayout(answer_line)
answer_group.hide()

ask(Q1)

formline1 = QHBoxLayout()
formline1.addWidget(btn1)
formline1.addWidget(btn2)

formline2 = QHBoxLayout()
formline2.addWidget(btn3)
formline2.addWidget(btn4)

formline = QVBoxLayout()
formline.addLayout(formline1)
formline.addLayout(formline2)

question_group.setLayout(formline)

mainlayout = QVBoxLayout()
mainlayout.addWidget(progress_txt, alignment=Qt.AlignLeft)
mainlayout.addWidget(question_txt, alignment=(Qt.AlignHCenter | Qt.AlignVCenter), stretch=2)
mainlayout.addWidget(question_group, stretch=8)
mainlayout.addWidget(answer_group, stretch=8)
mainlayout.addWidget(sabmit_btn, stretch=1)

mainlayout.setSpacing(5)

main_window.setLayout(mainlayout)

# показываем главное окно
main_window.show()
# выполняем, пока не нажмём крестик
app.exec_()