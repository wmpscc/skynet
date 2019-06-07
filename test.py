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
import evaluate.product.estimate

atom = [1.69, 1525104000, 5]
model_id = "017adc861c20b360bddb4dce92d9608a"

tree_price = evaluate.product.estimate.classifyTree([atom], model_id)

bayes_price = evaluate.product.estimate.classifyBayes([atom], model_id)

knn_price = evaluate.product.estimate.classifyKnn([atom], model_id)

print ("tree price is ", tree_price)
print ("bayes price is ", bayes_price)
print ("knn price is ", knn_price)