from django.db import models
from auth_system.models import MyUser

class ReserveFund(models.Model):
    """
    备用金申请
    """
    id = models.AutoField(primary_key=True)
    applyTime = models.DateTimeField(auto_now_add=True)  # 申请时间
    user = models.ForeignKey(MyUser, related_name='appled_ReserveFund', null=False, on_delete=models.PROTECT)
    applicant = models.TextField("申请人", null=False)
    department = models.TextField("部门", null=False)
    detail = models.TextField("申请事由", null=False)
    moneny = models.TextField("申请金额", null=False)
    useDate = models.DateField("使用日期", null=False)
    returnDate = models.DateField("归还日期", null=False)
    cashier = models.TextField("出纳", null=False)
    note = models.TextField("备注", null=False)
    approver = models.ForeignKey(MyUser, related_name='approved_ReserveFund', null=True, on_delete=models.PROTECT)
    result = models.BooleanField("备用金申请是否通过", default=False)
    handleTime = models.DateTimeField(null=True)  # 审核时间

class Payment(models.Model):
    """
    付款申请
    """
    id = models.AutoField(primary_key=True)
    applyTime = models.DateTimeField(auto_now_add=True)  # 申请时间
    user = models.ForeignKey(MyUser, related_name='appled_Payment', null=False, on_delete=models.PROTECT)
    detail = models.TextField("付款事由", null=False)
    moneny = models.TextField("付款总额", null=False)
    payType = models.TextField("付款方式", null=False)
    date = models.DateField("支付日期", null=False)
    payTo = models.TextField("支付对象", null=False)
    bank = models.TextField("开户行", null=False)
    account = models.TextField("银行账户", null=False)
    approver = models.ForeignKey(MyUser, related_name='approved_Payment', null=True, on_delete=models.PROTECT)
    result = models.BooleanField("付款申请是否通过", default=False)
    handleTime = models.DateTimeField(null=True) # 审核时间

class Reimbursement(models.Model):
    """
    报销申请
    """
    id = models.AutoField(primary_key=True)
    applyTime = models.DateTimeField(auto_now_add=True)  # 申请时间
    user = models.ForeignKey(MyUser, related_name='applyed_Reimbursement', on_delete=models.PROTECT)
    moneny = models.TextField("报销金额", null=False)
    type = models.TextField("报销类别", null=False)
    detail = models.TextField("费用明细", null=False)
    handleTime = models.DateTimeField(null=True) # 审核时间
    approver = models.ForeignKey(MyUser, related_name='approved_Reimbursement', null=True, on_delete=models.PROTECT) # 审核人
    result = models.BooleanField("报销是否成功", default=False)
    feedback = models.TextField("审核反馈", null=True)
