# def safe_find(element, method, *args, **kwargs):
#     try:
#         return getattr(element, method)(*args, **kwargs)
#     except AttributeError:
#         return None


arr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
enum = list(enumerate(arr))
print(*enum)

a = {}


for index, num in enumerate(arr):
    a[index] = num
print(a)


a = {index: num for index, num in enumerate(arr)}

print(a)

print(list(a.keys()))
