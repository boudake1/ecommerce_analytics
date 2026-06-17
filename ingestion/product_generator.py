from faker import Faker
import random
import json 

'''
This script generates fake JSON products for testing purposes.
{
  "product_id": "p123",
  "product_name": "p15",
  "categoryName": "Electronics",

'''

def generate_fake_product():
    faker = Faker()
    product = {
        "product_id": faker.uuid4(),
        "product_name": faker.catch_phrase(),
        "categoryName": faker.random_element(elements=("Electronics", "Clothing", "Books", "Home & Kitchen", "Sports & Outdoors", "Beauty & Personal Care")),
    }
    return product

def generate_fake_products(n):
    products = []
    for _ in range(n):
        products.append(generate_fake_product())
    return products
    
def generate_fake_products_json(n, file_path):
    products = generate_fake_products(n)
    with open(file_path, "w") as f:
        for product in products:
            f.write(json.dumps(product) + "\n")

#generate 1000 fake products
generate_fake_products_json(1000, "data/raw/products.json")      