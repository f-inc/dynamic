def dynamic(func):
    def wrapper():
        print("wrapper running")
        func()

    wrapper.is_wrapped = True
    return wrapper