import requests
from bs4 import BeautifulSoup

class CeneoScraper:

    def __init__(self,product_id: str):
        self.product_id = product_id
        
    def get_product_data(self):
        response = requests.get("https://www.ceneo.pl/" + self.product_id + "#tab=reviews")
        if response.status_code == 404:
            return 'Product not found'
        
        soup = BeautifulSoup(response.text,'lxml')
        
        product_name = soup.find('h1',{'class':'product-top-section__product-name'}).text
        image = 'https:'+soup.find('li',{'class':'gallery__photo js_gallery-photo'}).find('img')['src']
        
    
    def get_reviews(self): 
        page_id = 1
        
        while True:
            
            reviews_endpoint = f'https://m.ceneo.pl/' + self.product_id +'/opinie-'+ str(page_id)
            
            response = requests.get(reviews_endpoint)
            if response.status_code == 301 or response.url != reviews_endpoint:
                break
                
            soup = BeautifulSoup(response.text,'lxml')
            
            for review in soup.find_all('div',{'class':'row no-margin--bottom js_review review-box-item js_product-review user-box-container'}):
                
                user = review.find('span',{'class':'review-box-reviewer js_review-user-name'}).text.strip()
                review_date = review.find('time')['datetime']
                review_score = float(review.find('span',{'class':'score__meter'}).text.strip().replace(',','.'))
                
                try:
                    review.find('span',{'class':'uppercase green-text ceneo-1 m-font-small'}).text.strip().lower()
                    is_recommend  = True
                except:
                    is_recommend  = False

                reviewText = review.find('div',{'class':'review-box-text js_review-text'}).text.strip()
                
                vote_up_count = review.find('button',{'data-new-icon':'vote-up'})['data-total-vote']
                vote_down_count = review.find('button',{'data-new-icon':'vote-down'})['data-total-vote']
                
            page_id+=1
            
    
x = CeneoScraper('115107321').get_reviews()

