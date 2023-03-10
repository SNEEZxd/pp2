from flask import Flask, render_template,redirect,request
from scraper import CeneoScraper

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
        
@app.route('/products', methods=['GET','POST'])
def products():
    if request.method == 'GET':
        return render_template('products.html')

@app.route('/product/charts/', methods=['GET','POST'])
def charts():
    if request.method == 'GET':
        return render_template('products.html')


if __name__ == '__main__':
    app.run(debug=True)
    