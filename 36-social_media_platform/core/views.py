from django.shortcuts import redirect

def root_redirect(request):
    return redirect('home')