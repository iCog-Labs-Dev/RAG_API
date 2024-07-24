import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from dotenv import load_dotenv, set_key
import subprocess

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        # Step 1: Accept the .txt file
        uploaded_file = request.FILES['file']
        
        # Step 2: Create directories and save the file
        base_dir = 'ragdir/input'
        os.makedirs(base_dir, exist_ok=True)
        file_path = os.path.join(base_dir, uploaded_file.name)
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Step 3: Run the first command
        os.system(f"python -m graphrag.index --init --root ./ragdir")
        
        # Step 4: Load API key from root .env file
        root_env_path = os.path.join(settings.BASE_DIR, '.env')
        load_dotenv(root_env_path)
        api_key = os.getenv('API_KEY')
        
        if not api_key:
            return JsonResponse({'error': 'API_KEY not found in root .env file'}, status=400)
        
        # Step 5: Clear and update the .env file in ragdir
        ragdir_env_path = os.path.join('ragdir', '.env')
        if os.path.exists(ragdir_env_path):
            os.remove(ragdir_env_path)  # Remove existing .env file to clear contents

        # Create a new .env file and set GRAPHRAG_API_KEY
        set_key(ragdir_env_path, 'GRAPHRAG_API_KEY', api_key)
        
        # Step 6: Run the second command
        os.system(f"python -m graphrag.index --root ./ragdir")

        return JsonResponse({'message': 'File processed and API key set successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def run_query(request):
    if request.method == 'POST':
        # Step 1: Get the text query and option from the POST data
        text_query = request.POST.get('text_query')
        method_option = request.POST.get('method_option')
        
        # Check if the required parameters are provided
        if not text_query or method_option not in ('global', 'local'):
            return JsonResponse({'error': 'Invalid parameters'}, status=400)
        
        # Step 2: Form the command
        command = [
            'python', '-m', 'graphrag.query',
            '--root', './ragdir',
            '--method', method_option,
            text_query
        ]
        
        try:
            # Step 3: Run the command and capture the output
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout
            
            # Parse the output to extract the response
            response_start = output.find('SUCCESS:')
            if response_start != -1:
                response_text = output[response_start:].strip()
            else:
                response_text = "No valid response found."
            
            return HttpResponse(response_text, content_type='text/plain')
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': str(e), 'output': e.output, 'stderr': e.stderr}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
