from django.shortcuts import render
from auth_system.views import check_login
from django.http import HttpResponse
from django.contrib import auth
from .forms import *
from .models import *
import json
import datetime
import pdb

def check_super_login(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return HttpResponse("", status=401)
        else:
            if not args[0].user.is_admin:
                return HttpResponse("", status=401)
            else:
                return func(*args, **kwargs)
    return wrapper

@check_login
def handleReverseFund(request):
    """
    处理用户的备用金申请请求
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ReserveFundForm(request.POST)
        if form.is_valid():
            try:
                ReserveFund.objects.create(user=request.user,
                                           applicant=form.cleaned_data['applicant'],
                                           department=form.cleaned_data['department'],
                                           detail=form.cleaned_data['detail'],
                                           moneny=form.cleaned_data['moneny'],
                                           useDate=form.cleaned_data['useDate'],
                                           returnDate=form.cleaned_data['returnDate'],
                                           cashier=form.cleaned_data['cashier'],
                                           note=form.cleaned_data['note'])
            except:
                return HttpResponse("FAIL")
            return HttpResponse("SUCCESS")
    return HttpResponse("FAIL")

@check_login
def handlePayment(request):
    """
    处理付款申请
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                Payment.objects.create(user=request.user,
                                       detail=form.cleaned_data['detail'],
                                       moneny=form.cleaned_data['moneny'],
                                       payType=form.cleaned_data['type'],
                                       date=form.cleaned_data['date'],
                                       payTo=form.cleaned_data['payTo'],
                                       bank=form.cleaned_data['bank'],
                                       account=form.cleaned_data['account'])
            except:
                return HttpResponse("FAIL")
            return HttpResponse("SUCCESS")
    return HttpResponse("FAIL")

@check_login
def handleReimbursement(request):
    """
    处理报销申请
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ReimbursementForm(request.POST)
        if form.is_valid():
            try:
                Reimbursement.objects.create(user=request.user,
                                             moneny=form.cleaned_data['moneny'],
                                             type=form.cleaned_data['type'],
                                             detail=form.cleaned_data['detail'])
            except:
                return HttpResponse("FAIL")
            return HttpResponse("SUCCESS")
    return HttpResponse("FAIL")

def superLoing(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['phone'],
                                     password=form.cleaned_data['password'])
        if user:
            auth.login(request, user)
            if user.is_admin:
                return render(request, 'moneny/approve.html')
            else:
                return HttpResponse("只提供特定用户进行申请批准操作")
    else:
        if request.user.is_authenticated:
            if request.user.is_admin:
                return render(request, 'moneny/approve.html')
            else:
                return HttpResponse("只提供特定用户进行申请批准操作")
        else:
            return render(request, 'moneny/login.html')

@check_super_login
def getReverseFund(request):
    offset = None
    limit = None
    try:
        offset = int(request.GET['offset'])
        limit = int(request.GET['limit'])
    except:
        return HttpResponse()
    funds = ReserveFund.objects.all()[offset: offset + limit]
    json_data = {}
    records = []
    json_data['total'] = funds.count()
    for fund in funds:
        status = 0
        if fund.handleTime:
            status = 1
        record = {'id':str(fund.id)+'-'+str(status), 'applicant':fund.applicant, 'department':fund.department,
                  'detail':fund.detail, 'moneny':fund.moneny, 'useDate':fund.useDate.strftime('%Y-%m-%d %X'),
                  'returnDate':fund.returnDate.strftime('%Y-%m-%d'), 'cashier':fund.cashier, 'note':fund.note}
        records.append(record)
    json_data['rows'] = records
    return HttpResponse(json.dumps(json_data))

@check_super_login
def confirmReverseFund(request):
    if request.method == 'POST':
        form = ConfirmReserverFundForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            apply = None
            try:
                apply = ReserveFund.objects.get(id=id)
            except:
                return HttpResponse()
            if form.cleaned_data['confirm']:  # 审核通过
                apply.result = True
            else:
                apply.result = False
            apply.handleTime = datetime.datetime.now()
            apply.approver = request.user
            apply.save()
            return HttpResponse(1)
        else:
            return HttpResponse()
    return HttpResponse()

@check_super_login
def infoReverseFund(request):
    if request.method == 'GET':
        id = None
        try:
            id = request.GET['id']
        except:
            return HttpResponse()
        apply = None
        try:
            apply = ReserveFund.objects.get(id=id)
        except:
            return HttpResponse()
        if apply.handleTime:
            return HttpResponse(json.dumps({'time':apply.handleTime.strftime('%Y-%m-%d %X'),
                                            'user': apply.approver.get_full_name(),
                                            'result': apply.result}))
    return HttpResponse()

@check_super_login
def getPayment(request):
    offset = None
    limit = None
    try:
        offset = int(request.GET['offset'])
        limit = int(request.GET['limit'])
    except:
        return HttpResponse()
    payments = Payment.objects.all()[offset: offset + limit]
    json_data = {}
    records = []
    json_data['total'] = payments.count()
    for payment in payments:
        status = 0
        if payment.handleTime:
            status = 1
        record = {'id':str(payment.id)+'-'+str(status), 'detail':payment.detail, 'moneny':payment.moneny,
                  'payType':payment.payType, 'date':payment.date.strftime('%Y-%m-%d'),
                  'payTo':payment.payTo, 'bank':payment.bank, 'account':payment.account}
        records.append(record)
    json_data['rows'] = records
    return HttpResponse(json.dumps(json_data))

@check_super_login
def confirmPayment(request):
    if request.method == 'POST':
        form = ConfirmReserverFundForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            apply = None
            try:
                apply = Payment.objects.get(id=id)
            except:
                return HttpResponse()
            if form.cleaned_data['confirm']:  # 审核通过
                apply.result = True
            else:
                apply.result = False
            apply.handleTime = datetime.datetime.now()
            apply.approver = request.user
            apply.save()
            return HttpResponse(1)
        else:
            return HttpResponse()
    return HttpResponse()

@check_super_login
def infoPayment(request):
    if request.method == 'GET':
        id = None
        try:
            id = request.GET['id']
        except:
            return HttpResponse()
        apply = None
        try:
            apply = Payment.objects.get(id=id)
        except:
            return HttpResponse()
        if apply.handleTime:
            return HttpResponse(json.dumps({'time':apply.handleTime.strftime('%Y-%m-%d %X'),
                                            'user': apply.approver.get_full_name(),
                                            'result': apply.result}))
    return HttpResponse()

@check_super_login
def getRb(request):
    offset = None
    limit = None
    try:
        offset = int(request.GET['offset'])
        limit = int(request.GET['limit'])
    except:
        return HttpResponse()
    rbs = Reimbursement.objects.all()[offset: offset + limit]
    json_data = {}
    records = []
    json_data['total'] = rbs.count()
    for rb in rbs:
        status = 0
        if rb.handleTime:
            status = 1
        record = {'id':str(rb.id)+'-'+str(status), 'moneny':rb.moneny,
                  'type':rb.type, 'detail':rb.detail}
        records.append(record)
    json_data['rows'] = records
    return HttpResponse(json.dumps(json_data))

@check_super_login
def confirmRb(request):
    if request.method == 'POST':
        form = ConfirmReserverFundForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            apply = None
            try:
                apply = Reimbursement.objects.get(id=id)
            except:
                return HttpResponse()
            if form.cleaned_data['confirm']:  # 审核通过
                apply.result = True
            else:
                apply.result = False
            apply.handleTime = datetime.datetime.now()
            apply.approver = request.user
            apply.save()
            return HttpResponse(1)
        else:
            return HttpResponse()
    return HttpResponse()

@check_super_login
def infoRb(request):
    if request.method == 'GET':
        id = None
        try:
            id = request.GET['id']
        except:
            return HttpResponse()
        apply = None
        try:
            apply = Reimbursement.objects.get(id=id)
        except:
            return HttpResponse()
        if apply.handleTime:
            return HttpResponse(json.dumps({'time':apply.handleTime.strftime('%Y-%m-%d %X'),
                                            'user': apply.approver.get_full_name(),
                                            'result': apply.result}))
    return HttpResponse()