from flasgres import db
from flasgres.util.serialize import AlchemyJSON

class Usuario(db.Model, AlchemyJSON):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=True)
    pis = db.Column(db.String(14), nullable=True)

    endereco = db.relationship('Endereco',
        uselist=False, back_populates='usuario', cascade="all, delete-orphan"
    )

    def __repr__(self):
        return '<Usuario %r>' % self.nome

class Endereco(db.Model, AlchemyJSON):
    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(9), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    complemento = db.Column(db.String(255), nullable=True)
    municipio = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(255), nullable=True)
    pais = db.Column(db.String(255), nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', back_populates='endereco')

    def json(self, as_string=False):
        endereco_json = super().json(as_string)
        endereco_json.pop('usuario_id')
        endereco_json.pop('usuario')
        return endereco_json

    def __repr__(self):
        return '<Endereco %r, %r>' % (self.rua, self.numero)
