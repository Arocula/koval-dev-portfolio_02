from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-it'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# === МОДЕЛИ ===
class ConcretePrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.String(20), nullable=False)
    concrete_class = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class MortarPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class FineConcretePrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class ZBIPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

def init_db():
    with app.app_context():
        db.create_all()
        if ConcretePrice.query.count() == 0:
            # Начальные данные (сокращённо)
            for mark, cls, price in [('М-100','В-7,5',5900), ('М-150','В-10',6300), ('М-200','В-15',6800)]:
                db.session.add(ConcretePrice(mark=mark, concrete_class=cls, price=price))
            for mark, price in [('М-100',7400), ('М-150',8000)]:
                db.session.add(MortarPrice(mark=mark, price=price))
            for mark, price in [('М-100',6400), ('М-150',6900)]:
                db.session.add(FineConcretePrice(mark=mark, price=price))
            for name, price in [('КС-10-9',4000), ('КС-10-6',3500)]:
                db.session.add(ZBIPrice(name=name, price=price, category='rings'))
            for name, price in [('Садовый БР.100.30.6',330)]:
                db.session.add(ZBIPrice(name=name, price=price, category='borders'))
            db.session.commit()
            print("✅ БД создана")

# === ОСНОВНЫЕ МАРШРУТЫ ===
@app.route('/')
def index(): return render_template('index.html')

@app.route('/prices')
def prices():
    return render_template('price.html',
        concrete=ConcretePrice.query.all(),
        mortar=MortarPrice.query.all(),
        fine_concrete=FineConcretePrice.query.all(),
        rings=ZBIPrice.query.filter_by(category='rings').all(),
        borders=ZBIPrice.query.filter_by(category='borders').all())

@app.route('/about')
def about(): return render_template('about.html')
@app.route('/contacts')
def contacts(): return render_template('contacts.html')
@app.route('/privacy')
def privacy(): return render_template('privacy.html', now=datetime.now())

# === АДМИНКА ===
@app.route('/admin/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        flash('Неверный логин или пароль', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template('admin/dashboard.html', prices={
        'concrete': ConcretePrice.query.all(),
        'mortar': MortarPrice.query.all(),
        'fine_concrete': FineConcretePrice.query.all(),
        'rings': ZBIPrice.query.filter_by(category='rings').all(),
        'borders': ZBIPrice.query.filter_by(category='borders').all(),
    })

# === UPDATE ROUTES ===
@app.route('/admin/update_concrete', methods=['POST'])
def update_concrete():
    if not session.get('logged_in'): return redirect(url_for('login'))
    for id_, mark, cls, price in zip(request.form.getlist('id[]'), request.form.getlist('mark[]'), request.form.getlist('class[]'), request.form.getlist('price[]')):
        item = ConcretePrice.query.get(int(id_))
        if item: item.mark, item.concrete_class, item.price = mark, cls, int(price)
    db.session.commit()
    flash('Обновлено!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/update_mortar', methods=['POST'])
def update_mortar():
    if not session.get('logged_in'): return redirect(url_for('login'))
    for id_, mark, price in zip(request.form.getlist('id[]'), request.form.getlist('mark[]'), request.form.getlist('price[]')):
        item = MortarPrice.query.get(int(id_))
        if item: item.mark, item.price = mark, int(price)
    db.session.commit()
    flash('Обновлено!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/update_fine_concrete', methods=['POST'])
def update_fine_concrete():
    if not session.get('logged_in'): return redirect(url_for('login'))
    for id_, mark, price in zip(request.form.getlist('id[]'), request.form.getlist('mark[]'), request.form.getlist('price[]')):
        item = FineConcretePrice.query.get(int(id_))
        if item: item.mark, item.price = mark, int(price)
    db.session.commit()
    flash('Обновлено!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/update_rings', methods=['POST'])
def update_rings():
    if not session.get('logged_in'): return redirect(url_for('login'))
    for id_, name, price in zip(request.form.getlist('id[]'), request.form.getlist('name[]'), request.form.getlist('price[]')):
        item = ZBIPrice.query.get(int(id_))
        if item: item.name, item.price = name, int(price)
    db.session.commit()
    flash('Кольца обновлены!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/update_borders', methods=['POST'])
def update_borders():
    if not session.get('logged_in'): return redirect(url_for('login'))
    for id_, name, price in zip(request.form.getlist('id[]'), request.form.getlist('name[]'), request.form.getlist('price[]')):
        item = ZBIPrice.query.get(int(id_))
        if item: item.name, item.price = name, int(price)
    db.session.commit()
    flash('Бордюры обновлены!', 'success')
    return redirect(url_for('dashboard'))

# === ADD ROUTES ===
@app.route('/admin/add_concrete', methods=['POST'])
def add_concrete():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.form.get('mark') and request.form.get('class') and request.form.get('price'):
        db.session.add(ConcretePrice(mark=request.form.get('mark'), concrete_class=request.form.get('class'), price=int(request.form.get('price'))))
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/add_mortar', methods=['POST'])
def add_mortar():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.form.get('mark') and request.form.get('price'):
        db.session.add(MortarPrice(mark=request.form.get('mark'), price=int(request.form.get('price'))))
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/add_fine_concrete', methods=['POST'])
def add_fine_concrete():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.form.get('mark') and request.form.get('price'):
        db.session.add(FineConcretePrice(mark=request.form.get('mark'), price=int(request.form.get('price'))))
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/add_ring', methods=['POST'])
def add_ring():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.form.get('name') and request.form.get('price'):
        db.session.add(ZBIPrice(name=request.form.get('name'), price=int(request.form.get('price')), category='rings'))
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/add_border', methods=['POST'])
def add_border():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.form.get('name') and request.form.get('price'):
        db.session.add(ZBIPrice(name=request.form.get('name'), price=int(request.form.get('price')), category='borders'))
        db.session.commit()
    return redirect(url_for('dashboard'))

# === DELETE ROUTES ===
@app.route('/admin/delete_concrete/<int:id>', methods=['POST'])
def delete_concrete(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    item = ConcretePrice.query.get_or_404(id)
    db.session.delete(item); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_mortar/<int:id>', methods=['POST'])
def delete_mortar(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    item = MortarPrice.query.get_or_404(id)
    db.session.delete(item); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_fine_concrete/<int:id>', methods=['POST'])
def delete_fine_concrete(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    item = FineConcretePrice.query.get_or_404(id)
    db.session.delete(item); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_ring/<int:id>', methods=['POST'])
def delete_ring(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    item = ZBIPrice.query.get_or_404(id)
    db.session.delete(item); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_border/<int:id>', methods=['POST'])
def delete_border(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    item = ZBIPrice.query.get_or_404(id)
    db.session.delete(item); db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    print("🚀 Запуск: http://localhost:5000 | Админка: /admin/login")
    app.run(debug=True, port=5000)