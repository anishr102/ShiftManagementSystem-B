# Email Notification Setup

This feature automatically sends email reminders to employees 12 hours before their scheduled shift.

## Configuration

To enable email notifications, configure the following environment variables in your `.env` file:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

## Gmail Setup (Recommended)

If using Gmail:

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Go to Security > App Passwords
4. Generate a new app password
5. Use the app password as `SMTP_PASS`

## How It Works

- The system checks hourly for shifts starting in approximately 12 hours
- Employees receive an email with their shift details (date, time, shift name)
- Each employee-shift combination only receives one notification to prevent duplicates
- Notifications are tracked in the `shift_notifications` table

## Testing

To test the email functionality:

1. Ensure your SMTP credentials are correctly configured
2. Start the application
3. The scheduler will automatically run every hour
4. Check logs for email sending status

## Manual Trigger

You can manually trigger the email check by running:

```python
from app.backend.services.email_service import EmailService
EmailService.check_and_send_upcoming_shift_reminders()
```

## Troubleshooting

- **Emails not sending**: Check SMTP credentials and network connectivity
- **Duplicate emails**: The system prevents duplicates via the `shift_notifications` table
- **Scheduler not running**: Check application logs for "Email notification scheduler started"
