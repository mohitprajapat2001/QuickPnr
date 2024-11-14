"""Mail Services"""

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from utils.utils import get_model
from django_extensions.db.models import ActivatorModel
from utils.constants import EmailTemplates
from django.utils.timezone import now, timedelta
from logging import Logger

logger = Logger(__name__)
EmailTemplate = get_model("quickpnr", "EmailTemplate")
Otp = get_model(app_name="users", model_name="Otp")


class EmailService:
    """Email Service Class to Handle Mail"""

    @staticmethod
    def get_template(email_type: str):
        """Returns Email Template"""
        try:
            return EmailTemplate.objects.get(
                status=ActivatorModel.ACTIVE_STATUS, email_type=email_type
            )
        except EmailTemplate.DoesNotExist:
            return None

    @staticmethod
    def send_mail(
        subject: str,
        body: str,
        is_html: bool,
        to_email: list,
        template: str | None = None,
    ):
        """This function will be used to send email using celery task based on email template"""
        sender = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            subject=subject, from_email=sender, to=to_email, body=body
        )
        if is_html:
            msg.attach_alternative(template, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"Email Send Successfully : Subject: {subject}")
        return f"Email Send Successfully : Subject: {subject}"

    def registration_mail(self, user):
        """Sends a registration email to the specified user."""
        template = self.get_template(email_type=EmailTemplates.REGISTRED_SUCCESSFULLY)
        return self.send_mail(
            template.subject,
            template.body.format(username=user.username),
            template.is_html,
            [user.email],
            template.template,
        )

    def verify_email(self, user):
        """Send a Verification email to Specific User"""
        template = self.get_template(email_type=EmailTemplates.VERIFY_EMAIL)
        try:
            Otp.objects.get(user=user).delete()
        except Otp.DoesNotExist:
            pass
        otp, created = Otp.objects.get_or_create(
            user=user, expiry=now() + timedelta(minutes=10)
        )
        return self.send_mail(
            template.subject,
            template.body.format(
                otp=otp.otp, expiry=otp.expiry.strftime("%B %d %Y, %H:%M %p %Z")
            ),
            template.is_html,
            [user.email],
            template.template.format(
                otp=otp.otp, expiry=otp.expiry.strftime("%B %d %Y, %H:%M %p %Z")
            ),
        )

    def pnr_status_mail(self, user, pnr_detail):
        """Sends PNR Status Details to User's Email Address"""
        template = self.get_template(email_type=EmailTemplates.PNR_DETAILS)
        passenger_details = "\n".join(
            [
                f"""
 <ul
                                          style="
                                            list-style: none;
                                            padding: 0;
                                            margin: 0;
                                            display: flex;
                                            justify-content: space-between;
                                            background-color: #e0e0e0;
                                            border-radius: 8px;
                                            padding: 8px;
                                          "
                                        >
                                          <li
                                            style="
                                              margin: 0 8px;
                                              font-size: 14px;
                                              font-weight: bold;
                                            "
                                          >
                                            Name: {passenger['name']}
                                          </li>
                                          <li
                                            style="
                                              margin: 0 8px;
                                              font-size: 14px;
                                            "
                                          >
                                            Booking:
                                            {passenger['booking_status']}
                                          </li>
                                          <li
                                            style="
                                              margin: 0 8px;
                                              font-size: 14px;
                                            "
                                          >
                                            Current:
                                            {passenger['current_status']}
                                          </li>
                                        </ul>"""
                for passenger in pnr_detail["passengers_details"]
            ]
        )
        return (
            self.send_mail(
                template.subject,
                template.body,
                template.is_html,
                [user.email],
                template.template.format(
                    pnr=pnr_detail["pnr"],
                    train_number=pnr_detail["train_number"],
                    train_name=pnr_detail["train_name"],
                    reserved_class=pnr_detail["reserved_class"],
                    boarding_date=pnr_detail["boarding_date"][0:10],
                    reserved_from=pnr_detail["reserved_from"],
                    reserved_to=pnr_detail["reserved_to"],
                    boarding_point=pnr_detail["boarding_point"],
                    passengers_details=passenger_details,
                    fare=pnr_detail["fare"],
                    remark=(
                        pnr_detail["remark"]
                        if pnr_detail["remark"] is not None
                        else "No remarks"
                    ),
                    train_status=(
                        pnr_detail["train_status"]
                        if pnr_detail["train_status"]
                        else "Status not available"
                    ),
                    charting_status=pnr_detail["charting_status"],
                ),
            ),
        )

    def reset_password_otp(self, user):
        """Generates reset password otp to user's email address"""
        template = self.get_template(email_type=EmailTemplates.PASSWORD_RESET)
        try:
            otp = Otp.objects.get(user=user).delete()
        except Otp.DoesNotExist:
            pass
        otp, created = Otp.objects.get_or_create(
            user=user, expiry=now() + timedelta(minutes=10)
        )
        return self.send_mail(
            template.subject,
            template.body.format(
                otp=otp.otp, expiry=otp.expiry.strftime("%B %d %Y, %H:%M %p %Z")
            ),
            template.is_html,
            [user.email],
            template.template.format(
                otp=otp.otp, expiry=otp.expiry.strftime("%B %d %Y, %H:%M %p %Z")
            ),
        )

    def reset_password_done(self, user):
        """Sends a password reset done email to the specified user."""
        template = self.get_template(email_type=EmailTemplates.PASSWORD_RESET_DONE)
        return self.send_mail(
            template.subject,
            template.body.format(username=user.username),
            template.is_html,
            [user.email],
            template.template,
        )
