import queue

# a = queue.Queue()
# for i in range(10):
#     a.put(i)
#
# b = a
# for i in range(b.qsize()):
#     print(b.get(), end=' ')

a = [1, 2, 3, 4, 5]
print(a)
b = a
print(b)
b.append(6)
print(b)
print(a)

