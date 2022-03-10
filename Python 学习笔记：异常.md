# Python 学习笔记：异常

## 目标

* 了解异常
* 捕获异常
* 异常的else
* 异常的finally
* 异常的传递
* 自定义异常

## 1. 了解异常

当检测到一个错误时，解释器无法继续执行了，反而出现了一些错误的提示，这就是异常。

## 2 异常的写法

### 2.1 语法

```python
    try:
        可能出现异常的代码
    except:
        如果出现异常执行的代码
```    
> 注意：
>    1. 如果没有指定异常，那么所有的异常都会被捕获;
>    2. 如果指定了异常，那么只有指定的异常才会被捕获;
>    3. 一般try下方只放一行尝试执行的代码。

### 2.2 捕获指定异常

#### 2.2.1 语法

```python
    try:
        可能出现异常的代码
    except 异常类型:
        如果捕获到该异常类型执行的代码
```

#### 2.2.2 捕获多个异常

当捕获多个异常时，可以把要捕获的异常类型的名字，放到except后，并使用元组的方式进行书写。

```python
    try：
        print(1/0)
    except (NameError, ZeroDivisionError):
        print("出现了错误")
```

#### 2.2.3 捕获异常描述信息

```python
    try:
        print(num)
    except (NameError, ZeroDivisionError) as e:
        print(e)
```

#### 2.2.4 捕获所有异常

Exception 是所有程序异常类的父类。

```python
    try:
        print(num)
    except Exception as e:
        print(e)
```

### 2.3 异常的else

else表示如果没有异常要执行的代码。

```python
    try:
        print(num)
    except Exception as e:
        print(e)
    else:
        print("我是else，没有异常时执行的代码")
```

### 2.4 异常的finally

finally表示无论是否有异常，都要执行的代码。

```python
    try:
        # 尝试以 a 模式打开文件
        f = open("test.txt", "a")
    except Exception as e:
        # 如果有异常就以 w 模式打开文件
        f = open("test.txt", "w")       
    else:
        # 如果没有异常，执行的代码
        print("没有异常，真开心")     
    finally:
        # 有无异常都会关闭文件
        f.close()
```

## 3. 异常的传递

需求：
1. 尝试只读方式打开文件，如果文件存在则读取文件，如果文件不存在，则提示用户；
2. 读取内容要求：尝试循环读取内容，读取过程中如果检测到用户意外终止程序，则except捕获异常。

```python
    import time
    try:
        f = open("test.txt")
        try:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                # 暂停2秒以便于用户中止
                time.sleep(2)
                print(line)
        except:
            # 如果在读取文件的过程中，产生了异常，那么就会捕获到
            # 比如 按下了 ctrl+C
            print('意外终止了读取数据')
        finally:
            f.close()
            print('关闭文件')
    except:
        
```

## 4. 自定义异常

在 Python 中，抛出自定义异常的语法为 **raise 异常对象**。

需求：密码长度不足，则报异常（用户输入密码，如果输入的长度不足6位，则报错，即抛出自定义异常，并捕获该异常）。

```python
    # 自定义异常类，继承Exception
    class ShortInputError(Exception):
        def __init__(self, length, min_len):
            self.length = length
            self.min_len = min_len
            
        # 设置抛出异常的描述信息
        def __str__(self):
            return f'你输入的长度是 {self.length} 个字符， 不能少于 {self.min_len} 个字符'
        
        
    def main():
        try:
            con = input('请输入密码：')
            if len(con) < 6:
                raise ShortInputError(len(con), 6)
        except Exception as result:
            print(result)
        else:
            print('密码已经输入完成')
    
    
    main()
```

## 5. 总结

* 异常语法
```python
    try:
        可能发生异常的代码
    except:
        如果出现异常执行的代码
    else:
        没有异常执行的代码
    finally::
        无论是否出现异常都要执行折代码
```

* 捕获异常

```python
    except 异常类型：
        代码
    
    except 异常类型 as x:
        代码
```

* 自定义异常

```python
    # 1. 自定义异常
    class 异常类类名(Exception):
        代码
        
        # 设置抛出异常的描述信息
        def __str__(self):
            return 'str'
        
    # 2. 抛出异常
    raise 异常名()

    # 捕获异常
    except Exception...
```




