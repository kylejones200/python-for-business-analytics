"""Show that a function can read a module-global variable."""

x = 10

def my_function():
    print(x)

if __name__ == "__main__":
    my_function()
    print(x)
