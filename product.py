import json
import os


class Product:
    def __init__(self, product_id):
        self.product_id = product_id
        self.product_data = {}
        self.reviews = []
        
    def save_to_json(self):
        with open(f'static/{self.product_id}.json', "w", encoding='utf-8') as f:
            json.dump(self.product_data, f, indent=4, ensure_ascii=False)
        return self.product_data
    
    def product_data_to_json(self,product_id, product_name, product_image, product_reviews_count):
        self.product_id = product_id
        self.product_data = {
            "product_id": product_id,
            "product_name": product_name,
            "product_image": product_image,
            "product_reviews_count": product_reviews_count,
            "reviews": self.reviews
        }

    def append_to_reviews(self, review):
        self.reviews.append(review)
            
    
    @staticmethod
    def product_stats(file):
        product_stats = {}
        average_score = 0
        total_advantages = 0
        total_disadvantages = 0
        total_recommend = 0
        total_not_recommend = 0
        product_rating = {0.5: 0 , 1.0: 0, 1.5: 0, 2.0: 0, 2.5: 0, 3.0: 0, 3.5: 0, 4.0: 0, 4.5: 0, 5.0: 0}

        for review in file["reviews"]:
            total_advantages += review["advantages_count"]
            total_disadvantages += review["disadvantages_count"]
            average_score += review["review_score"]
            if review["is_recommend"]:
                total_recommend += 1
            else:
                total_not_recommend += 1
                
            product_rating[review["review_score"]] += 1 
            
        product_stats["product_rating"] = product_rating
        product_stats["total_recommend"] = total_recommend
        product_stats["total_not_recommend"] = total_not_recommend
        product_stats["total_advantages"] = total_advantages
        product_stats["total_disadvantages"] = total_disadvantages
        product_stats["average_score"] = round(average_score / len(file["reviews"]), 1)
        return product_stats
    
    @staticmethod
    def get_scrapped_products():
        products = []
        dir_files = os.listdir('static')
        
        if len(dir_files) > 0:
            for file in dir_files:
                with open('static/' + file, encoding='utf-8') as f:
                    data = json.load(f)
                    
                product_stats =  Product.product_stats(data)
                products.append({"product_id": data["product_id"],
                                 "product_name": data["product_name"],
                                 "product_image": data["product_image"],
                                 "product_rating": product_stats["product_rating"],
                                 "total_product_reviews": data["product_reviews_count"],
                                 "total_advantages": product_stats["total_advantages"],
                                 "total_disadvantages": product_stats["total_disadvantages"],
                                 "average_score": product_stats["average_score"]})
            return products
        else:
            return products
