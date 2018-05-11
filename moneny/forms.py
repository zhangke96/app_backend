from django import forms

class ReserveFundForm(forms.Form):
    applicant = forms.CharField()
    department = forms.CharField()
    detail = forms.CharField()
    moneny = forms.CharField()
    useDate = forms.DateField()
    returnDate = forms.DateField()
    cashier = forms.CharField()
    note = forms.CharField()

class PaymentForm(forms.Form):
    detail = forms.CharField()
    moneny = forms.CharField()
    type = forms.CharField()
    date = forms.DateField()
    payTo = forms.CharField()
    bank = forms.CharField()
    account = forms.CharField()

class ReimbursementForm(forms.Form):
    moneny = forms.CharField()
    type = forms.CharField()
    detail = forms.CharField()

class LoginForm(forms.Form):
    phone = forms.CharField(label="手机号码", max_length=11, required=True)
    password = forms.CharField(label="密码", max_length=20, required=True)

class ConfirmReserverFundForm(forms.Form):
    id = forms.IntegerField(required=True)
    confirm = forms.BooleanField(required=False)

