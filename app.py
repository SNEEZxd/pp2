from flask import Flask, render_template,redirect,request

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

    # @app.route('api/review', methods=['POST'])     
    # def review(self):
        
if __name__ == '__main__':
    app.run(debug=True)