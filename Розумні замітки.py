
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import * 
 
 
app=QApplication([]) 
 
notes = []
 
 
notes_win=QWidget() 
notes_win.setWindowTitle("Розумні замітки") 
notes_win.resize(900,600) 
notes_win.setStyleSheet("background-color: paleturquoise;")
 
list_notes=QListWidget() 
list_notes_label=QLabel("Список заміток") 
list_notes.setStyleSheet("background-color: palegreen;")
 
button_note_create=QPushButton("Створити замітку") 
button_note_del=QPushButton("Видалити замітку") 
button_note_save=QPushButton("Зберегти замітку") 
 

field_tag=QLineEdit() 
field_tag.setPlaceholderText("Введіть тег...") 
field_text=QTextEdit() 
button_tag_add=QPushButton("Додати до замітки") 
button_tag_del=QPushButton("Відкріпити від замітки") 
button_tag_search=QPushButton("Шукати замітки по тегу") 
list_tags=QListWidget() 
list_tags_label=QLabel("Список тегів") 
list_tags.setStyleSheet("background-color: palegreen;")
 
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
layout_notes.addLayout(col_1, stretch = 2) 
layout_notes.addLayout(col_2, stretch = 1) 
 
layout_notes.addLayout(col_1, stretch=2) 
layout_notes.addLayout(col_2, stretch=1) 
notes_win.setLayout(layout_notes) 

def show_note(): 
    key = list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if note[0] == keys:
            field_text.setText(note[1])
            list_tags.clear
            list_tags.addItems(note[2])
def add_note():
    note_name,ok = QInputDialog.getText(notes_win,"Додати за мітку","Назва за мітки")
    if ok and note_name!= '':
        note = list()
        note = [note_name, '',[]]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItems(note[2])
        print(notes)
        with open(str(len(notes)-1)+'txt','w') as file:
            file.write(note[0]+'/n')
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0 
        for note in  notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index)+ '.txt','w') as file:
                    file.write(note[0]+"\n")
                    file.write(note[1]+'\n')
                    for tag in note[2]:
                        file.write(tag+"")
                    file.write("\n")
            index += 1
        print(notes)
    else:
        print('Замітка для збереження не вибрана')
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
notes_win.show()
name = 0
note = []
while True:
    filename = str(name) + '.txt'
    try:
        with open(filename,'r') as file:
            for line in file:
                line = line.replace('\n','')
                note.append(line)
        tags = note[2].split(' ')
        note[2] = tags 
        notes.append(note) 
        note = []
        name += 1
    except IOError:
        break
print(notes)
for note in notes:
    list_notes.addItem(note[0])
app.exec_()           