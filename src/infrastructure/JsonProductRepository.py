import json
import os
from typing import List, Optional
from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product

class JsonProductRepository(IProductRepository):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.__ensure_file_exists()
        self.__load_products()

    def __ensure_file_exists(self) -> None:
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file)

    def __load_products(self) -> None:
        try:
            with open(self.file_path, "r") as file:
                products_data = json.load(file)
                self.__products = []
                for data in products_data:
                    product = _Product(name=data['name'], quantity=data['quantity'], id=data['id'])
                    product.purchased = data['_purchased']
                    self.__products.append(product)
        except FileNotFoundError:
            self.__products = []

    def __save_products(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump([product.__dict__ for product in self.__products], file)

    def add_product(self, product: _Product) -> None:
        if self.get_product_by_id(product.id) is not None:
            raise ValueError(f"Product with id {product.id} already exists.")
        self.__products.append(product)
        self.__save_products()

    def get_all_products(self) -> List[_Product]:
        return self.__products

    def remove_product(self, product_id: str) -> None:
        product = self.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with id {product_id} does not exist.")
        self.__products = [product for product in self.__products if product.id != product_id]
        self.__save_products()

    def get_product_by_id(self, product_id: str) -> Optional[_Product]:
        for product in self.__products:
            if product.id == product_id:
                return product
        return None

    def update_product(self, product: _Product) -> None:
        for i, p in enumerate(self.__products):
            if p.id == product.id:
                self.__products[i] = product
                self.__save_products()
                return
        raise ValueError(f"Product with id {product.id} does not exist.")