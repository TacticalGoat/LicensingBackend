from app import db
import random
import string

def generate_id():
    return ''.join(
        random.choice(string.ascii_lowercase
                      + string.ascii_uppercase
                      + string.digits
                      + "_" + "-")
        for _ in range(16)
    )

class Product(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_id)
    name = db.Column(db.String)
    platform = db.Column(db.String)
    version = db.Column(db.String)
    licenses = db.relationship("License", back_populates="product")

    __table_args__ = (
        db.UniqueConstraint("name", "platform", "version"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "platform": self.platform,
            "version": self.version
        }