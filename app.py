from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from models import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    products = Product.query.filter(
        db.or_(
            Product.description.ilike(f'%{query}%'),
            Product.product_no.ilike(f'%{query}%'),
            Product.category.ilike(f'%{query}%')
        )
    ).all()

    return render_template('search.html', products=products, query=query)

@app.route('/product/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('detail.html', product=product)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if Product.query.count() == 0:
            products_list = [
                {'p_no': 'P001', 'description': 'Kazak', 'price': 34.00, 'image_file': 'kazak.jpg', 'category': 'kazak'},
                {'p_no': 'P002', 'description': 'Pantolon', 'price': 50.90, 'image_file': 'pantolon.jpg', 'category': 'pantolon'},
                {'p_no': 'P003', 'description': 'Canta', 'price': 24.95, 'image_file': 'canta.jpg', 'category': 'Accessories'},
                {'p_no': 'P004', 'description': 'Atkı', 'price': 99.90, 'image_file': 'atkı.jpg', 'category': 'atkı'},
                {'p_no': 'P005', 'description': 'Sneakers', 'price': 1024, 'image_file': 'sneakers.jpg', 'category': 'sneakers'},
                {'p_no': 'P006', 'description': 'Krem Kaban', 'price': 279.90, 'image_file': 'kaban.jpg', 'category': 'kaban'},
                {'p_no': 'P007', 'description': 'Lacivert Cizgili Kaban', 'price': 458.90, 'image_file': 'kaban2.jpg', 'category': 'kaban'},
                {'p_no': 'P008', 'description': 'Mavi Gomlek', 'price': 140.99, 'image_file': 'gomlek.jpg', 'category': 'gomlek'},
                {'p_no': 'P009', 'description': 'Mom Jean', 'price': 34.99, 'image_file': 'jean.jpg', 'category': 'Jean'}
            ]

            for product in products_list:
                new_product = Product(
                    product_no=product['product_no'],
                    description=product['description'],
                    price=product['price'],
                    image_file=product['image_file'],
                    category=product['category']
                )
                db.session.add(new_product)

            db.session.commit()

    app.run(debug=False)
