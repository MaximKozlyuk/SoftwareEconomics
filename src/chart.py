import matplotlib.pyplot as plt


def func():
    return [1, 2, 3]


x = func()
y = [5, 7, 4]

plt.xlabel('x')
plt.ylabel('y')
plt.title("Example chart")

plt.plot(x, y)

plt.show()
