from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QWidget
from ui import *
import json


# notes={
#     "Ласкаво просимо":{
#         "текст":"У цьому додатку можна створити замітки з тегами...",
#         "теги":["інструкція","розумні замітки"]
#     }
# }

# with open("note.json",'w',encoding='utf-8') as file:
#     json.dump(notes, file, ensure_ascii=False, indent=4)


app = QApplication([])
class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
note_names = []
with open("note.json",'r',encoding='utf-8') as file:
    notes = json.load(file)
    for n in notes:
        note_names.append(n)

ex = Widget()
ex.ui.listWidget.addItems(note_names)

def show_note():
    name = ex.ui.listWidget.selectedItems()[0].text()
    ex.ui.textEdit.setText(notes[name]["текст"])
    ex.ui.listWidget_2.clear()
    ex.ui.listWidget_2.addItems(notes[name]["теги"])

def add_note():
    notes_win = QWidget()
    note_name, result = QInputDialog.getText(
        notes_win, "Додати замітку", "Назва замітки:")
    notes[note_name] = {
        "текст": "",
        "теги": []
    }
    ex.ui.listWidget.addItem(note_name)
    ex.ui.listWidget_2.addItems(notes[note_name]["теги"])

def del_note():
    name = ex.ui.listWidget.selectedItems()[0].text()
    del notes[name]
    ex.ui.listWidget.clear()
    ex.ui.listWidget_2.clear()
    ex.ui.textEdit.clear()
    ex.ui.listWidget.addItems(notes)

def save_note():
    if ex.ui.listWidget.selectedItems():
        key = ex.ui.listWidget.selectedItems()[0].text()
        notes[key]['текст'] = ex.ui.textEdit.toPlainText()

def save_tag():
    if ex.ui.listWidget.selectedItems():
        key = ex.ui.listWidget.selectedItems()[0].text()
        tag = ex.ui.lineEdit.text()
        notes[key]['теги'].append(tag)
        ex.ui.lineEdit.clear()
        show_note()

def del_tag():
    if ex.ui.listWidget.selectedItems():
        key = ex.ui.listWidget.selectedItems()[0].text()
        tag = ex.ui.listWidget_2.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        show_note()

def search_tag():
    tag = ex.ui.lineEdit.text()
    print(ex.ui.pushButton_4.text() == "Шукати замітку по тегу" and tag)
    if ex.ui.pushButton_4.text() == "Шукати замітку по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        ex.ui.pushButton_4.setText("Скинути пошук")
        ex.ui.listWidget.clear()
        ex.ui.listWidget_2.clear()
        ex.ui.listWidget.addItems(notes_filtered)
    elif ex.ui.pushButton_4.text() == "Скинути пошук":
        ex.ui.listWidget.clear()
        ex.ui.listWidget_2.clear()
        ex.ui.lineEdit.clear()
        ex.ui.listWidget.addItems(notes)
        ex.ui.pushButton_4.setText("Шукати замітку по тегу")
    else:
        pass


ex.ui.listWidget.itemClicked.connect(show_note)
ex.ui.pushButton.clicked.connect(add_note)
ex.ui.pushButton_2.clicked.connect(del_note)
ex.ui.pushButton_3.clicked.connect(save_note)
ex.ui.pushButton_4.clicked.connect(save_tag)
ex.ui.pushButton_6.clicked.connect(del_tag)


ex.show()
app.exec_()