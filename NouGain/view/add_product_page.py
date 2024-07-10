from PyQt5 import QtWidgets, QtCore, QtGui

class AddProductPage(QtWidgets.QWidget):
    def __init__(self):
        super(AddProductPage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.name_label = QtWidgets.QLabel('Name:')
        self.name_input = QtWidgets.QLineEdit()

        self.price_label = QtWidgets.QLabel('Price:')
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setMaximum(1000000)

        self.tva_label = QtWidgets.QLabel('TVA:')
        self.tva_input = QtWidgets.QComboBox()

        self.description_label = QtWidgets.QLabel('Description:')
        self.description_input = QtWidgets.QLineEdit()

        self.discount_label = QtWidgets.QLabel('Discount:')
        self.discount_input = QtWidgets.QDoubleSpinBox()
        self.discount_input.setMaximum(100)

        self.quantity_label = QtWidgets.QLabel('Quantity:')
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setMaximum(10000)

        self.unit_label = QtWidgets.QLabel('Unit Type:')
        self.unit_input = QtWidgets.QComboBox()
        self.unit_input.addItems(["Kg", "Litre", "Gramme", "Unit"])

        self.unit_value_label = QtWidgets.QLabel('Unit Value:')
        self.unit_value_input = QtWidgets.QDoubleSpinBox()
        self.unit_value_input.setMaximum(10000)

        self.season_label = QtWidgets.QLabel('Season:')
        self.season_input = QtWidgets.QComboBox()

        self.active_label = QtWidgets.QLabel('Active:')
        self.active_checkbox = QtWidgets.QCheckBox()

        self.add_button = QtWidgets.QPushButton('Add Product')
        self.back_button = QtWidgets.QPushButton('Back')

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.price_label)
        self.layout.addWidget(self.price_input)
        self.layout.addWidget(self.tva_label)
        self.layout.addWidget(self.tva_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.discount_label)
        self.layout.addWidget(self.discount_input)
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(self.unit_label)
        self.layout.addWidget(self.unit_input)
        self.layout.addWidget(self.unit_value_label)
        self.layout.addWidget(self.unit_value_input)
        self.layout.addWidget(self.season_label)
        self.layout.addWidget(self.season_input)
        self.layout.addWidget(self.active_label)
        self.layout.addWidget(self.active_checkbox)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)
