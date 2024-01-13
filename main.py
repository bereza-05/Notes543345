from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout

import json

style = '''
QWidget {
    background-image: url('da.jpg'); 
    background-color: #f5f5f5;
}

QListWidget {
background-image: url(' .jpg'); 
    border: 2px solid #8e44ad;
    background-color: #ecf0f1;
    padding: 8px;
    color: #2c3e50;
}

QListWidget::item:selected {
    background-color: #8e44ad;
    color: #fff;
}

QPushButton {
    background-image: url(' .jpg'); 
    background-color: #9b59b6;
    color: #fff;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s ease-in-out;
}

QPushButton:hover {
    background-color: #8e44ad;
}

QLineEdit, QTextEdit {

    border: 2px solid #8e44ad;
    padding: 8px;
    background-color: #ecf0f1;
    color: #2c3e50;
}

QLabel {
    background-image: url(' .jpg'); 
    background-color: None; 
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
}

QWidget[editable="true"] {
    background-color: #7434a8;
    border: 2px solid #8e44ad;
    padding: 10px;
}

QTextEdit {
    margin-left: 0;
}

QHBoxLayout, QVBoxLayout {
    margin: 0;
    padding: 0;
}

QHBoxLayout > QPushButton {
    margin-right: 12px;
}

QVBoxLayout {
    spacing: 12px;
}

QHBoxLayout > QLineEdit, QHBoxLayout > QPushButton {
    margin-right: 12px;
}
'''






app = QApplication([])

app.setStyleSheet(style)
# notes={
#     "Ласкаво просимо":{
#         "текст":"У цьому додатку можна створити замітки з тегами...",
#         "теги":["інструкція","розумні замітки"]
#     }
# }

# with open("notes_data.json",'w',encoding='utf-8') as file:
#     json.dump(notes, file)


'''Інтерфейс програми'''
# параметри вікна програми
notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)

# віджети вікна програми
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')

button_note_create = QPushButton('Створити замітку')  # з'являється вікно з полем "Введіть ім'я замітки"
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки за тегом')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

# розташування віджетів по лейаутах
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

'''Функціонал програми'''

'''Робота з текстом замітки'''

def add_note():
    global notes
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)

def show_note():
    global notes
    # отримуємо текст із замітки з виділеною назвою та відображаємо її в полі редагування
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def save_note():
    global notes
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для збереження не вибрана!")

def del_note():
    global notes
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes.keys())
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для вилучення не обрана!")

'''Работа з тегами замітки'''

def add_tag():
    global notes
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для додавання тега не обрана!")

def del_tag():
    global notes
    if list_tags.selectedItems() and list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Тег для вилучення не обраний!")

def search_tag():
    global notes
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки за тегом" and tag:
        print(tag)
        notes_filtered = {}  # тут будуть замітки з виділеним тегом
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered.keys())
        print(button_tag_search.text())
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes.keys())
        button_tag_search.setText("Шукати замітки за тегом")
        print(button_tag_search.text())
    else:
        pass

'''Запуск програми'''
# підключення обробки подій
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

# запуск програми
notes_win.show()

try:
    with open("notes_data.json", "r") as file:
        data = file.read()
        if data:
            notes = json.loads(data)
        else:
            notes = {}
except json.JSONDecodeError:
    notes = {}

list_notes.addItems(notes.keys())

app.exec_()