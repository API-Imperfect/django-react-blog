from allauth.account.adapter import DefaultAccountAdapter
from blog.settings import development


class CustomDefaultAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        context["activate_url"] = (
            development.ACTIVATE_EMAIL_URL
            + "/api/v1/registration/account-confirm-email/"
            + context["key"]
        )
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
