from flask import render_template, request, redirect, url_for, flash
import functools

from . import app, db
from .models import DBarang, HTransaksi, DTransaksi, Laporan, Kasir
from .forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

import uuid
import json

@app.route('/')
def home_page():
    return render_template('home.html')


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
@login_required
def market_page():
    if request.method == "GET":
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
            brng = DBarang.query.filter_by(namaClass=class_name).first()
            baranglist.append({'id': brng.barangID, 'name': brng.namaBarang, 'price': brng.harga, 'stock': brng.totalStok})

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

            dtransaksi = DTransaksi(transID = h_id, barangID = pid, qtyPerBrg = qty, totalHargaPerBrg=total)
            total_harga = total_harga + total
            db.session.add(dtransaksi)

        htransaksi = HTransaksi.query.filter_by(transID=h_id).first()
        htransaksi.totalPayment = total_harga
        
        # db.session.merge(htransaksi)
        db.session.commit()

        return "Success"

