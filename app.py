from flask import Flask, render_template

app = Flask(__name__)

class API:
    
    @app.route('/')
    def home(self):
        return render_template('home.html')
    
    @app.route('/about')
    def about(self):
        return render_template('about.html')
    
    @app.route('/products')
    def products(self):
        return render_template('products.html')
    
    @app.route('/reviews')
    def reviews(self):
        return render_template('reviews.html')
    
api = API()

if __name__ == '__main__':
    app.run(debug=True)