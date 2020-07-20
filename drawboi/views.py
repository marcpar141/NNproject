from django.http import HttpResponse


def start_screen(request):
    return HttpResponse("<h1>Hello, world. You're at the start_screen.</h1>")


def test_me(request):
    return HttpResponse("All works fine for now :) ")


def draw_screen(request):
    return HttpResponse("Some day you will paint here")


def end_screen(request):
    return HttpResponse("good work!\t I guess :')")
