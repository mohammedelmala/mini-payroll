# Generated by Django 3.1.3 on 2021-09-15 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_auto_20210915_0529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elemententry',
            old_name='elementType',
            new_name='element_type',
        ),
        migrations.CreateModel(
            name='RunResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(choices=[('E', 'Earnings'), ('D', 'Deductions'), ('I', 'Information')], max_length=1)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sign', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('element_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='payroll.elemententry')),
                ('element_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='payroll.elementtype')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='payroll.employee')),
                ('employee_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='payroll.employeeaction')),
            ],
        ),
        migrations.CreateModel(
            name='PrePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prepayments', to='payroll.employee')),
                ('employee_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prepayments', to='payroll.employeeaction')),
            ],
        ),
    ]
