from app.backend.extensions import db
from datetime import datetime

class ShiftNotification(db.Model):
    __tablename__ = 'shift_notifications'

    id = db.Column(db.Integer, primary_key=True)
    shift_allocation_id = db.Column(db.Integer, db.ForeignKey('shift_allocations.id', ondelete='CASCADE'), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notification_type = db.Column(db.Enum('12_hours_before', name='notification_types'), nullable=False)

    # Unique constraint to prevent duplicate notifications for the same allocation
    __table_args__ = (
        db.UniqueConstraint('shift_allocation_id', 'notification_type', name='unique_allocation_notification'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'shift_allocation_id': self.shift_allocation_id,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'notification_type': self.notification_type
        }
