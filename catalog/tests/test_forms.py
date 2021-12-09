import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import ExtendAdoptionForm

class ExtendAdoptionFormTest(TestCase):
    def test_extended_adoption_date_field_label(self):
        form = ExtendAdoptionForm()
        self.assertTrue(form.fields['extended_adoption_date'].label is None or form.fields['extended_adoption_date'].label == 'extended adoption date')

    def test_extension_form_date_field_help_text(self):
        form = ExtendAdoptionForm()
        self.assertEqual(form.fields['extended_adoption_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_extension_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = ExtendAdoptionForm(data={'extended_adoption_date': date})
        self.assertFalse(form.is_valid())

    def test_extension_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = ExtendAdoptionForm(data={'extended_adoption_date': date})
        self.assertFalse(form.is_valid())

    def test_extension_form_date_today(self):
        date = datetime.date.today()
        form = ExtendAdoptionForm(data={'extended_adoption_date': date})
        self.assertTrue(form.is_valid())

    def test_extension_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = ExtendAdoptionForm(data={'extended_adoption_date': date})
        self.assertTrue(form.is_valid())
