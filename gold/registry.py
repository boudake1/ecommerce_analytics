from gold.build_customer_360 import build_customer_360
from gold.build_product_performance import build_product_performance
from gold.build_category_performance import build_category_performance
from gold.prospect import prospect_user

AGGREGATIONS = {
    "customer_360": build_customer_360,
    "product_performance": build_product_performance,
    "category_performance": build_category_performance,
    "prospect_user": prospect_user
    #"sales_analytics": build_sales_analytics
}           