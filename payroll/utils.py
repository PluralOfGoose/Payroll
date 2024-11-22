# utils.py
from decimal import Decimal
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string

def get_state_tax_rate(state):
    """
    Returns the tax rate for the given state.
    Defaults to a general tax rate of 6% if the state is not listed.
    """
    state_tax_rates = {
        'NY': 0.07,  # New York
        'CA': 0.08,  # California
        'TX': 0.05,  # Texas
        'FL': 0.06,  # Florida
        'PA': 0.055, # Pennsylvania
        # Add more states and their tax rates as needed
    }
    return state_tax_rates.get(state, 0.06)  # Default tax rate is 6%


def calculate_payroll(hours_worked, hourly_rate, state):
    """
    Calculates the gross pay, taxes withheld, and net pay for an employee.
    
    Args:
        hours_worked (float): Number of hours worked by the employee.
        hourly_rate (float): Hourly wage of the employee.
        state (str): State in which the employee worked.
    
    Returns:
        dict: A dictionary containing:
            - 'gross_pay': Total earnings before taxes.
            - 'taxes_withheld': Amount withheld for taxes.
            - 'net_pay': Total earnings after taxes.
    """
    hours_worked = Decimal(hours_worked)
    hourly_rate = Decimal(hourly_rate)
    gross_pay = hours_worked * hourly_rate

    tax_rate = get_state_tax_rate(state)
    tax_rate = Decimal(tax_rate)
    taxes_withheld = gross_pay * tax_rate
    net_pay = gross_pay - taxes_withheld

    return {
        'gross_pay': round(gross_pay, 2),
        'taxes_withheld': round(taxes_withheld, 2),
        'net_pay': round(net_pay, 2),
    }

def generate_pdf(template_path, context):
    """
    Generates a PDF from an HTML template.
    """
    html = render_to_string(template_path, context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if pdf.err:
        return None
    return result.getvalue()
