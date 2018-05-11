from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^reservefund/', views.handleReverseFund, name='handle_reverseFund'),
    url(r'^payment/', views.handlePayment, name='handle_payment'),
    url(r'^reimbursement/', views.handleReimbursement, name='handle_reimbursment'),
    url(r'^approve/', views.superLoing, name='approve'),
    url(r'^reverseData/', views.getReverseFund, name='get_reverse'),
    url(r'^confirmR/', views.confirmReverseFund, name='confirm_reverse'),
    url(r'^viewR/', views.infoReverseFund, name='view_reverse'),
    url(r'^paymentData/', views.getPayment, name='get_payment'),
    url(r'^confirmP/', views.confirmPayment, name='confirm_payment'),
    url(r'^viewP/', views.infoPayment, name='view_payment'),
    url(r'^rbData/', views.getRb, name='get_rb'),
    url(r'^confirmRb/', views.confirmRb, name='confirm_rb'),
    url(r'^viewRbP/', views.infoRb, name='view_rb'),
]
