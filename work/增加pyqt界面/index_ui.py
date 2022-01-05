# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designermfTbOD.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PyQt5.QtCore import QCoreApplication, QMetaObject, QSize
from PyQt5.QtWidgets import QHBoxLayout, QGroupBox, QSpacerItem, QSizePolicy, QPushButton, QVBoxLayout, QLabel, \
	QLineEdit, QTextEdit, QGridLayout


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(940, 631)
        self.horizontalLayout_7 = QHBoxLayout(Form)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_fly_1 = QPushButton(self.groupBox)
        self.btn_fly_1.setObjectName(u"btn_fly_1")
        self.btn_fly_1.setSizeIncrement(QSize(0, 100))

        self.verticalLayout.addWidget(self.btn_fly_1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.status_lin_1 = QLineEdit(self.groupBox)
        self.status_lin_1.setObjectName(u"status_lin_1")

        self.verticalLayout.addWidget(self.status_lin_1)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.textEdit = QTextEdit(self.groupBox)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_2.addWidget(self.textEdit)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_5.addLayout(self.horizontalLayout)


        self.horizontalLayout_7.addWidget(self.groupBox)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_fly_2 = QPushButton(self.groupBox_2)
        self.btn_fly_2.setObjectName(u"btn_fly_2")

        self.horizontalLayout_3.addWidget(self.btn_fly_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.status_lin_2 = QLineEdit(self.groupBox_2)
        self.status_lin_2.setObjectName(u"status_lin_2")

        self.horizontalLayout_2.addWidget(self.status_lin_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_fly_3 = QPushButton(self.groupBox_3)
        self.btn_fly_3.setObjectName(u"btn_fly_3")

        self.verticalLayout_4.addWidget(self.btn_fly_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.status_lin_3 = QLineEdit(self.groupBox_3)
        self.status_lin_3.setObjectName(u"status_lin_3")

        self.verticalLayout_3.addWidget(self.status_lin_3)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_gd = QPushButton(self.groupBox_3)
        self.btn_gd.setObjectName(u"btn_gd")

        self.gridLayout.addWidget(self.btn_gd, 0, 1, 1, 1)

        self.btn_wsdgd = QPushButton(self.groupBox_3)
        self.btn_wsdgd.setObjectName(u"btn_wsdgd")

        self.gridLayout.addWidget(self.btn_wsdgd, 2, 0, 1, 1)

        self.btn_tlnj = QPushButton(self.groupBox_3)
        self.btn_tlnj.setObjectName(u"btn_tlnj")

        self.gridLayout.addWidget(self.btn_tlnj, 2, 1, 1, 1)

        self.btn_fy = QPushButton(self.groupBox_3)
        self.btn_fy.setObjectName(u"btn_fy")

        self.gridLayout.addWidget(self.btn_fy, 0, 0, 1, 1)

        self.btn_czsd = QPushButton(self.groupBox_3)
        self.btn_czsd.setObjectName(u"btn_czsd")

        self.gridLayout.addWidget(self.btn_czsd, 1, 1, 1, 1)

        self.btn_jksd = QPushButton(self.groupBox_3)
        self.btn_jksd.setObjectName(u"btn_jksd")

        self.gridLayout.addWidget(self.btn_jksd, 1, 0, 1, 1)

        self.btn_fly_hx = QPushButton(self.groupBox_3)
        self.btn_fly_hx.setObjectName(u"btn_fly_hx")

        self.gridLayout.addWidget(self.btn_fly_hx, 3, 0, 1, 1)

        self.btn_mhs = QPushButton(self.groupBox_3)
        self.btn_mhs.setObjectName(u"btn_mhs")

        self.gridLayout.addWidget(self.btn_mhs, 3, 1, 1, 1)


        self.horizontalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_6.addWidget(self.groupBox_3)


        self.horizontalLayout_7.addLayout(self.verticalLayout_6)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u7a0b\u5e8f\u4e00", None))
        self.btn_fly_1.setText(QCoreApplication.translate("Form", u"\u98de\u884c\u6570\u636e\u4f20\u8f93\u4e0e\u5b58\u50a8\u7cfb\u7edf", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8fde\u63a5\u72b6\u6001", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u63a5\u6536\u4fe1\u606f:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u7a0b\u5e8f\u4e8c", None))
        self.btn_fly_2.setText(QCoreApplication.translate("Form", u"\u98de\u884c\u6570\u636e\u7b5b\u9009\u4e0e\u8bd1\u7801\u7cfb\u7edf", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u72b6\u6001:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u7a0b\u5e8f\u4e09", None))
        self.btn_fly_3.setText(QCoreApplication.translate("Form", u"\u98de\u884c\u6570\u636e\u7b5b\u9009\u4e0e\u5206\u6790\u7cfb\u7edf", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u72b6\u6001:", None))
        self.btn_gd.setText(QCoreApplication.translate("Form", u"\u6eda\u52a8", None))
        self.btn_wsdgd.setText(QCoreApplication.translate("Form", u"\u65e0\u7ebf\u7535\u9ad8\u5ea6", None))
        self.btn_tlnj.setText(QCoreApplication.translate("Form", u"\u63a8\u7406\u626d\u77e9", None))
        self.btn_fy.setText(QCoreApplication.translate("Form", u"\u4fef\u4ef0", None))
        self.btn_czsd.setText(QCoreApplication.translate("Form", u"\u5782\u76f4\u901f\u5ea6", None))
        self.btn_jksd.setText(QCoreApplication.translate("Form", u"\u8ba1\u7b97\u7a7a\u901f", None))
        self.btn_fly_hx.setText(QCoreApplication.translate("Form", u"\u822a\u5411", None))
        self.btn_mhs.setText(QCoreApplication.translate("Form", u"\u9a6c\u8d6b\u6570", None))
    # retranslateUi

