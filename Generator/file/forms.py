
from django import forms
import os 


class UploadForm(forms.Form):
    file = forms.FileField(allow_empty_file=False, label='File')

    def clean_file(self):
        data = self.cleaned_data["file"]
        name, ext = os.path.splitext(data.name)
        valid_exts = ['.csv', '.json', '.xlsx', '.xls', '.xml']
        if ext.lower() not in valid_exts:
            raise forms.ValidationError("Esse arquivo não é válido.")
        
        if ext.lower() == '.csv':
            resume = data.read(2884).decode('utf-8', errors = 'ignore')
            data.seek(0)
            separador = [',', ';', '|','\t']
            sep_detect = max(separador, key=resume.count)
            if resume.count(sep_detect) == 0:
                raise forms.ValidationError("Separador do arquivo CSV não identificado.")
            self.cleaned_data['sep'] = sep_detect
        return data
       