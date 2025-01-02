from datetime import datetime
from ..database import db

class Domain(db.Model):
    """
    Domain model for storing domain-related information.
    """
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    domain_name = db.Column(db.String(255), unique=True, nullable=False)
    registered = db.Column(db.Boolean, default=False)
    ssl_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='domains')

    def __init__(self, user_id, domain_name, registered=False, ssl_enabled=False):
        self.user_id = user_id
        self.domain_name = domain_name
        self.registered = registered
        self.ssl_enabled = ssl_enabled

    def to_dict(self):
        """
        Convert the domain object to a dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'domain_name': self.domain_name,
            'registered': self.registered,
            'ssl_enabled': self.ssl_enabled,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f"<Domain {self.domain_name}>"
