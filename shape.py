from typing import List
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgb

def Rectangle(
    ax: plt.Axes, 
    x: float,       # 左下角x坐标
    y: float,       # 左下角y坐标
    width: float,   # 宽度
    height: float,  # 高度
    color: str,     # 颜色
) -> None:
    ax.add_patch(mpatches.Rectangle([x,y],width,height, color = color))

def Polygon(
    ax: plt.Axes,       
    points: List[List[float]],  # 多边形顶点坐标
    color: str                   # 颜色
) -> None:
    ax.add_patch(mpatches.Polygon(points, color = color))

def Line(
    ax: plt.Axes,       
    x1: float,          # 起点x坐标
    y1: float,          # 起点y坐标
    x2: float,          # 终点x坐标
    y2: float,          # 终点y坐标
    color: str          # 颜色
) -> None:
    ax.plot([x1,x2],[y1,y2], color = color)

def Circle(
    ax: plt.Axes,
    x: float,               # 圆心x坐标
    y: float,               # 圆心y坐标
    r: float,               # 半径
    color: str,             # 颜色
    theta1: float = 0,      # 起始角度
    theta2: float = 360,    # 终止角度
    fill: bool = True,      # 是否填充
    shade: bool = False     # 是否阴影
) -> None:
    if shade:
        ax.add_patch(mpatches.Circle([x-1,y+1], r, color = "white"))
        ax.add_patch(mpatches.Circle([x+1,y-1], r, color = "black"))
    ax.add_patch(mpatches.Wedge([x,y], r, theta1, theta2, fill = fill, color = color))
    if shade:
        n = 5
        light = 0.85
        rgb = to_rgb(color)
        dist = [0.5-0.5**(i+1) for i in range(1, n+1)]  # 等比数列求和
        rs = [rgb[0] + (max(light-rgb[0], 0))*d/n for d in range(1, n+1)]
        gs = [rgb[1] + (max(light-rgb[1], 0))*d/n for d in range(1, n+1)]
        bs = [rgb[2] + (max(light-rgb[2], 0))*d/n for d in range(1, n+1)]
        for i in range(n):
            ax.add_patch(mpatches.Circle([x-dist[i]*r,y+dist[i]*r], r*0.6/(i+1), color = (rs[i],gs[i],bs[i])))