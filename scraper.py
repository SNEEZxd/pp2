from bs4 import BeautifulSoup
from product import Product
import os, json, requests

class CeneoScraper:

    def __init__(self):
        self.product_id = ''
        self.product_reviews = Product(self.product_id)
        self.product_name = ''
        self.product_image = ''
        
    def check_product_id(self, product_id):
        self.product_id = product_id
        # dir_files = os.listdir('database')
        # if product_id in str(dir_files):
        #     for file in dir_files:
        #         if file == f'{product_id}.json':
        #             with open('database/' + file, encoding='utf-8') as f:
        #                 data = json.load(f)
        #             return data
        # else:
        response = requests.get("https://www.ceneo.pl/" + self.product_id)
        if response.status_code != 200:
            return False 
        else:
            return True
    def check_database(self,product_id):
        dir_files = os.listdir('database')
        
        if len(dir_files) > 0:
            for file in dir_files:
                if product_id in str(file):
                    with open('database/' + file, encoding='utf-8') as f:
                        data = json.load(f)
                    return data
            return {}
        else:       
            return {}      
    def get_product_data(self):
        response = requests.get("https://www.ceneo.pl/" + self.product_id + "#tab=reviews")
        soup = BeautifulSoup(response.text, 'lxml')
        self.product_name = soup.find('meta', {'name': 'keywords'})['content'].split(',')[0]
        self.product_image = soup.find('meta', {'property': 'og:image'})['content']

    def get_reviews(self):
        page_id = 1
        reviews_count = 0
        while True:
            reviews_endpoint = f'https://m.ceneo.pl/' + self.product_id + '/opinie-' + str(page_id)

            response = requests.get(reviews_endpoint)
            if response.status_code == 301 or response.url != reviews_endpoint:
                break

            soup = BeautifulSoup(response.text, 'lxml')

            for review in soup.find_all('div', {'class': 'row no-margin--bottom js_review review-box-item js_product-review user-box-container'}):

                user = review.find('span', {'class': 'review-box-reviewer js_review-user-name'}).text.strip()
                review_date = review.find('time')['datetime']
                review_score = float(review.find('span', {'class': 'score__meter'}).text.strip().replace(',', '.'))
                review_text = review.find('div', {'class': 'review-box-text js_review-text'}).text.strip().replace('\r\n                (…) więcej\n', '').replace('\n mniej', '')
                vote_up_count = review.find('button', {'data-new-icon': 'vote-up'})['data-total-vote']
                vote_down_count = review.find('button', {'data-new-icon': 'vote-down'})['data-total-vote']
                purchase_date = review.find('span', {'class': 'm-font-small'}).find('time')['datetime']
                advantages_count = 0
                disadvantages_count = 0

                advantages_raw = review.find('div', {'class': 'col s6 no-padding product-pros-cons m-font-small'})
                disadvantages_raw = review.find('div', {'class': 'col s6 product-pros-cons m-font-small'})
                if 'green-text' in str(advantages_raw):
                    advantages = advantages_raw.find('ul', {'class': 'no-margin--top no-margin--bottom'})
                    advantages_count += (len(advantages.find_all('li')))

                if 'red-text' in str(disadvantages_raw):
                    disadvantages = disadvantages_raw.find('ul', {'class': 'no-margin--top no-margin--bottom'})
                    disadvantages_count += (len(disadvantages.find_all('li')))

                try:
                    review.find('span', {'class': 'uppercase green-text ceneo-1 m-font-small'}).text.strip().lower()
                    is_recommend = True
                except:
                    is_recommend = False

                reviews_count += 1

                review_data = {"user": user,
                               "review_date": review_date,
                               "review_score": review_score,
                               "review_text": review_text,
                               "vote_up_count": vote_up_count,
                               "vote_down_count": vote_down_count,
                               "purchase_date": purchase_date,
                               "advantages_count": advantages_count,
                               "disadvantages_count": disadvantages_count,
                               "is_recommend": is_recommend}
                self.product_reviews.append_to_reviews(review_data)

            page_id += 1
        
        self.product_reviews.product_data_to_json(self.product_id, self.product_name, self.product_image, reviews_count)
        product_data = self.product_reviews.save_to_json()
        
        return product_data
        

