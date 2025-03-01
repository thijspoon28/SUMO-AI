my_dict = {}

a = "a"
b = "b"
my_dict[a][b] = my_dict.setdefault(a, {}).get(b, 0) + 1

print(my_dict)