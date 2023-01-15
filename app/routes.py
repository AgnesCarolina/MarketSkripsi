from . import app, db
from .models import DBarang, HTransaksi, DTransaksi, Laporan, Kasir
from flask import render_template, request, redirect, url_for, flash
import uuid
import json

from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/item', methods=['GET', 'POST'])
def item_page():
    if request.method == "GET":
        allbarang = DBarang.query.all()
        baranglist = []
        for brng in allbarang:
            baranglist.append({'barangID': brng.barangID, 'namaBarang': brng.namaBarang, 'harga': brng.harga, 'totalStok': brng.totalStok})
        
        return render_template('dataProduct.html', allbarang=allbarang)

    if request.method == "POST":
        # Input Data to DB
        dt = request.get_json()
        # Check if each product is valid
        for product in dt:
            barang = DBarang(barangID= uuid.uuid4().hex[:6], namaBarang = product.get('name'), namaClass= product.get('class'), harga = product.get('price'), totalStok = product.get('qty'))
            db.session.add(barang)
        
        db.session.commit()

        return "Success"

@app.route('/market', methods=['GET', 'POST'])
def market_page():
    if request.method == "GET":
        # flash("Laoding...", category='info')
        return render_template('market.html', detected=[])

@app.route('/market/add',methods=['POST'])
def add_product():
    if request.method == "POST":
        # Input Data to DB
        dt = request.get_json()
        
        # Check if each product is valid
        baranglist = []
        for product in dt.get('predictions', []): 
            class_name = product.get('class')
            if not class_name:
                continue
            brng = DBarang.query.filter_by(namaClass=class_name).first() #knp first untuk simpen yg diambil dlm bentuk objek 
            # karena DBarang.query.filter_by(namaClass=class_name) bakal simpen array
            baranglist.append({'id': brng.barangID, 'name': brng.namaBarang, 'price': brng.harga, 'stock': brng.totalStok})
            #appen tuh buat nambahin

        return baranglist

@app.route('/market/confirm', methods=['POST'])
def confirm():
    if request.method == "POST":
        dt = request.get_json()
        # Get H Transaksi Data
        h_id = uuid.uuid4().hex[:6]
        htransaksi = HTransaksi(transID = h_id)
        db.session.add(htransaksi)        

        # Get D Transaksi Data
        total_harga = 0
        for pd in dt.get('items'):
            # if id not found than skip it
            pid = pd.get('id')
            if not pid:
                continue

            brng = DBarang.query.filter_by(barangID=pid).first()
            qty =  pd.get('qty', 1)
            price = brng.harga
            total = qty * price

            # Check if stock still exit
            if brng.totalStok < qty:
                continue

            # Decrease stock
            brng.totalStok = brng.totalStok - qty

            dtransaksi = DTransaksi(transID = h_id, barangID = pid, qtyPerBrg = qty, totalHargaPerBrg=total)
            total_harga = total_harga + total
            db.session.add(dtransaksi)

        htransaksi = HTransaksi.query.filter_by(transID=h_id).first()
        htransaksi.totalPayment = total_harga
        
        # db.session.merge(htransaksi)
        db.session.commit()

        return "Success"


@app.route ('/laporan', methods=['GET'])
def laporan_page():
    allLaporan = HTransaksi.query.all()
    laporlist = []
    for lapor in allLaporan:
        laporlist.append({'transID': lapor.transID, 'totalPayment': lapor.totalPayment, 'transDate': lapor.transDate})
        
    return render_template('laporan.html', allLaporan=allLaporan)


@app.route ('/detail_laporan/<string:transID>', methods=['GET'])
def d_laporan_page(transID):
    id = HTransaksi.query.filter_by(transID = transID).one()
    items = DTransaksi.query.filter_by(transID = id.transID)

    allLdetail = DTransaksi.query.all()
    dlaporlist = []
    for Dtrs in allLdetail:
        dlaporlist.append({'barangID': Dtrs.barangID, 'qtyPerBrg': Dtrs.qtyPerBrg, 'totalHargaPerBrg': Dtrs.totalHargaPerBrg,})
        
    return render_template('laporanD.html', id = id, items = items, allLdetail=allLdetail)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Kasir(kName=form.kName.data,
                              kAddress=form.kAddress.data,
                              kPhone=form.kPhone.data,
                              username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Kasir.query.filter_by(
            username=form.username.data).first()
        if attempted_user:
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again',
                  category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))