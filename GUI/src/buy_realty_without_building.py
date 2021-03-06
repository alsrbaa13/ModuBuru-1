import sys
import os
import csv
import pickle
from PyQt4 import QtGui
from functools import partial

selectedNumOfBuilding = {'land' : 0, 'villa' : 0, 'building' : 0, 'hotel' : 0}

class BuyRealtyWithoutBuilding(QtGui.QMainWindow):
    def __init__(self):
        super(BuyRealtyWithoutBuilding, self).__init__()
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('Buy Realty Without Building')
        self.set_background()

        # '금액' 텍스트 표시 Label
        lblPriceTxt = QtGui.QLabel('금액', self)
        lblPriceTxt.setFont(QtGui.QFont('SansSerif', 80, QtGui.QFont.Bold))
        lblPriceTxt.resize(lblPriceTxt.sizeHint())
        lblPriceTxt.move(300, 100)

        # 금액 표시할 Label
        self.lblPrice = QtGui.QLabel('￦ 0', self)
        self.lblPrice.setFont(QtGui.QFont('SansSerif', 80))
        self.lblPrice.resize(750, 100)
        self.lblPrice.move(100, 300)

        # 토지 가격 세팅
        landPrice = self.show_price()

        # 구매 취소 PushButton
        self.btnCancel = QtGui.QPushButton('취소', self)
        self.btnCancel.clicked.connect(self.cancel_buy)
        self.btnCancel.setFont(QtGui.QFont('SansSerif', 50, QtGui.QFont.Bold))
        self.btnCancel.resize(200, 200)
        self.btnCancel.move(900, 100)

        # 구매 결정 PushButton
        self.btnOK = QtGui.QPushButton('구매', self)
        self.btnOK.clicked.connect(partial(self.pay_money, landPrice))
        self.btnOK.setFont(QtGui.QFont('SansSerif', 50, QtGui.QFont.Bold))
        self.btnOK.resize(200, 200)
        self.btnOK.move(900, 350)

        self.show()

    # 배경 설정 기능 호출 method
    def set_background(self):
        self.background = BackGround(self)
        self.setCentralWidget(self.background)

    # 토지 가격 보여주는 method
    def show_price(self):
        landNameColumn = 2
        landPriceColumn = 5
        f = open('./realty_info.csv', 'r')
        csvReader = csv.reader(f)
        for col in csvReader:
            if col[landNameColumn] == sys.argv[1]:
                self.lblPrice.setText('￦ %s' %col[landPriceColumn])
                break

        return col[landPriceColumn]

    # 구매 취소 버튼 클릭 이벤트 method
    def cancel_buy(self):
        selectedNumOfBuilding['land'] = 0
        buyFlag = 0
        f = open('selected_num_of_building.dat', 'wb')
        pickle.dump(selectedNumOfBuilding, f)
        pickle.dump(buyFlag, f)
        f.close()

        sys.exit()

    # 구매 버튼 클릭 이벤트 method
    def pay_money(self, landPrice):
        # 토지 수량 증가시키기
        selectedNumOfBuilding['land'] = 1
        totalPrice = self.lblPrice.text()[2:0]
        buyFlag = 1
        f = open('selected_num_of_building.dat', 'wb')
        pickle.dump(selectedNumOfBuilding, f)
        pickle.dump(buyFlag, f)
        pickle.dump(totalPrice, f)
        f.close()

        #print(landPrice)
        os.system('python3 pay_money.py %s' % landPrice)
        sys.exit()

# 배경 설정 class
class BackGround(QtGui.QFrame):
    def __init__(self, parent):
        super(BackGround, self).__init__(parent)
        self.init_background()

    def init_background(self):
        self.setStyleSheet('background-image: url("../image/%s.png")' % sys.argv[1])

def run():
    app = QtGui.QApplication([])
    window = BuyRealtyWithoutBuilding()
    app.exec_()

run()
