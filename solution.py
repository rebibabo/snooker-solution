from typing import List, Tuple, Callable
import math

def symmetry(n: int) -> List[Tuple[int, int]]:
    ''' 计算n库解决的镜像坐标，表示为(x,y)坐标，其中x表示x轴上多少个桌子长度，y表示y轴上多少个桌子宽度 '''
    ret = [(0, n), (n, 0), (0, -n), (-n, 0)]
    for i in range(1, n//2+1):
        if i == n - i:  # e.g. （1,1), (1,-1), (-1,1), (-1,-1)
            ret.extend([(i, n-i), (-i, n-i), (i, i-n), (-i, i-n)])
        else:   # e.g. (1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)
            ret.extend([(i, n-i), (-i, n-i), (i, i-n), (-i, i-n), (n-i, i), (i-n, i), (n-i, -i), (i-n, -i)])
    return ret

def line(x1: float, y1: float, x2: float, y2: float) -> Tuple[Callable, Callable]:
    ''' 构建直线方程，返回f(x)和f(y) '''
    if x2 == x1:
        return None, lambda y: x1
    if y2 == y1:
        return lambda x: y1, None
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    return lambda x: k * x + b, lambda y: (y - b) / k

def dist(x1: float, y1: float, x2: float, y2: float, x: float, y: float) -> float:
    ''' 计算点到直线距离 '''
    if x2 == x1:
        return abs(x1 - x)
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    return abs(k * x + b - y) / math.sqrt(1 + k**2)

def inLine(x1: float, y1: float, x2: float, y2: float, x: float, y: float) -> bool:
    ''' 计算点是否在线段两端垂直线之间 '''
    vector = (x2 - x1, y2 - y1)   # 线段的方向向量
    vector1 = (x1 - x, y1 - y)   # 点到线段起点的方向向量
    vector2 = (x2 - x, y2 - y)   # 点到线段终点的方向向量
    angle1 = vector1[0] * vector[0] + vector1[1] * vector[1]   # 点到线段起点的角度,忽略长度
    angle2 = vector2[0] * vector[0] + vector2[1] * vector[1]   # 点到线段终点的角度,忽略长度
    if angle1 * angle2 > 0:   # 点在线段两端，两个方向向量符号一样
        return False
    return True