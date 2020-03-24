# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'word_editor.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class word_editor(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(640, 480)
        Dialog.setMinimumSize(QtCore.QSize(640, 480))
        Dialog.setMaximumSize(QtCore.QSize(640, 480))
        self.buttonbox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonbox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName("buttonbox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 150, 601, 243))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.description_edit = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.description_edit.setObjectName("description_edit")
        self.gridLayout.addWidget(self.description_edit, 6, 1, 1, 1)
        self.translation_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.translation_edit.setObjectName("translation_edit")
        self.gridLayout.addWidget(self.translation_edit, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.word_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.word_edit.setObjectName("word_edit")
        self.gridLayout.addWidget(self.word_edit, 2, 1, 1, 1)
        self.example_sentence_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.example_sentence_edit.setObjectName("example_sentence_edit")
        self.gridLayout.addWidget(self.example_sentence_edit, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.file_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.file_button.setObjectName("file_button")
        self.gridLayout.addWidget(self.file_button, 3, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.example_translation_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.example_translation_edit.setObjectName("example_translation_edit")
        self.gridLayout.addWidget(self.example_translation_edit, 5, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 3, 1, 1)
        self.pos_combo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.pos_combo.setObjectName("pos_combo")
        self.gridLayout.addWidget(self.pos_combo, 2, 4, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica LT Std")
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 3, 1, 1)
        self.rel_words_combo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.rel_words_combo.setObjectName("rel_words_combo")
        self.gridLayout.addWidget(self.rel_words_combo, 4, 4, 1, 2)
        self.related_image_label = QtWidgets.QLabel(Dialog)
        self.related_image_label.setGeometry(QtCore.QRect(0, 0, 641, 131))
        self.related_image_label.setObjectName("related_image_label")

        self.retranslateUi(Dialog)
        self.buttonbox.accepted.connect(Dialog.accept)
        self.buttonbox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Word Editor"))
        self.label_3.setText(_translate("Dialog", "Translation"))
        self.label.setText(_translate("Dialog", "New Word"))
        self.label_5.setText(_translate("Dialog", "Example Translation"))
        self.label_4.setText(_translate("Dialog", "Example Sentence"))
        self.file_button.setText(_translate("Dialog", "File..."))
        self.label_2.setText(_translate("Dialog", "Word"))
        self.label_9.setText(_translate("Dialog", "Description"))
        self.label_6.setText(_translate("Dialog", "Part of Speech"))
        self.label_7.setText(_translate("Dialog", "Related Image"))
        self.label_8.setText(_translate("Dialog", "Related Words"))
