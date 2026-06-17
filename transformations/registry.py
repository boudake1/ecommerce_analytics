from transformations.events import clean_events
from transformations.customers import normalize_customers
from transformations.products import normalize_products

TRANSFORMATIONS = {
    "events": clean_events,
    "customers": normalize_customers,
    "products": normalize_products,
}