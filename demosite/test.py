import re
import json

# res = {
#     'C2': False,
#     'A0': False,
#     'A1': False,
#     'C0': False,
#     'B0': False,
#     'D2': False,
#     'D0': False,
#     'B1': False,
#     'C1': False,
#     'B2': False,
#     'D1': False,
#     'A2': False
# }

# with open('media/matrix.json', 'w') as f:
#     f.write(json.dumps(res))

with open('media/matrix.json', 'r') as f:
    json_obj = json.load(f)

matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
for row, col in json_obj:
    # print(row, col, "haha")
    print(json_obj[row + col])
    is_ava = 0
    if json_obj[row + col] is True:
        is_ava = 1
    if row == 'A':
        matrix[0][int(col)] = is_ava
    elif row == 'B':
        matrix[1][int(col)] = is_ava
    elif row == 'C':
        matrix[2][int(col)] = is_ava
    elif row == 'D':
        matrix[3][int(col)] = is_ava

print(matrix)