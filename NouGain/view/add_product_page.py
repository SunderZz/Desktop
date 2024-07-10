from PyQt5 import QtWidgets

class AddProductPage(QtWidgets.QWidget):
    def __init__(self):
        super(AddProductPage, self).__init__()
        self.init_ui()
        self.image_file_path = None

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.name_label = QtWidgets.QLabel('Nom du Produit:')
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

        self.image_label = QtWidgets.QLabel('Image:')
        self.image_button = QtWidgets.QPushButton('Selectionner une Image')
        self.image_button.clicked.connect(self.select_image)
        self.image_file_name = QtWidgets.QLabel('Aucune image selectionné')

        self.add_button = QtWidgets.QPushButton('Ajouter le produit')
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
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.image_button)
        self.layout.addWidget(self.image_file_name)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)

    def select_image(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if file_path:
            self.image_file_path = file_path
            self.image_file_name.setText(file_path.split('/')[-1])
