'''
Created on 2019/07/07

@author: shunsuke
'''

# sort の使い方について
COLOR_A = {
    "no": 5,
    "kind": 1,
    "name": "aliceblue",
}
COLOR_B = {
    "no": 4,
    "kind": 1,
    "name": "Black",
}
COLOR_C = {
    "no": 3,
    "kind": 2,
    "name": "coral",
}
COLOR_D = {
    "no": 2,
    "kind": 2,
    "name": "Deepskyblue",
}
COLOR_F = {
    "no": 1,
    "kind": 2,
    "name": "forestgreen",
}

sample_list = [
    COLOR_A,
    COLOR_B,
    COLOR_C,
    COLOR_D,
    COLOR_F
]

# 1. 番号の順番で並び替える
no_index = [5, 2, 3, 4, 1]

print(
    sorted(
        sample_list,
        key=lambda data: no_index.index(data["no"])
    )
)

# 2. 文字列の順番で並び変える
name_index = [
    COLOR_B["name"], COLOR_D["name"], COLOR_F["name"],
    COLOR_C["name"], COLOR_A["name"]
]

print(
    sorted(
        sample_list,
        key=lambda data: name_index.index(data["name"])
    )
)

# 3. 種類と文字列（大文字小文字区別なし辞書）の順番で並び替える
print(
    sorted(
        sample_list,
        key=lambda data: [no_index.index(data["kind"]),
        str.lower(data["name"])]
    )
)

