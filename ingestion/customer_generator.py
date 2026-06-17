from faker import Faker
import random
import json 

'''
This script generates fake JSON customers for testing purposes.
{
  "user_id": "u15",
  "name": "John Doe",
  "email": "[EMAIL_ADDRESS]",
  "age": 30,
  "gender": "Male",
  "address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",

'''

def generate_fake_customer():
    faker = Faker()
    customer = {
        "user_id": faker.uuid4(),
        "name": faker.name(),
        "email": faker.email(),
        "age": random.randrange(18, 90),
        "gender": faker.random_element(elements=("Male", "Female")),
        "address": faker.address(),
        "city": faker.city(),
        "state": faker.state(),
        "zip_code": faker.zipcode(),
    }
    return customer

def generate_fake_customers(n):
    customers = []
    for _ in range(n):
        customers.append(generate_fake_customer())
    return customers

def generate_fake_customers_json(n, file_path):
    customers = generate_fake_customers(n)
    with open(file_path, "w") as f:
        for customer in customers:
            f.write(json.dumps(customer) + "\n")

    

#generate 1000 fake customers
generate_fake_customers_json(1000, "data/raw/customers.json")    