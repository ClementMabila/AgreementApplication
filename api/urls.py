from django.urls import path
from .views import contract_form, view_contract, send_contract_to_ceo, send_contract_to_supervisor, internship_agreement, contact_view, edit_contract, download_contract, show_view

urlpatterns = [
    path('contract-form/', contract_form, name='contract_form'),
    path('contract/<int:contract_id>/', view_contract, name='view_contract'),
    path('contract/<int:contract_id>/edit/', edit_contract, name='edit_contract'),
    path('contract/<int:contract_id>/download/', download_contract, name='download_contract'),
    path('contract-show/<int:contract_id>/', show_view, name='show'),
    path('contact/', contact_view, name='contact'),
    path('', internship_agreement, name='internship_agreement'),
    path('send-contract-to-supervisor/<int:contract_id>/', send_contract_to_supervisor, name='send_contract_to_supervisor'),
    path('send-contract-to-ceo/<int:contract_id>/', send_contract_to_ceo, name='send_contract_to_ceo'),
]
