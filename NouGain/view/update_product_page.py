from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
import requests
from io import BytesIO

class UpdateProductPage(QtWidgets.QWidget):
    def __init__(self):
        super(UpdateProductPage, self).__init__()
        self.init_ui()
        self.image_file_path = None

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.name_label = QtWidgets.QLabel('Nom du produit:')
        self.name_input = QtWidgets.QLineEdit()

        self.price_label = QtWidgets.QLabel('Prix:')
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setMaximum(1000000)

        self.tva_label = QtWidgets.QLabel('TVA:')
        self.tva_input = QtWidgets.QComboBox()

        self.description_label = QtWidgets.QLabel('Description:')
        self.description_input = QtWidgets.QLineEdit()

        self.discount_label = QtWidgets.QLabel('Promotion:')
        self.discount_input = QtWidgets.QDoubleSpinBox()
        self.discount_input.setMaximum(100)

        self.quantity_label = QtWidgets.QLabel('Quantité:')
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setMaximum(10000)

        self.unit_label = QtWidgets.QLabel('Format de quantité:')
        self.unit_input = QtWidgets.QComboBox()
        self.unit_input.addItems(["Kg", "Litre", "Gramme", "Unité"])

        self.unit_value_label = QtWidgets.QLabel('Format de quantité:')
        self.unit_value_input = QtWidgets.QDoubleSpinBox()
        self.unit_value_input.setMaximum(10000)

        self.season_label = QtWidgets.QLabel('Saison:')
        self.season_input = QtWidgets.QComboBox()

        self.active_label = QtWidgets.QLabel('Actif:')
        self.active_checkbox = QtWidgets.QCheckBox()

        self.date_activation_label = QtWidgets.QLabel('Date de création:')
        self.date_activation_input = QtWidgets.QLineEdit()
        self.date_activation_input.setReadOnly(True)

        self.image_label = QtWidgets.QLabel('Image:')
        self.image_button = QtWidgets.QPushButton('Selectionner une image')
        self.image_button.clicked.connect(self.select_image)
        self.image_file_name = QtWidgets.QLabel('Aucune image selectionné')

        self.update_button = QtWidgets.QPushButton('Modifier le Produit')
        self.back_button = QtWidgets.QPushButton('Retour')

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
        self.layout.addWidget(self.date_activation_label)
        self.layout.addWidget(self.date_activation_input)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.image_button)
        self.layout.addWidget(self.image_file_name)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)

    def select_image(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if file_path:
            self.image_file_path = file_path
            self.image_file_name.setText(file_path.split('/')[-1])

    def set_product_data(self, product_data):
        self.name_input.setText(product_data['Name'])
        self.price_input.setValue(product_data['Price_ht'])
        self.tva_input.setCurrentText(product_data['Tva_Name'])
        self.description_input.setText(product_data['Description'])
        self.discount_input.setValue(product_data.get('Discount', 0.0))
        self.quantity_input.setValue(product_data.get('Quantity', 0))
        self.unit_value_input.setValue(product_data.get('Unit_Value', 0.0))
        self.season_input.setCurrentText(product_data['Season_Name'])
        self.active_checkbox.setChecked(product_data['Active'])
        self.date_activation_input.setText(product_data['Date_activation'])

    def set_product_image(self, image_url):
        response = requests.get(image_url)
        pixmap = QPixmap()
        pixmap.loadFromData(BytesIO(response.content).read())
        self.image_display.setPixmap(pixmap)
