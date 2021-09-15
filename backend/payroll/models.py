from django.db import models

# define variables

classifications = (("E", "Earnings"), ("D", "Deductions"),
                   ("I", "Information"))
action_types = (("R", "Run"), ("P", "Pre-Payment"))
status = (("S", "Success"), ("E", "Error"))

# Create your models here.


class Job(models.Model):
    name = models.CharField(max_length=60)
    title = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.job


class Department(models.Model):
    name = models.CharField(max_length=60)
    manager = models.ForeignKey(
        'Employee', related_name='manage', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_number = models.PositiveIntegerField()
    name = models.CharField(max_length=60)
    job = models.ForeignKey(
        Job, related_name='employees', on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, related_name="employees", on_delete=models.CASCADE)
    hiredate = models.DateField()
    manager = models.ForeignKey(
        'self', related_name="employees", null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True,)

    def __str__(self):
        return self.name


class ElementType(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    classification = models.CharField(max_length=1, choices=classifications)
    recurring = models.BooleanField(default=True)
    balance = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def sign(self):
        return 1 if self.classification == "E" else 1 if self.classification == "D" else 0

    def __str__(self):
        return self.name


class ElementEntry(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="elements")
    element_type = models.ForeignKey(
        ElementType, on_delete=models.CASCADE, related_name="entries")
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment = models.DecimalField(max_digits=10, decimal_places=2)
    last_payment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def pay_amount(self):

        if self.elementType.classification == "E":
            return self.amount
        if self.elementType.classification == "D":
            if not self.elementType.recurring:
                return self.amount
            else:
                if self.elementType.balance:
                    return self.installment
                else:
                    return self.amount
        else:
            return self.amount

    def __str__(self):
        return f'{self.employee.employee_number}-{self.employee.name}-{self.elementType.name}-{self.pay_amount}'


class PayrollAction(models.Model):
    action_type = models.CharField(max_length=1, choices=action_types)
    action_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=1, choices=status)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.action_type}-{self.action_time}-{self.status}'


class EmployeeAction(models.Model):
    employee = models.ForeignKey(
        Employee, related_name="actions", on_delete=models.CASCADE)
    action = models.ForeignKey(
        PayrollAction, related_name="employees", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=status)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.employee.employee_number}-{self.employee.name}-{self.action.action_type}-{self.status}"


class RunResult(models.Model):
    employee_action = models.ForeignKey(
        EmployeeAction, related_name="results", on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee, related_name="results", on_delete=models.CASCADE)
    element_type = models.ForeignKey(
        ElementType, related_name="results", on_delete=models.CASCADE)
    element_entry = models.ForeignKey(
        ElementEntry, related_name="results", on_delete=models.CASCADE)
    classification = models.CharField(max_length=1, choices=classifications)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sign = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.employee.employee_number}-{self.employee.name}-{self.element_type.name}-{self.element_type.classification}-{self.amount}'


class PrePayment(models.Model):
    employee_action = models.ForeignKey(
        EmployeeAction, related_name="prepayments", on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee, related_name="prepayments", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.employee.employee_number}-{self.employee.name}-{self.amount}'
