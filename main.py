
import sys
import uuid

import psycopg2
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QErrorMessage, QWidget
from Auth import Authorization
from Reg import Registration

# class HospitalTable(QTableWidget):
#     def __init__(self, wg):
#         self.wg = wg
#         super().__init__(wg)
#         self.setGeometry(0, 0, 700, 500)
#         self.verticalHeader().show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Authorization()
    ex.connection()
    reg = Registration(ex.conn, ex.cur)
    ex.show()
    sys.exit(app.exec())