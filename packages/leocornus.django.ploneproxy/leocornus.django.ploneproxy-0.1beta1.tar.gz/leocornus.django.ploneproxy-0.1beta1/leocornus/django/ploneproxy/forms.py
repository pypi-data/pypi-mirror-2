
# forms.py

"""
form classes for Leocornus Django Ploneproxy
"""

from django.forms import BooleanField
from django.contrib.auth.forms import AuthenticationForm as BaseForm
from django.utils.translation import ugettext_lazy as _ 

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class AuthenticationForm(BaseForm):
    """
    a sample authentication form extends from the base authentication
    form.  adding a check box
    """

    acceptDisclaimer = BooleanField(label='')

    
