def some_function(str):
    print(str)

a = "hi"
slot = lambda a1 = a :some_function(a) 
a = "hello"

slot()