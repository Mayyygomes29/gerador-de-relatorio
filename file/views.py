import base64
import io
import os
from io import BytesIO, StringIO
from pyexpat.errors import messages
import tempfile
import textwrap
from urllib import request
from django.http import HttpResponse
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import redirect, render
from .forms import UploadForm
import matplotlib
matplotlib.use('Agg')

#Retorna um erro
def system_error(request):
    return render(request, 'error.html', status=400)


#Ler um arquivo 
def upload(request):
    global arq 
    if request.method == 'POST':
        form= UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            name, ext = os.path.splitext(file.name)
            try:
                if ext == '.csv':
                    sep = form.cleaned_data.get('sep', ',')  # default vírgula
                    df = pd.read_csv(file, sep=sep)   
                    resume  = df.head(20) 
                elif ext == '.json':
                    df = pd.read_json(file) 
                    resume  = df.head(20)
                elif ext == ".xlsx":
                    df = pd.read_excel(file, engine="openpyxl")
                    resume  = df.head(20)
                elif ext == ".xls":
                    df = pd.read_excel(file)
                    resume  = df.head(20)
                elif ext == ".xml":
                    df = pd.read_xml(file) 
                    resume  = df.head(20) 
                else:
                    messages.error(request, 'Extensão inválida!')
                    return redirect('system_error')
              
            except Exception as e:
                messages.error(request, f'Erro ao ler o arquivo: {e}')
                return redirect('system_error')
            
            df_json = df.to_json(orient='records')
            request.session['uploaded_file'] = df_json
            return render(request, 'upload.html', {'df': resume.to_html()})
    else:
        form = UploadForm()
        
    return render(request, 'upload.html', {'form': form})


#Gera gráficos de colunas numéricas
def graph(request):
    if 'uploaded_file' not in request.session:
        return redirect('error')

    df = pd.read_json(StringIO(request.session['uploaded_file']))
    data_numeric = df.select_dtypes('number')

    graphs = []

    for coluna in data_numeric.columns:
        plt.figure()
        plt.hist(data_numeric[coluna].dropna())
        plt.title(f"Histograma de {coluna}")
        plt.ylabel("Frequência")
        plt.grid()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        graphs.append({
            'coluna': coluna,
            'img': img_base64
        })

        buffer.close()
        plt.close()

    return render(request, "graphs.html", {"graphs": graphs})


def stats(request):
    if 'uploaded_file' not in request.session:
        return redirect('error')

    df_json = request.session['uploaded_file']
    df = pd.read_json(df_json, orient='records')

    estatisticas = []

    for coluna in df.columns:
        try:
            desc = df[coluna].describe()
            estatisticas.append({
                'coluna': coluna,
                'stats': desc.to_dict()  # 🔥 converte para dict
            })
        except Exception:
            estatisticas.append({
                'coluna': coluna,
                'stats': None,
                'erro': 'Não é possível calcular estatísticas para esta coluna.'
            })
    
    request.session['stats'] = estatisticas
    return render(request, 'stats.html', {
        'estatisticas': estatisticas
    })



def pdf_graph(request):
    if 'uploaded_file' not in request.session:
        return redirect('error')

    df = pd.read_json(StringIO(request.session['uploaded_file']))
    data_numeric = df.select_dtypes(include='number')

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    temp_files = []

    for col in data_numeric.columns:
        plt.figure(figsize=(7, 4), dpi=100)
        plt.hist(data_numeric[col].dropna(), bins=20)
        plt.title(f"Histograma de {col}")
        plt.xlabel(col)
        plt.ylabel("Frequência")
        plt.grid(True)
        plt.tight_layout()

        fd, temp_path = tempfile.mkstemp(suffix=".png")
        os.close(fd)

        plt.savefig(temp_path, bbox_inches='tight')
        plt.close()

        temp_files.append(temp_path)

        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Histograma da coluna: {col}", ln=True, align="C")
        pdf.ln(5)
        pdf.image(temp_path, x=10, w=190)

    # 👉 Gera PDF em buffer
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Graficos.pdf"'

    # Limpa arquivos temporários
    for path in temp_files:
        if os.path.exists(path):
            os.remove(path)

    return response





def pdf_stats(request):
    if 'stats' not in request.session:
        return redirect('error')
    estatisticas = request.session['stats']

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Relatório Estatístico', ln=True, align='C')
    pdf.ln(10)

    for item in estatisticas:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f"Coluna: {item['coluna']}", ln=True)

        pdf.set_font('Arial', '', 11)

        if item['stats']:
            for k, v in item['stats'].items():
                pdf.cell(0, 6, f"{k}: {v}", ln=True)
        else:
            pdf.cell(0, 6, "Não é possível gerar estatísticas para esta coluna.", ln=True)

        pdf.ln(5)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estatisticas.pdf"'
    return response
