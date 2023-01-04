from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    # @property
    # def prettier_budget(self):
    #     if len(str(self.budget)) >= 4:
    #         return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
    #     else:
    #         return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    # def can_purchase(self, item_obj):
    #     return self.budget >= item_obj.totalPayment

    def can_sell(self, item_obj):
        return item_obj in self.items

class Item(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    # name = db.Column(db.String(length=30), nullable=False, unique=True)
    totalPayment = db.Column(db.Integer(), nullable=False)
    transDate = db.Column(db.String(12), nullable=False)
    # description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Item({self.name},{self.transDate},{self.totalPayment})',

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.totalPayment
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.totalPayment
        db.session.commit()


class dbarang (db.Model):
    barangID = db.Column(db.String(6), primary_key=True, nullable=False)
    namaBarang = db.Column(db.String(50), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    totalStok = db.Column(db.Integer, nullable=False)
    # barangJoinDtlBrng = db.relationship('DTransaksi', backref='dtansaksi', lazy=True)

    def __repr__(self):
        #return f'Barang({self.barangID})'
        return f'Barang({self.barangID}, {self.harga},{self.totalStok})'


class d_transaksi(db.Model):
    # transID = db.Column(db.String(6), primary_key=True, nullable=False)
    barangID = db.Column(db.String(6), primary_key=True, nullable=False)
    qtyPerBrng = db.Column(db.Integer, nullable=False)
    totalHargaPerBrng = db.Column(db.Integer, nullable=False)
    # totalHarga = db.Column(db.Float, nullable=False) ini perlu gk ya?? 
    # dtransToLaporan = db.relationship('Laporan', backref='laporan', lazy=True)

    def __repr__(self):
        return f'd_transaksi({self.barangID},{self.qtyPerBrng},{self.totalHargaPerBrng})'
        # {self.transID},


class trial(db.Model):
    idtrial = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(6))
    qty = db.Column(db.Integer)
    harga = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __repr__(self):
            return f'trial({self.nama},{self.qty},{self.harga})'