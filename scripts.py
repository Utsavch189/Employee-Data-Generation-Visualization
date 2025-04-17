# seed_data.py
import os
import django
import random
from datetime import timedelta, datetime
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from app.models import Employee, Attendance, Performance, Salary

fake = Faker()

def random_gender():
    return random.choice(['M', 'F'])

def random_status():
    return random.choice(['P', 'A', 'L'])

def generate_employees(n=5):
    employees = []
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        emp = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=fake.unique.email(),
            phone_number=fake.phone_number(),
            gender=random_gender(),
            date_of_birth=fake.date_of_birth(minimum_age=22, maximum_age=50),
            join_date=fake.date_between(start_date='-2y', end_date='today'),
            department=fake.job()
        )
        employees.append(emp)
    return employees

def generate_attendance(employees):
    for emp in employees:
        for _ in range(10):
            date = fake.date_between(start_date='-15d', end_date='today')
            check_in = fake.time_object()
            working_hours = round(random.uniform(6.0, 9.0), 2)
            check_out = (datetime.combine(datetime.today(), check_in) + timedelta(hours=working_hours)).time()

            Attendance.objects.create(
                employee=emp,
                date=date,
                status=random_status(),
                check_in_time=check_in,
                check_out_time=check_out,
                working_hours=working_hours,
                location=fake.city()
            )

def generate_performance(employees):
    for emp in employees:
        for _ in range(3):
            Performance.objects.create(
                employee=emp,
                review_period=f"Q{random.randint(1, 4)} 202{random.randint(2, 4)}",
                rating=round(random.uniform(2.5, 5.0), 1),
                goals_met=random.choice([True, False]),
                feedback=fake.paragraph(),
                manager_name=fake.name(),
                promotion_recommendation=random.choice([True, False])
            )

def generate_salary(employees):
    for emp in employees:
        for _ in range(3):
            basic = random.randint(30000, 80000)
            bonus = random.randint(1000, 10000)
            tax = random.randint(2000, 8000)
            net = basic + bonus - tax
            Salary.objects.create(
                employee=emp,
                basic_salary=basic,
                bonus=bonus,
                tax_deductions=tax,
                net_salary=net,
                payment_date=fake.date_between(start_date='-3M', end_date='today'),
                bank_account_no=fake.bban(),
                payment_mode=random.choice(['Bank Transfer', 'UPI', 'Cheque'])
            )

def run():
    print("Deleting old data...")
    Employee.objects.all().delete()
    Attendance.objects.all().delete()
    Performance.objects.all().delete()
    Salary.objects.all().delete()

    print("Creating synthetic employees...")
    employees = generate_employees(100)

    print("Generating attendance records...")
    generate_attendance(employees)

    print("Generating performance records...")
    generate_performance(employees)

    print("Generating salary records...")
    generate_salary(employees)

    print("Done.")

if __name__ == '__main__':
    run()
