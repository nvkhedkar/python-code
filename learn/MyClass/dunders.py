
class Student:
  def __init__(self):
    """Constructor"""
    print("init object")
    self.name = ''
    self.address = ''

  def create(self, n, a):
    self.name = n
    self.address = a
  # def __call__(self, *args, **kwargs):
  #     if "myfunc" in kwargs.keys():
  #         kwargs['myfunc'](self)
  #     else:
  #         self.address = self.address.upper()
  #     return self

  def __call__(self, *args, **kwargs):
    """Makes object callable"""
    self.address = self.address.upper()
    return self

  def __str__(self):
    """Maps to str()"""
    return f"name: {self.name}, address: {self.address}"

  def __len__(self):
    """Maps to len()"""
    return len(self.name) + len(self.address)

  def __eq__(self, other):
    """Overloads == operator"""
    return self.name == other.name


# def all_upper(st: Student):
#     st.name = st.name.upper()
#     st.address = st.address.upper()
#
#
# def add_prefix(st: Student):
#     st.name = f"ABC_{st.name}"
#     st.address = f"XYZ_{st.address}"


s = Student()
s.create(n='nikhil', a='pune')

s_string = str(s)  # __str__
s_len = len(s)  # __len__
print(f"Student string: {s_string}")
print(f"Student length: {s_len}")

print(f"Student before call: {str(s)}")
s()  # __call__ - the student object is now callable
print(f"Student after call: {str(s)}")

s2 = Student()
s2.create('amit', a='mumbai')

print(f"Are students equal: {s == s2}")  # __eq__ - students are comparable

