import json

class Product:
    def __init__(self,product_id):
        self.product_id = product_id
        self.product_data = {}
        self.reviews = []

    def product_data_to_json(self, product_name, product_image, product_reviews_count):
        self.product_data = {
            "product_id": self.product_id,
            "product_name": product_name,
            "product_image": product_image,
            "product_reviews_count": product_reviews_count,
            "reviews": self.reviews
        }
        
    def append_to_reviews(self,review):
        self.reviews.append(review)
        
    def save_to_json(self):
        with open(f'database/{self.product_id}.json', "w", encoding='utf-8') as f:
            json.dump(self.product_data, f, indent=4,ensure_ascii=False)
    
