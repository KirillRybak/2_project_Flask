from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer,nullable=False)
    isActive = db.Column(db.Boolean,default=True)
    text = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f'Название товара:{self.title}'


@app.route('/')
@app.route('/index')
def index():
    items= Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create_product', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']

        item = Item(title=title,price=price, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return '<h1>Произошла ошибка</h1>'
    else:
        return render_template('create_product.html')


@app.route('/payment')
def payment():
    return render_template('money.html')


if __name__ == '__main__':
    app.run(debug=True)