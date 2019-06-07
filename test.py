# class Employee:
#
#     empCount = 0
#
#     def __init__(self, name, salary):
#         self.name = name
#         self.salary = salary
#         Employee.empCount += 1
#
#     def displayCount(self):
#         print "Total Employee %d" % Employee.empCount
#
#     def displayEmployee(self):
#         print "Name : ", self.name, ", Salary: ", self.salary
#
#
#
# emp1 = Employee("Zara", 2000)
# emp2 = Employee("Manni", 5000)
# emp1.displayEmployee()
# emp2.displayEmployee()
# print "Total Employee %d" % Employee.empCount

# 获取单个
from evaluate.product.estimate import classify

price = classify([1.69, 1525104000, 5], "017adc861c20b360bddb4dce92d9608a")

print (price)