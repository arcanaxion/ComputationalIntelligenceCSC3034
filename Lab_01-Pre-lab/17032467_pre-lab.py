def fibonacci(sl):
    if sl == 1:
        return 0
    elif sl == 2:
        return 1
    else:
        return fibonacci(sl-2) + fibonacci(sl-1)

if __name__ == "__main__":
    print(fibonacci(10)) 