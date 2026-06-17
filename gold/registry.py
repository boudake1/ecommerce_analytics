from gold.build_customer_360 import build_customer_360
from gold.build_product_performance import build_product_performance
from gold.build_category_performance import build_category_performance

AGGREGATIONS = {
    "customer_360": build_customer_360,
    "product_performance": build_product_performance,
    "category_performance": build_category_performance
    #"sales_analytics": build_sales_analytics
}           