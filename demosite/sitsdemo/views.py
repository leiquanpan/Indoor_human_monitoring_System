from django.http import HttpResponse
from django.shortcuts import render
import json


def index(request):
    with open('media/matrix.json', 'r') as f:
        json_obj = json.load(f)

    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for row, col in json_obj:
        # print(row, col, "haha")
        # print(json_obj[row + col])
        is_ava = 0
        if json_obj[row + col] is True:
            is_ava = 1
        if row == 'A':
            matrix[0][2-int(col)] = is_ava
        elif row == 'B':
            matrix[1][2-int(col)] = is_ava
        elif row == 'C':
            matrix[2][2-int(col)] = is_ava
        elif row == 'D':
            matrix[3][2-int(col)] = is_ava
    context = {'sits_matrix': matrix}
    return render(request, 'sitsdemo/index.html', context)
