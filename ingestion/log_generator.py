from faker import Faker
import random
import json 

''''

This script generates fake JSON events for testing purposes.
{
  "event_id": "e123",
  "user_id": "u15",
  "session_id": "s10",
  "event_type": "product_view",
  "product_id": "p100",
  "price": 500,
  "country": "Senegal",
  "device": "mobile",
  "timestamp": "2026-06-05T12:00:00"


'''
products_list = []
faker = Faker()
with open("data/raw/products.json", "r") as file:
    for line in file:
        if line.strip():  # This skips empty lines if there are any
            products_list.append(json.loads(line))
customers_list = []
with open("data/raw/customers.json", "r") as file:
    for line in file:
        if line.strip():  # This skips empty lines if there are any
            customers_list.append(json.loads(line)) 

# 2. Extract arrays for Faker to choose from
# Adjust these keys based on what your actual JSON fields are named!
PRODUCT_IDS = [p["product_id"] for p in products_list]
USER_IDS = [p["user_id"] for p in customers_list]

def generate_fake_event():
    event = {
        "event_id": faker.uuid4(),
        "user_id": faker.random_element(USER_IDS),
        "session_id": faker.uuid4(),
        "event_type": faker.random_element(elements=("product_view", "purchase", "add_to_cart", "remove_from_cart", "search")),
        "product_id": faker.random_element(PRODUCT_IDS),
        "price": round(random.uniform(10.0, 1000.0), 2), # Rounded for realistic pricing
        "country": faker.country(),
        "device": faker.random_element(elements=("mobile", "web")), # Removed the duplicate "web"
        "timestamp": faker.date_time_this_year().isoformat()
    }
    return event

def generate_fake_events(n):
    events = []
    for _ in range(n):
        events.append(generate_fake_event())
    return events

def generate_fake_events_json(n, file_path):
    events = generate_fake_events(n)
    with open(file_path, "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

#generate 10000 fake events
generate_fake_events_json(10000, "data/raw/events.json")    
