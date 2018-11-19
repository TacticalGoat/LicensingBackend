from app import db
from .product import Product
from .user import User
import random
import string

def generate_license_id():
    return ''.join(
        random.choice(string.ascii_lowercase
                      + string.ascii_uppercase
                      + string.digits
                      + "_" + "-")
        for _ in range(16)
    )


class License(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_license_id)
    account_number = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user_email = db.Column(db.String, db.ForeignKey("user.email"))
    user = db.relationship("User", back_populates="licenses")
    product_id = db.Column(db.String, db.ForeignKey("product.id"))
    product = db.relationship("Product", back_populates="licenses")

    __table_args__ = (
        db.UniqueConstraint("user_email", "product_id", "account_number"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "account_number": self.account_number,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "user": self.user.to_dict(),
            "product": self.product.to_dict()
        }