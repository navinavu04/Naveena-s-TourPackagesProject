from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from extensions import db
from forms import VendorRegistrationForm,PackageForm
from models import User, Vendor,Package,Booking
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.path.join('static', 'uploads')

def create_app():
            app = Flask(__name__, template_folder='app/templates')
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            app.config['SECRET_KEY'] = 'your_secret_key_here'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            db.init_app(app)
            return app

app = create_app()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id 
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return f"Registration successful for {username}"
    return render_template('register.html')

@app.route('/vendor/register', methods=['GET', 'POST'])
def vendor_register():
    form = VendorRegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        vendor = Vendor(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor registered successfully!', 'success')
        return redirect(url_for('vendor_register'))  # Change to vendor_login later
    return render_template('vendor_register.html', form=form)

@app.route('/vendor/login', methods=['GET', 'POST'])
def vendor_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        vendor = Vendor.query.filter_by(email=email).first()
        if vendor and check_password_hash(vendor.password, password):
            session['vendor_id'] = vendor.id
            flash('Login successful!', 'success')
            return redirect(url_for('vendor_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('vendor_login.html')


@app.route('/vendor/create_package', methods=['GET', 'POST'])
def create_package():
    form = PackageForm()
    if form.validate_on_submit():
        vendor_id = 1  
        filename = None
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_package = Package(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            location=form.location.data,
            duration=form.duration.data,
            vendor_id=vendor_id,
            image=filename
        )
        db.session.add(new_package)
        db.session.commit()
        flash('Package created successfully!', 'success')
        return redirect(url_for('vendor_dashboard'))
    
    if form.errors:
        print("Form errors:", form.errors)

    return render_template('create_package.html', form=form)

@app.route('/vendor/dashboard')
def vendor_dashboard():
    vendor_id = 1
    packages = Package.query.filter_by(vendor_id=vendor_id).all()
    return render_template('vendor_dashboard.html', packages=packages)

@app.route('/vendor/package/edit/<int:package_id>', methods=['GET', 'POST'])
def edit_package(package_id):
    package = Package.query.get_or_404(package_id)
    form = PackageForm(obj=package)  

    if form.validate_on_submit():
        package.title = form.title.data
        package.description = form.description.data
        package.price = form.price.data
        db.session.commit()
        flash('Package updated successfully!', 'success')
        return redirect(url_for('vendor_dashboard'))

    return render_template('edit_package.html', form=form)

@app.route('/vendor/package/delete/<int:package_id>', methods=['POST'])
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('vendor_dashboard'))

@app.route('/view_packages')
def view_packages():
    packages = Package.query.all()
    return render_template('view_packages.html', packages=packages)

@app.route('/book/<int:package_id>', methods=['POST'])
def book_package(package_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to book a package.", "warning")
        return redirect(url_for('login'))
    booking = Booking(user_id=user_id, package_id=package_id)
    db.session.add(booking)
    db.session.commit()
    flash("Package booked successfully!", "success")
    return redirect(url_for('view_packages'))

@app.route('/user/bookings')
def user_bookings():
    user_id = 1 
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return render_template('user_bookings.html', bookings=bookings)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
         db.create_all()
    app.run(debug=True)
