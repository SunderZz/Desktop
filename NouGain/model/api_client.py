import requests
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.id_users: Optional[int] = None
        self.id_producers: Optional[int] = None
        self.token: Optional[str] = None

    def login(self, mail: str, password: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/users/login"
        response = requests.post(endpoint, params={"mail": mail, "password": password})
        response.raise_for_status() 
        data = response.json()
        self.id_users = data.get('Id_Users')
        if self.id_users:
            self.id_producers = self.get_producer_id(self.id_users)
            self.token = data.get('token')
        return data

    def get_producer_id(self, id_users: int) -> Optional[int]:
        endpoint = f"{self.base_url}/producers/{id_users}"
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data.get('Id_Producers')

    def get_give_products(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/give_producers"
        params = {"give_id": self.id_producers}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/products_by_id/"
        params = {"id": product_id}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_season_with_product(self, product_id: int) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/get_seasons_with_product"
        params = {"is_on_id": product_id}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_season_by_name(self, product_id: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/get_seasons_by_name"
        params = {"name": product_id}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_seasons(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/seasons"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_units(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/units"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_all_tvas(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/tva"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_tva(self, tva_id: int) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/tva/{tva_id}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_tva_by_name(self, tva_name: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/tva_name/{tva_name}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def calculate_tva(self, tva_name: str, price: float) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/tva/calculate/{tva_name}"
        params = {"price": price}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def add_product(self, producer_id: int, product_data: Dict[str, Any], unit_data: Dict[str, Any], quantity: int, season: int) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/producers/{producer_id}/create_product_by_producer"
        params = {"quantity": quantity, "season": season}
        payload = {
            "unit": unit_data,
            "products": product_data
        }
        response = requests.post(endpoint, params=params, json=payload)
        response.raise_for_status()
        return response.json()

    def update_product(self, product_id: int, product_data: Dict[str, Any], season: int) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/products/{product_id}"
        params = {"season": season}
        response = requests.put(endpoint, params=params, json=product_data)
        response.raise_for_status()
        return response.json()

    def logout(self) -> int:
        endpoint = f"{self.base_url}/users/logout"
        response = requests.delete(endpoint, json={"user_id": self.id_users})
        response.raise_for_status()
        if response.status_code == 200:
            self.id_users = None
            self.id_producers = None
            self.token = None
        return response.status_code

    def get_produit_image(self, produit_image_id: int) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/produit_image/{produit_image_id}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def upload_produit_image(self, produit_id: int, file_path: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/produit_image/upload/{produit_id}"
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file)}
            response = requests.post(endpoint, files=files)
            response.raise_for_status()
            return response.json()
        
    def replace_produit_image(self, produit_id: int, file_path: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/produit_image/replace/{produit_id}"
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file)}
            response = requests.put(endpoint, files=files)
            response.raise_for_status()
            return response.json()