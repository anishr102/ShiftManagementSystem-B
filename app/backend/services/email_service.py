from flask import current_app
from flask_mail import Message
from datetime import datetime, timedelta
from app.backend.extensions import db, mail
from app.backend.models.shift_notification import ShiftNotification
from app.backend.models.shift import ShiftAllocation


class EmailService:
    
    @staticmethod
    def send_shift_reminder(allocation):
        """Send email reminder to employee 12 hours before their shift"""
        try:
            employee = allocation.employee
            shift = allocation.shift
            user = employee.user
            
            if not user or not user.email:
                current_app.logger.warning(f"No email found for employee {employee.id}")
                return False
            
            # Check if notification already sent for this allocation
            existing_notification = ShiftNotification.query.filter_by(
                shift_allocation_id=allocation.id,
                notification_type='12_hours_before'
            ).first()
            
            if existing_notification:
                current_app.logger.info(f"Notification already sent for allocation {allocation.id}")
                return False
            
            # Create email message
            subject = f"Shift Reminder: {shift.name} Shift Tomorrow"
            
            shift_start_time = shift.start_time.strftime('%I:%M %p')
            shift_end_time = shift.end_time.strftime('%I:%M %p')
            shift_date = allocation.date.strftime('%A, %B %d, %Y')
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #333;">Shift Reminder</h2>
                <p>Dear {employee.first_name} {employee.last_name},</p>
                <p>This is a friendly reminder that you have an upcoming shift scheduled for tomorrow:</p>
                
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Shift:</strong> {shift.name}</p>
                    <p><strong>Date:</strong> {shift_date}</p>
                    <p><strong>Time:</strong> {shift_start_time} - {shift_end_time}</p>
                </div>
                
                <p>Please ensure you arrive on time and are prepared for your shift.</p>
                
                <p style="color: #666; font-size: 12px;">This is an automated message. Please do not reply.</p>
            </body>
            </html>
            """
            
            text_body = f"""
            Shift Reminder
            
            Dear {employee.first_name} {employee.last_name},
            
            This is a friendly reminder that you have an upcoming shift scheduled for tomorrow:
            
            Shift: {shift.name}
            Date: {shift_date}
            Time: {shift_start_time} - {shift_end_time}
            
            Please ensure you arrive on time and are prepared for your shift.
            
            This is an automated message. Please do not reply.
            """
            
            msg = Message(
                subject=subject,
                recipients=[user.email],
                html=html_body,
                body=text_body
            )
            
            # Send email
            mail.send(msg)
            
            # Record that notification was sent
            notification = ShiftNotification(
                shift_allocation_id=allocation.id,
                notification_type='12_hours_before'
            )
            db.session.add(notification)
            db.session.commit()
            
            current_app.logger.info(f"Shift reminder email sent to {user.email} for allocation {allocation.id}")
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send shift reminder email: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def check_and_send_upcoming_shift_reminders():
        """Check for shifts starting in 12 hours and send reminders"""
        try:
            now = datetime.utcnow()
            twelve_hours_later = now + timedelta(hours=12)
            
            # Get date component for comparison
            target_date = twelve_hours_later.date()
            
            # Find all shift allocations for the target date
            allocations = ShiftAllocation.query.filter_by(date=target_date).all()
            
            sent_count = 0
            for allocation in allocations:
                # Check if notification already sent
                existing = ShiftNotification.query.filter_by(
                    shift_allocation_id=allocation.id,
                    notification_type='12_hours_before'
                ).first()
                
                if not existing:
                    if EmailService.send_shift_reminder(allocation):
                        sent_count += 1
            
            current_app.logger.info(f"Shift reminder check completed. Sent {sent_count} reminders.")
            return sent_count
            
        except Exception as e:
            current_app.logger.error(f"Error in check_and_send_upcoming_shift_reminders: {str(e)}")
            return 0
