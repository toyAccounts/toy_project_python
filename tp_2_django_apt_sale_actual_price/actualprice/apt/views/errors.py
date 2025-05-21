from django.shortcuts import redirect

def custom_404(request, exception):
    return redirect('/apt/main')

def custom_500(request):
    return redirect('/apt/main')