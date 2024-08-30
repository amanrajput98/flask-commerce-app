from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import io, jwt, secrets
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  
app.config['SECRET_KEY'] = secrets.token_hex(32)
db = SQLAlchemy(app)
app.app_context().push()
# User model for authentication
class User(db.Model):
    """User Model to store users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User:(user_id={self.id}, username={self.username}>"

# Product model for storing product data
class Product(db.Model):
    """Product model to store products"""
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    quantity_sold = db.Column(db.Integer)
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)

    def __repr__(self):
        return f"<Product:(id={self.id}, product_name={self.product_name}>"

# Decorator for verifying JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/signup', methods=['POST'])
def signup():
    """Sign Up for new User"""
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    """LogIn for existing Users and returns token"""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload-data', methods=['POST'])
@token_required
def upload_data(current_user):
    """Cleaning and transforming the data & Upload it to DB"""
    # Please modify or change the csv file for custom Inputs
    file = 'config/sample_ecommerce_dataset.csv'
    df = pd.read_csv(file)
    
    # Data Cleaning
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['price'].fillna(df['price'].median(), inplace=True)
    df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
    df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))
    
    # Insert data into the database
    for index, row in df.iterrows():
        new_product = Product(
            id=row['product_id'],
            product_name=row['product_name'],
            category=row['category'],
            price=row['price'],
            quantity_sold=row['quantity_sold'],
            rating=row['rating'],
            review_count=row['review_count']
        )
        db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Data uploaded successfully'})

@app.route('/summary-report', methods=['GET'])
@token_required
def summary_report(current_user):
    """Generate the summary report """
    # Generate summary report
    summary = db.session.query(
        Product.category,
        db.func.sum(Product.price * Product.quantity_sold).label('total_revenue'),
        db.func.max(Product.product_name).label('top_product'),
        db.func.max(Product.quantity_sold).label('top_product_quantity_sold')
    ).group_by(Product.category).all()

    # Convert to DataFrame for CSV export
    summary_df = pd.DataFrame([{
        'category': s.category,
        'total_revenue': s.total_revenue,
        'top_product': s.top_product,
        'top_product_quantity_sold': s.top_product_quantity_sold
    } for s in summary])

    # Generate CSV file
    output = io.StringIO()
    summary_df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='summary_report.csv'
    )

if __name__ == '__main__':
    # Create tables if they don't exist
    db.create_all()
    app.run(debug=True)