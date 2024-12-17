class A:
    def method_a(self):
        print("Method A")

class B:
    def method_b(self):
        print("Method B")

class C(A, B):
    def method_c(self):
        print("Method C")

# 创建类 C 的实例
c = C()

# 可以调用来自类 A 和类 B 的方法
c.method_a()  # 输出: Method A
c.method_b()  # 输出: Method B
c.method_c()  # 输出: Method C
