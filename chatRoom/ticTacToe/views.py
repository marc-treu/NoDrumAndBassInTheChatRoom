from django.shortcuts import render


def index(request):
    return render(request, "ticTacToe/lobby.html")


def room(request, room_name):
    return render(request, "ticTacToe/tictactoe.html", {"room_name": room_name})
