from datetime import date
from PyQt5 import QtWidgets, QtCore
from model.api_client import APIClient
from view.home_page import HomePage
from view.login_page import LoginPage
from view.product_page import ProductPage
from view.add_product_page import AddProductPage
from view.update_product_page import UpdateProductPage

class MainController:
    def __init__(self):
        self.api_client = APIClient(base_url="http://127.0.0.1:8000")
        
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QStackedWidget()
        self.main_window.setCentralWidget(self.central_widget)

        self.home_page = HomePage()
        self.login_page = LoginPage()
        self.product_page = ProductPage()
        self.add_product_page = AddProductPage()
        self.update_product_page = UpdateProductPage()

        self.central_widget.addWidget(self.home_page)
        self.central_widget.addWidget(self.login_page)
        self.central_widget.addWidget(self.product_page)
        self.central_widget.addWidget(self.add_product_page)
        self.central_widget.addWidget(self.update_product_page)

        self.connect_signals()
        self.main_window.show()
        self.central_widget.setCurrentWidget(self.home_page)

    def connect_signals(self):
        self.home_page.home_button.clicked.connect(self.show_login_page)
        self.login_page.login_button.clicked.connect(self.login)
        self.product_page.add_product_button.clicked.connect(self.show_add_product_page)
        self.product_page.product_edit_requested.connect(self.show_update_product_page)
        self.product_page.logout_requested.connect(self.logout)
        self.add_product_page.add_button.clicked.connect(self.add_product)
        self.add_product_page.back_button.clicked.connect(self.show_product_page)
        self.update_product_page.update_button.clicked.connect(self.update_product)
        self.update_product_page.back_button.clicked.connect(self.show_product_page)

    def show_login_page(self):
        self.central_widget.setCurrentWidget(self.login_page)

    def show_add_product_page(self):
        self.load_combobox_data()
        self.central_widget.setCurrentWidget(self.add_product_page)

    def show_update_product_page(self, product_id):
        self.load_combobox_data()
        product_detail = self.api_client.get_product_by_id(product_id)
        season_detail = self.api_client.get_season_with_product(product_id)
        tva_detail = self.api_client.get_tva(product_detail['Id_tva'])
        product_detail['Season_Name'] = season_detail.get('Name', 'N/A')
        product_detail['Tva_Name'] = tva_detail['Name']
        self.update_product_page.set_product_data(product_detail)
        self.central_widget.setCurrentWidget(self.update_product_page)

    def show_product_page(self):
        self.central_widget.setCurrentWidget(self.product_page)

    def find_product_row(self, product_id):
        for row in range(self.product_page.product_table.rowCount()):
            item = self.product_page.product_table.item(row, 0)
            stored_product_id = item.data(QtCore.Qt.UserRole)
            if stored_product_id == product_id:
                return row
        return None

    def login(self):
        mail = self.login_page.login_input.text()
        password = self.login_page.password_input.text()
        response = self.api_client.login(mail, password)
        if 'Id_Users' in response:
            user_name = f"{response['F_Name']} {response['Name']}"
            self.product_page.set_user_info(user_name)
            if self.api_client.id_producers:
                self.central_widget.setCurrentWidget(self.product_page)
                self.load_products()
            else:
                print('Failed to retrieve producer ID')
        else:
            print('Login failed:', response.get('detail', 'Unknown error'))

    def load_products(self):
        give_products = self.api_client.get_give_products()
        self.product_page.product_table.setRowCount(0)

        for give in give_products:
            product_id = give['Id_Product']
            product_detail = self.api_client.get_product_by_id(product_id)
            season_details = self.api_client.get_season_with_product(product_id)
            tva_detail = self.api_client.get_tva(product_detail['Id_tva'])
            if isinstance(season_details, list):
                season_names = [detail.get('Name', 'N/A') for detail in season_details if isinstance(detail, dict)]
                product_detail['Season_Name'] = ', '.join(season_names) if season_names else 'N/A'
            else:
                product_detail['Season_Name'] = season_details.get('Name', 'N/A') if isinstance(season_details, dict) else 'N/A'
            product_detail['Tva_Name'] = tva_detail['Name']
            product_detail['Quantity'] = give['Quantity']

            self.product_page.add_product_row(product_detail)

    def add_product(self):
        name = self.add_product_page.name_input.text()
        price = self.add_product_page.price_input.value()
        tva_name = self.add_product_page.tva_input.currentText()
        description = self.add_product_page.description_input.text()
        discount = self.add_product_page.discount_input.value()
        quantity = self.add_product_page.quantity_input.value()
        unit_type = self.add_product_page.unit_input.currentText()
        unit_value = self.add_product_page.unit_value_input.value()
        season_name = self.add_product_page.season_input.currentText()
        active = self.add_product_page.active_checkbox.isChecked()  

        tva_details = self.api_client.get_tva_by_name(tva_name)
        tva_id = tva_details['Id_Tva']

        season_details = self.api_client.get_season_by_name(season_name)
        season_id = season_details['Id_Season']


        if not name or price == 0 or quantity == 0:
            QtWidgets.QMessageBox.warning(self.main_window, 'Validation Error', 'Please fill all required fields: Name, Price, Quantity.')
            return

        unit_data = {unit_type: unit_value}
        product_data = {
            "Name": name,
            "Description": description,
            "Price_ht": price,
            "Active": active,
            "Date_activation": date.today().isoformat(),
            "Date_stop": None,
            "Discount": discount,
            "Id_tva": tva_id
        }
        response = self.api_client.add_product(self.api_client.id_producers, product_data, unit_data, quantity, season_id)
        if 'Id_Product' in response:
            self.load_products()
            self.central_widget.setCurrentWidget(self.product_page)
        else:
            print('Failed to add product:', response.get('detail', 'Unknown error'))

    def update_product(self):
        selected_items = self.product_page.product_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            product_id_item = self.product_page.product_table.item(row, 0)
            product_id = product_id_item.data(QtCore.Qt.UserRole)
            
            name = self.update_product_page.name_input.text()
            price = self.update_product_page.price_input.value()
            tva_name = self.update_product_page.tva_input.currentText()
            description = self.update_product_page.description_input.text()
            discount = self.update_product_page.discount_input.value()
            quantity = self.update_product_page.quantity_input.value()
            unit_type = self.update_product_page.unit_input.currentText()
            unit_value = self.update_product_page.unit_value_input.value()
            season_name = self.update_product_page.season_input.currentText()
            active = self.update_product_page.active_checkbox.isChecked()
            date_activation = self.update_product_page.date_activation_input.text()

            tva_details = self.api_client.get_tva_by_name(tva_name)
            tva_id = tva_details['Id_Tva']

            season_details = self.api_client.get_season_by_name(season_name)
            season_id = season_details['Id_Season']
            
            if not name or price == 0 or quantity == 0:
                QtWidgets.QMessageBox.warning(self.main_window, 'Validation Error', 'Please fill all required fields: Name, Price, Quantity.')
                return

            unit_data = {unit_type: unit_value}
            product_data = {
                "Name": name,
                "Description": description,
                "Price_ht": price,
                "Active": active,
                "Date_activation": date_activation,
                "Date_stop": date.today().isoformat(),
                "Discount": discount,
                "Id_tva": tva_id
            }
            response = self.api_client.update_product(product_id, product_data, season_id)
            if response:
                self.load_products()
                self.central_widget.setCurrentWidget(self.product_page)
            else:
                print('Failed to update product:', response.get('detail', 'Unknown error'))

    def logout(self):
        status_code = self.api_client.logout()
        if status_code == 200:
            self.clear_ui()
            self.central_widget.setCurrentWidget(self.home_page)
        else:
            print('Failed to log out')

    def clear_ui(self):
        self.product_page.product_table.setRowCount(0)
        self.product_page.set_user_info('')
        self.add_product_page.name_input.clear()
        self.add_product_page.price_input.setValue(0)
        self.add_product_page.tva_input.setCurrentIndex(-1)
        self.add_product_page.description_input.clear()
        self.add_product_page.discount_input.setValue(0)
        self.add_product_page.quantity_input.setValue(0)
        self.add_product_page.unit_input.setCurrentIndex(-1)
        self.add_product_page.unit_value_input.setValue(0)
        self.add_product_page.season_input.setCurrentIndex(-1)
        self.add_product_page.active_checkbox.setChecked(False)  
        self.update_product_page.name_input.clear()
        self.update_product_page.price_input.setValue(0)
        self.update_product_page.tva_input.setCurrentIndex(-1)
        self.update_product_page.description_input.clear()
        self.update_product_page.discount_input.setValue(0)
        self.update_product_page.quantity_input.setValue(0)
        self.update_product_page.unit_input.setCurrentIndex(-1)
        self.update_product_page.unit_value_input.setValue(0)
        self.update_product_page.season_input.setCurrentIndex(-1)
        self.update_product_page.active_checkbox.setChecked(False)
        self.login_page.login_input.clear()
        self.login_page.password_input.clear()

    def load_combobox_data(self):
        tvas = self.api_client.get_all_tvas()
        self.add_product_page.tva_input.clear()
        self.update_product_page.tva_input.clear()
        for tva in tvas:
            self.add_product_page.tva_input.addItem(tva['Name'], tva['Rate'])
            self.update_product_page.tva_input.addItem(tva['Name'], tva['Rate'])

        seasons = self.api_client.get_seasons()
        self.add_product_page.season_input.clear()
        self.update_product_page.season_input.clear()
        for season in seasons:
            self.add_product_page.season_input.addItem(season['Name'], season['Id_Season'])
            self.update_product_page.season_input.addItem(season['Name'], season['Id_Season'])
