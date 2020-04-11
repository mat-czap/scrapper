from scrapper import db

class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"link: {self.link}"

