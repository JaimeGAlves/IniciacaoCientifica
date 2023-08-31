import requests
from django.http import JsonResponse
from django.shortcuts import render

def upload_file_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        # Preparar os dados para envio à API externa
        files = {'file': uploaded_file}

        # Enviar a solicitação POST para a API externa
        api_url = 'http://localhost:8000/uploadfile'  # Substitua pela URL real da API
        try:
            response = requests.post(api_url, files=files)
            response_data = response.json()

            return JsonResponse(response_data)
        except Exception as e:
            error_message = f"Erro ao enviar o arquivo para a API: {e}"
            return JsonResponse({"error": error_message}, status=500)

    return render(request, 'frontend/templates/home.html')