from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, redirect

from control_panel.forms import NewsletterCreationForm
from plants_app.config import pagination
from main.models import Newsletter


# # @login_required(login_url='/accounts/login/')
# @staff_member_required
# def control_newsletter(request):
#     form = NewsletterCreationForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save()
#         messages.success(request, 'Newsletter has been successfully created.')
#         newsletter = Newsletter.objects.get(id=instance.id)
#         if newsletter.status == "Published":
#             subject = f"Newsletter from Watering Plant App: {newsletter.subject}"
#             body = newsletter.body
#             from_email = settings.EMAIL_HOST_USER
#             for email in newsletter.email.all():
#                 send_mail(subject=subject, message=body, from_email=from_email,
#                           recipient_list=[email], fail_silently=True)
#
#     form = NewsletterCreationForm()
#     context = {'form': form}
#     template = 'control_panel/control_newsletter.html'
#     return render(request, template, context)

@staff_member_required
def control_newsletter(request):
    form = NewsletterCreationForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        messages.success(request, 'Newsletter has been successfully created.')
        newsletter = Newsletter.objects.get(id=instance.id)

        if newsletter.status == "Published":
            subject = f"New newsletter from Watering Plant App: {newsletter.subject}"
            body = {'body': newsletter.body}
            plaintext = template.loader.get_template('control_panel/newsletter_form.txt')
            htmltemp = template.loader.get_template('control_panel/newsletter_form.html')
            from_email = settings.EMAIL_HOST_USER
            text_content = plaintext.render(body)
            html_content = htmltemp.render(body)
            for email in newsletter.email.all():
                try:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [email],
                                                 headers={'Reply-To': 'YOUR_GMAIL'})
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            messages.success(request, 'New newsletter was sent successfully.')
            return redirect('control_panel:control_newsletter')
    else:
        form = NewsletterCreationForm()

    return render(request, 'control_panel/control_newsletter.html', {'form': form})


@staff_member_required
def control_newsletter_list(request):
    newsletters = Newsletter.objects.all()
    pages = pagination(request, newsletters, 15)

    context = {'control_newsletter_list': pages,
               'page_obj': pages}
    return render(request, 'control_panel/control_newsletter_list.html', context)


# def control_newsletter_detail(request, pk):
#     newsletter = get_object_or_404(Newsletter, pk=pk)
#
#     context = {
#         'newsletter': newsletter
#     }
#     template = 'control_panel/control_newsletter_detail.html'
#     return render(request, template, context)


def control_newsletter_edit(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save()
            if newsletter.status == 'Published':
                subject = f"New newsletter from Watering Plant App: {newsletter.subject}"
                body = {'body': newsletter.body}
                plaintext = template.loader.get_template('control_panel/newsletter_form.txt')
                htmltemp = template.loader.get_template('control_panel/newsletter_form.html')
                from_email = settings.EMAIL_HOST_USER
                text_content = plaintext.render(body)
                html_content = htmltemp.render(body)

                for email in newsletter.email.all():
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [email],
                                                     headers={'Reply-To': 'YOUR_GMAIL'})
                        msg.attach_alternative(html_content, 'text/html')
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

            messages.success(request, "Newsletter has been edited successfully!")
            return redirect('control_panel:control_newsletter_list')
    else:
        form = NewsletterCreationForm(instance=newsletter)


    return render(request, 'control_panel/control_newsletter.html', {'form': form})


def control_newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, 'Newsletter has been deleted.')
        return redirect('control_panel:control_newsletter_list')

    return render(request, 'control_panel/control_newsletter_delete.html', {'newsletter': newsletter})
