from django.shortcuts import render


def index(request):
    return render(request, "shifumi/shifumi.html")
    # return render(request, "ticTacToe/lobby.html")
