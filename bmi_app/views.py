from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .forms import BMICalculatorForm
from .models import BMIRecord
from smtplib import SMTPException
import socket
from datetime import datetime

def home(request):
    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            # Process form data
            data = form.cleaned_data
            height = data['height']
            weight = data['weight']
            email = data['email']
            name = data['name']
            
            # Calculate BMI
            height_in_m = height / 100
            bmi = round(weight / (height_in_m ** 2), 1)
            
            # Determine category
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            
            # Save to database
            BMIRecord.objects.create(
                name=name,
                email=email,
                height=height,
                weight=weight,
                bmi_value=bmi,
                bmi_category=category
            )
            
            # Send email with all required parameters
            email_sent = send_bmi_report(
                email=email,
                name=name,
                bmi=bmi,
                category=category,
                height=height,
                weight=weight
            )
            
            return render(request, 'bmi_app/result.html', {
                'name': name,
                'bmi': bmi,
                'category': category,
                'email_sent': email_sent,
                'email_address': email,
                'height': height,
                'weight': weight
            })
    else:
        form = BMICalculatorForm()
    
    return render(request, 'bmi_app/index.html', {'form': form})

def calculate_bmi(request):
    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            height = data['height']
            weight = data['weight']
            email = data['email']
            name = data['name']
            height_in_m = height / 100
            bmi = round(weight / (height_in_m ** 2), 1)
            
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            
            # Send email with all required parameters
            email_sent = send_bmi_report(
                email=email,
                name=name,
                bmi=bmi,
                category=category,
                height=height,
                weight=weight
            )
                
            return render(request, 'bmi_app/result.html', {
                'name': name,
                'bmi': bmi,
                'category': category,
                'email_sent': email_sent,
                'email_address': email,
                'height': height,
                'weight': weight
            })
    
    return redirect('bmi_app:home')

def send_bmi_report(email, name, bmi, category, height, weight):
    subject = "Your BMI Report from BMI Calculator"
    current_year = datetime.now().year
    
    message = f"""
    Subject: Your BMI Report from BMI Calculator

    Hi {name},

    Thank you for using our BMI Calculator!

    Here is your personalized BMI report:

    - Height: {height} cm  
    - Weight: {weight} kg  
    - BMI: {bmi}  
    - Category: {category}

    Your health is important, and knowing your BMI is a great first step in understanding your body better.

    If you'd like to track your BMI over time or re-calculate in the future, feel free to visit us again!

    Stay healthy and take care,  
    – The BMI Calculator Team

    ---

    Support: mohannaidu2004@gmail.com
    © {current_year} BMI Calculator. All rights reserved.
    """
    
    try:
        send_mail(
            subject,
            message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print(f"Email sent successfully to {email}")
        return True
    except BadHeaderError:
        print("Invalid header found in email")
        return False
    except SMTPException as e:
        print(f"SMTP error occurred: {str(e)}")
        return False
    except socket.gaierror:
        print("Network connection error")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False