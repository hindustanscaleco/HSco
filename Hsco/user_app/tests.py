
#decorator function
def lowercase(function):
    def wrapper():
        # pre processing before calling any function
        func = function()
        # post processing after calling any function
        string_lowercase = func.lower()
        return string_lowercase
    return wrapper

@lowercase
def hello():
    return 'HELLO WORLD'

print(hello())

a = [1, 2, 3]
b = [7, 8, 9, 4, 7]

print([x**2 for x in a])
print([x+y for (x,y) in zip(a,b)])
print([x for (x,y) in zip(a,b)])

my_list = [[10,20,30],[40,50,60],[70,80,90]]
flattened = [x for temp in my_list for x in temp]

print('flattened -->', flattened)
print('my list-->', my_list)

mul = lambda x, y : x * y
print('mul ---->', mul(2,5))

#generators

def fib(n):
    p, q = 0, 1
    while(p<n):
        yield p
        p, q = q, p+q
        
x = fib(10)
print(x.__next__())
print(x.__next__())
print(x.__next__())
print(x.__next__())
print(x.__next__())
print(x.__next__())
print(x.__next__())


#iterators
class ArrayList:
   def __init__(self, number_list):
       self.numbers = number_list
   def __iter__(self):
       self.pos = 0
       return self
   def __next__(self):
       if(self.pos < len(self.numbers)):
           self.pos += 1
           return self.numbers[self.pos - 1]
       else:
           raise StopIteration
array_obj = ArrayList([1, 2, 3])
it = iter(array_obj)
print('iterator')
print(next(it)) #output: 2
print(next(it)) #output: 3
print(next(it))