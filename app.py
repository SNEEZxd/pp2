from flask import Flask, render_template,request,url_for, make_response, send_file
from scraper import CeneoScraper
from product import Product
ceneo_craper = CeneoScraper()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product', methods=['GET','POST'])
def product():
    if request.method == 'GET':
        return render_template('getProduct.html')
    
    if request.method == 'POST':
        product_id = request.form["product_id"]
        
        if product_id == "":
            return render_template('getProduct.html',error = "Product does not exist")
        product_data = ceneo_craper.check_database(product_id)
        if product_data != {}:
            return render_template('product.html',product_data = product_data)
        else:
            if ceneo_craper.check_product_id(product_id):
                ceneo_craper.get_product_data()
                product_data = ceneo_craper.get_reviews()
                return render_template('product.html',product_data = product_data)
            else:
                return render_template('getProduct.html',error = "Product does not exist")
        
@app.route('/products', methods=['GET'])
def products():
    if request.method == 'GET':
        product = Product('')
        products = product.get_scrapped_products()
        if products == []:
            return render_template('products.html',error = "Firstly extract reviews!")
        else:
            return render_template('products.html',products = products)
            
@app.route('/product/charts/', methods=['GET','POST'])
def charts():
    if request.method == 'GET':
        return render_template('products.html')

@app.route('/download_file/<file_id>')
def download_json(file_id):
    with open('static'+file_id+'.json') as f:
        json_data = f.read()

    response = make_response(json_data)

    response.headers.set('Content-Disposition', 'attachment', filename=file_id+'.json')
    response.headers.set('Content-Type', 'application/json')

    return response

if __name__ == '__main__':
    app.run(debug=True)
    