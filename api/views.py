from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ContractForm as ContractForm, DutyFormSet
from .models import Contracts_completed
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import logging
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

def contract_form(request):
    contract = Contracts_completed()

    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        duty_formset = DutyFormSet(request.POST, instance=contract)

        if form.is_valid() and duty_formset.is_valid():
            form.save()
            duty_formset.save()
            return redirect('view_contract', contract_id=contract.id)
        else:
            print(form.errors)
            print(duty_formset.errors)
    else:
        form = ContractForm(instance=contract)
        duty_formset = DutyFormSet(instance=contract)

    return render(request, 'contract_form.html', {
        'form': form,
        'duty_formset': duty_formset,
    })

def view_contract(request, contract_id):
    contract = get_object_or_404(Contracts_completed, id=contract_id)
    return render(request, 'view_contract.html', {'contract': contract})

def edit_contract(request, contract_id):
    contract = get_object_or_404(Contracts_completed, id=contract_id)
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        duty_formset = DutyFormSet(request.POST, instance=contract)

        if form.is_valid() and duty_formset.is_valid():
            form.save()
            duty_formset.save()
            return redirect('view_contract', contract_id=contract.id)
    else:
        form = ContractForm(instance=contract)
        duty_formset = DutyFormSet(instance=contract)

    return render(request, 'edit_contract.html', {'form': form, 'duty_formset': duty_formset, 'contract': contract})

def download_contract(request, contract_id):
    contract = get_object_or_404(Contracts_completed, id=contract_id)
    html_string = render_to_string('contract_template.html', {'contract': contract})
    result = BytesIO()
    pdf = pisa.CreatePDF(html_string, dest=result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="contract_{contract.id}.pdf"'
        return response
    else:
        logger.error("Error generating PDF: %s", pdf.err)
        return HttpResponse("Error generating PDF")

def show_view(request, contract_id):
    contract = get_object_or_404(Contracts_completed, id=contract_id)
    return render(request, 'contract_template.html', {'contract': contract})

def contact_view(request):
    return render(request, 'contact.html')

def internship_agreement(request):
    return render(request, 'connect.html')

def send_contract_to_supervisor(request, contract_id):
    contract = get_object_or_404(Contracts_completed, id=contract_id)
    context_data = {
        'contract': contract
    }
    html_content = render_to_string('send.html', context_data)
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), pdf_buffer)
    if pisa_status.err:
        return JsonResponse({'success': False, 'message': 'Failed to create PDF'})

    pdf_buffer.seek(0)

    email = EmailMessage(
        subject="Contract for Your Review and Signature",
        body="Please find the attached contract for review and signature.",
        from_email=settings.EMAIL_HOST_USER,
        to=[contract.supervisor_email]
    )

    email.attach('contract.pdf', pdf_buffer.read(), 'application/pdf')

    try:
        email.send()
        return render(request, 'view_contract.html', {'contract': contract})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
    
def send_contract_to_ceo(request, contract_id):
    contract = get_object_or_404(Contracts_completed, id=contract_id)
    context_data = {
        'contract': contract
    }
    html_content = render_to_string('contract_template.html', context_data)
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), pdf_buffer)
    if pisa_status.err:
        return JsonResponse({'success': False, 'message': 'Failed to create PDF'})

    pdf_buffer.seek(0)

    email = EmailMessage(
        subject="Contract for Your Review and Signature",
        body="Please find the attached contract for review and signature.",
        from_email=settings.EMAIL_HOST_USER,
        to=['craniuminvestments@gmail.com']
    )

    email.attach('contract.pdf', pdf_buffer.read(), 'application/pdf')

    try:
        email.send()
        return render(request, 'view_contract.html', {'contract': contract})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})