from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO

class ProductPage(QtWidgets.QWidget):
    product_edit_requested = QtCore.pyqtSignal(int)
    logout_requested = QtCore.pyqtSignal()

    def __init__(self):
        super(ProductPage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.header_layout = QtWidgets.QHBoxLayout()
        self.user_info_label = QtWidgets.QLabel()
        self.user_info_label.setFont(QtGui.QFont("Arial", 12))
        self.logout_button = QtWidgets.QPushButton('Déconnexion')
        self.logout_button.setFont(QtGui.QFont("Arial", 12))
        self.logout_button.setFixedSize(120, 40)
        self.logout_button.setStyleSheet("background-color: #FF6347; color: white; border-radius: 10px;")

        self.header_layout.addWidget(self.user_info_label, alignment=QtCore.Qt.AlignRight)
        self.header_layout.addWidget(self.logout_button, alignment=QtCore.Qt.AlignRight)

        self.add_product_layout = QtWidgets.QHBoxLayout()
        self.add_product_button = QtWidgets.QPushButton('Add Product')
        self.add_product_button.setFont(QtGui.QFont("Arial", 12))
        self.add_product_button.setFixedSize(150, 40)
        self.add_product_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.add_product_layout.addWidget(self.add_product_button, alignment=QtCore.Qt.AlignLeft)

        self.product_table_layout = QtWidgets.QVBoxLayout()
        self.product_table = QtWidgets.QTableWidget()
        self.product_table.setColumnCount(10)
        self.product_table.setHorizontalHeaderLabels([
            "Produit", "Description", "Prix HT", "Actif", "Date de Création",
            "Date de Modification", "Discount", "Saison", "Quantité", "Image"
        ])
        self.product_table.setAlternatingRowColors(True)
        self.product_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.product_table.horizontalHeader().setStretchLastSection(True)

        self.product_table_layout.addWidget(self.product_table)

        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.add_product_layout)
        self.layout.addLayout(self.product_table_layout)
        self.layout.setAlignment(self.product_table_layout, QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)

        self.product_table.cellDoubleClicked.connect(self.on_product_double_clicked)
        self.logout_button.clicked.connect(self.on_logout_button_clicked)

    def set_user_info(self, user_name):
        self.user_info_label.setText(f"Bienvenue {user_name}")

    def add_product_row(self, product):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)

        id_item = QtWidgets.QTableWidgetItem(product['Name'])
        id_item.setData(QtCore.Qt.UserRole, product['Id_Product'])
        self.product_table.setItem(row_position, 0, id_item)

        self.product_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(product['Description'] or ''))
        self.product_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(product['Price_ht'])))
        self.product_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(product['Active'])))
        self.product_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(product['Date_activation'] or '')))
        self.product_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(product['Date_stop'] or '')))
        self.product_table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(str(product['Discount'] or '')))
        self.product_table.setItem(row_position, 7, QtWidgets.QTableWidgetItem(str(product.get('Season_Name', 'N/A'))))
        self.product_table.setItem(row_position, 8, QtWidgets.QTableWidgetItem(str(product['Quantity'])))

        image_label = QtWidgets.QLabel()
        if 'ImageURL' in product and product['ImageURL']:
            self.set_image_from_url(image_label, product['ImageURL'])
        self.product_table.setCellWidget(row_position, 9, image_label)

    def set_image_from_url(self, label, url):
        response = requests.get(url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).read())
            label.setPixmap(pixmap)
            label.setScaledContents(True)
            label.setFixedSize(100, 100) 

    def on_product_double_clicked(self, row, column):
        product_id_item = self.product_table.item(row, 0)
        product_id = product_id_item.data(QtCore.Qt.UserRole)
        self.product_edit_requested.emit(product_id)

    def on_logout_button_clicked(self):
        self.logout_requested.emit()
