import os
from django.core.mail import send_mail
from django.conf import settings
# from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage


SITE_URL = settings.SITE_URL
ASSET_DIR = os.path.join(settings.BASE_DIR, 'public')


def send(to, subject, message, from_email=settings.DEFAULT_MAIL_FROM):

    send_mail(
        subject,
        message,
        from_email,
        to,
        fail_silently=False,
    )


# helpers
def send_with_template(to, subject, template, context,
                       from_email=settings.DEFAULT_MAIL_FROM):

    if not isinstance(to, list):
        to = [to]
    message = get_template(template).render(context)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        print(e)

def send_welcome(user):
    template = "email/welcome.html"
    to = user.email
    from_email = settings.DEFAULT_MAIL_FROM
    #from_email = invited_by.email
    f = open(os.path.join(ASSET_DIR, 'index.styles.css'), 'r')
    style = f.read()
    f.close()
    context = {
        'user': user,
        'style': style,
        'welcome_url': SITE_URL,
    }
    subject = "Welcome to In The Cloud Contracts"

    return send_with_template(to, subject, template, context, from_email)


def send_invite(invite):
    template = 'email/invite_user.html'
    to = invite.email
    invited_by = invite.invited_by
    from_email = settings.DEFAULT_MAIL_FROM
    #from_email = invited_by.email
    f = open(os.path.join(ASSET_DIR, 'index.styles.css'), 'r')
    style = f.read()
    f.close()
    context = {
        'invite': invite,
        'invited_by': invite.invited_by,
        'style': style,
        'site_url': SITE_URL,
        'invite_url': "%s/register?invite_code=%s" % (SITE_URL, invite.invite_code)
    }
    subject = "You're invited to InTheCloudContracts"

    #subject = '%s %s has invited you to ITCC' % (
    #    invited_by.first_name, invited_by.last_name)

    return send_with_template(to, subject, template, context, from_email)


def send_invite_request(admin, request):
    template = 'email/invite_request_user.html'
    to = admin.email
    from_email = settings.DEFAULT_MAIL_FROM

    context = {
        'admin': admin,
        'request': request,
        'site_url': SITE_URL,
    }
    subject = '%s %s has requested to join the %s organization on ITCC' % (
        request.user.first_name, request.user.last_name,
        request.organization.name)

    return send_with_template([to], subject, template, context, from_email)


def send_welcome_email(user):
    """send a welcome email to the customer with a link to their profile info"""
    pass
