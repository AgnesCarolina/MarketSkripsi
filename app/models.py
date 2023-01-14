from . import db
from datetime import datetime

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
    status = db.Column(db.String(1), nullable=False, default='I') # A = Printed, I = Not-Printed

    def __repr__(self):
        return f'laporan({self.lapID},{self.lapDate},{self.status})'

class Kasir(db.Model):
    kasirID = db.Column(db.String(6), primary_key=True, nullable=False)
    kName = db.Column(db.String(50), nullable=False)
    kAddress = db.Column(db.String(50), nullable=False)
    kPhone = db.Column(db.String(16), nullable=False)
    kEmail = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    
    @property
    def password(self):
        return self.password


# class hTransToLaporan(db.Model):
#     lapID = db.Column(db.String(6), db.ForeignKey('laporan.lapID'), nullable=False)
#     transID = db.Column(db.String(6),  db.ForeignKey('h_transaksi.transID'), nullable=False)
    
#     def __repr__(self):
#         return f'laporan()'
 