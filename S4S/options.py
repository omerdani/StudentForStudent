from django.shortcuts import render, redirect


def settings(request):
    if request.method == 'POST':
        color = request.POST.get('color')
        dark_mode = 'dark_mode' in request.POST
        request.session['color'] = color
        request.session['dark_mode'] = dark_mode
        return redirect('settings')
    else:
        return render(request, 'settings.html')
from django.http import JsonResponse

def toggle_dark_mode(request):
    if request.method == 'POST':
        dark_mode = request.POST.get('dark_mode') == 'true'
        request.session['dark_mode'] = dark_mode
        return JsonResponse({'dark_mode': dark_mode})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)