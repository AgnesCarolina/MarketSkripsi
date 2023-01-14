from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin

class DBarang (db.Model):
    barangID = db.Column(db.String(6), primary_key=True, nullable=False)
    namaBarang = db.Column(db.String(50), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    totalStok = db.Column(db.Integer, nullable=False, default=0)
    namaClass = db.Column(db.String(50), nullable=True)
    # barangJoinDtlBrng = db.relationship('DTransaksi', backref='dtansaksi', lazy=True)

    def __repr__(self):
        return f'dbarang({self.barangID}, {self.namaBarang}, {self.harga},{self.totalStok})'


class HTransaksi(db.Model):
    transID = db.Column(db.String(6), primary_key=True, nullable=False)
    tokoName = db.Column(db.String(6), nullable=True)
    kasirID = db.Column(db.String(6), db.ForeignKey('kasir.kasirID'), nullable=True)
    transDate = db.Column(db.String(12), nullable=False, default=datetime.utcnow())
    totalPayment = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'hTransaksi({self.transID}, {self.tokoName}, {self.kasirID}, {self.transDate}, {self.totalPayment})'

class DTransaksi(db.Model):
    transID = db.Column(db.String(6), db.ForeignKey('h_transaksi.transID'), primary_key=True, nullable=False)
    barangID = db.Column(db.String(6), db.ForeignKey('d_barang.barangID'), nullable=False)
    qtyPerBrg = db.Column(db.Integer, nullable=False)
    totalHargaPerBrg = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'dTransaksi({self.transID},{self.barangID},{self.qtyPerBrg},{self.totalPerBrg})'

class Laporan(db.Model):
    lapID = db.Column(db.String(6), primary_key=True, nullable=False)
    lapDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    status = db.Column(db.String(1), nullable=False, default='A') # A = Printed, I = Not-Printed

    def __repr__(self):
        return f'laporan({self.lapID},{self.lapDate},{self.status})'


@login_manager.user_loader
def load_user(user_id):
    return Kasir.query.get((user_id))

class Kasir(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    kasirID = db.Column(db.String(6), nullable=False)
    kName = db.Column(db.String(50), nullable=True)
    kAddress = db.Column(db.String(50), nullable=True)
    kPhone = db.Column(db.String(16), nullable=True)
    kEmail = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    
    @property
    def password(self):
        return self.password

    def check_password_correction():
        return True


# class hTransToLaporan(db.Model):
#     lapID = db.Column(db.String(6), db.ForeignKey('laporan.lapID'), nullable=False)
#     transID = db.Column(db.String(6),  db.ForeignKey('h_transaksi.transID'), nullable=False)
    
#     def __repr__(self):
#         return f'laporan()'
 