from app import db

class ModelMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))
    # Add other relevant fields here

    def __repr__(self):
        return f'<Model {self.name}>'
