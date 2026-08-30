"""Contrast a module-global name with a function-local name."""

y = 10

def my_function():
    y = 5
    print(y)

if __name__ == "__main__":
    my_function()
    print(y)
    try:
        print(z)
    except NameError:
        print("NameError: name 'z' is not defined")
