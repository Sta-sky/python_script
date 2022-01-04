
from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
	QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox, QVBoxLayout


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(941, 755)
        self.horizontalLayout_8 = QHBoxLayout(Form)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(12, 27, 441, 701))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblxh = QLabel(self.widget)
        self.lblxh.setObjectName(u"lblxh")

        self.horizontalLayout.addWidget(self.lblxh)

        self.inputxh = QLineEdit(self.widget)
        self.inputxh.setObjectName(u"inputxh")

        self.horizontalLayout.addWidget(self.inputxh)

        self.lblxm = QLabel(self.widget)
        self.lblxm.setObjectName(u"lblxm")

        self.horizontalLayout.addWidget(self.lblxm)

        self.inputxm = QLineEdit(self.widget)
        self.inputxm.setObjectName(u"inputxm")

        self.horizontalLayout.addWidget(self.inputxm)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lbyl = QLabel(self.widget)
        self.lbyl.setObjectName(u"lbyl")

        self.horizontalLayout_3.addWidget(self.lbyl)

        self.inputyl = QLineEdit(self.widget)
        self.inputyl.setObjectName(u"inputyl")

        self.horizontalLayout_3.addWidget(self.inputyl)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lblcssj = QLabel(self.widget)
        self.lblcssj.setObjectName(u"lblcssj")

        self.horizontalLayout_4.addWidget(self.lblcssj)

        self.input1cssj = QLineEdit(self.widget)
        self.input1cssj.setObjectName(u"input1cssj")

        self.horizontalLayout_4.addWidget(self.input1cssj)

        self.input2cssj = QLineEdit(self.widget)
        self.input2cssj.setObjectName(u"input2cssj")

        self.horizontalLayout_4.addWidget(self.input2cssj)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.input4cssj = QLineEdit(self.widget)
        self.input4cssj.setObjectName(u"input4cssj")

        self.horizontalLayout_5.addWidget(self.input4cssj)

        self.input3cssj = QLineEdit(self.widget)
        self.input3cssj.setObjectName(u"input3cssj")

        self.horizontalLayout_5.addWidget(self.input3cssj)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lblpzjd = QLabel(self.widget)
        self.lblpzjd.setObjectName(u"lblpzjd")

        self.horizontalLayout_6.addWidget(self.lblpzjd)

        self.inputpzjd = QLineEdit(self.widget)
        self.inputpzjd.setObjectName(u"inputpzjd")

        self.horizontalLayout_6.addWidget(self.inputpzjd)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buttoncalculation = QPushButton(self.widget)
        self.buttoncalculation.setObjectName(u"buttoncalculation")

        self.horizontalLayout_2.addWidget(self.buttoncalculation)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.buttonOpenCom = QPushButton(self.widget)
        self.buttonOpenCom.setObjectName(u"buttonOpenCom")

        self.horizontalLayout_2.addWidget(self.buttonOpenCom)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_8.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_img_show = QLabel(self.groupBox_2)
        self.label_img_show.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_img_show)


        self.horizontalLayout_8.addWidget(self.groupBox_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"功能区", None))
        self.lblxh.setText(QCoreApplication.translate("Form", u"型号", None))
        self.lblxm.setText(QCoreApplication.translate("Form", u"鞋码", None))
        self.lbyl.setText(QCoreApplication.translate("Form", u"拉力", None))
        self.lblcssj.setText(QCoreApplication.translate("Form", u"测试数据", None))
        self.lblpzjd.setText(QCoreApplication.translate("Form", u"偏折角度", None))
        self.buttoncalculation.setText(QCoreApplication.translate("Form", u"计算", None))
        self.buttonOpenCom.setText(QCoreApplication.translate("Form", u"打开设备", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"图像显示区", None))
        self.label_img_show.setText(QCoreApplication.translate("Form", u"", None))
    # retranslateUi

