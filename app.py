from flask import Flask, render_template,redirect,request
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/review', methods=['GET'])
def reviews():
    return render_template('reviews.html')

@app.route('/api/review', methods=['POST'])     
def review():
    product_id = request.form["product_id"]
    error_message = 'Product not found'
    if product_id == '':
        return render_template('reviews.html',error=error_message)

    headers = {
        'authority': 'm.ceneo.pl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    response = requests.get('https://m.ceneo.pl/'+product_id, headers=headers)
    if response.status_code != 200:
        return render_template('reviews.html',error=error_message)
    else:
        return redirect(f'https://www.ceneo.pl/{product_id}')
        
if __name__ == '__main__':
    app.run(debug=True)