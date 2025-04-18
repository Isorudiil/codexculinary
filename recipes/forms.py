from django import forms
import csv

class RecipeForm(forms.Form):
    name = forms.CharField(label='Recipe Name', max_length=100)
    ingredient_details = forms.CharField(label='Ingredient Details ("name: quantity unit", one per line - in desired order)', widget=forms.Textarea(attrs={'placeholder': 'format = name: quantity unit\none ingredient per line'}))
    instructions = forms.CharField(label='Instructions (one step per line)', widget=forms.Textarea(attrs={'placeholder': 'one step per line'}))
    servings = forms.IntegerField(label='Servings')
    prep_time = forms.IntegerField(label='Preparation Time')
    cook_time = forms.IntegerField(label='Cooking Time')
    category = forms.CharField(label='Categories (comma-separated, optional)', widget=forms.Textarea(attrs={'placeholder': 'comma-separated\noptional'}), required=False)
    notes = forms.CharField(label='Notes (optional)', widget=forms.Textarea(attrs={'placeholder': 'optional'}), required=False)

    def clean_ingredient_names(self):
        data = self.cleaned_data['ingredient_names']
        return [name.strip() for name in data.split(',')]

    def clean_ingredient_details(self):
        data = self.cleaned_data['ingredient_details']
        ingredient_details = {}
        for line in data.strip().split('\n'):
            if line:
                parts = line.split(':')
                if len(parts) == 2:
                    name = parts[0].strip()
                    quantity_unit = parts[1].strip().split()
                    if len(quantity_unit) >= 1:
                        quantity = quantity_unit[0]
                        unit = ' '.join(quantity_unit[1:])
                        try:
                            quantity = float(quantity)
                            ingredient_details[name] = {'quantity': quantity, 'unit': unit}
                        except ValueError:
                            raise forms.ValidationError(f"Invalid quantity for '{name}'. Please enter a number.")
                    else:
                        raise forms.ValidationError(f"Missing quantity for '{name}'.")
                else:
                    raise forms.ValidationError("Each ingredient details should be in the format 'name: quantity unit'.")
        return ingredient_details

    def clean_instructions(self):
        data = self.cleaned_data['instructions']
        return [step.strip() for step in data.strip().split('\n') if step.strip()]

    def clean_category(self):
        data = self.cleaned_data['category']
        if data:
            return [cat.strip() for cat in data.split(',')]
        return []

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label='CSV File')
    has_header = forms.BooleanField(label='File has header', initial=False, required=False)
