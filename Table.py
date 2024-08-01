import matplotlib.pyplot as plt
from typing import Union, Tuple, List, Dict
from shape import *
from solution import *
import math

class Ball:
    x: float    # 球的x坐标
    y: float    # 球的y坐标
    color: str  # 球的颜色

    def __init__(self, x: float, y: float, color: str) -> None:
        self.x = x
        self.y = y
        self.color = color

class Table:
    width: float = 1778     # 球桌宽度
    length: float = 3568    # 球桌长度
    hole: float = 42.5      # 球洞半径
    ball: float = 26.8      # 球半径
    line_x: float = 737     # 开球区x轴坐标
    Circle_r: float = 292   # 开球区半径
    balls: Dict[str, Ball] = {} # 球桌上的球
        
    def __init__(self, balls: Union[List[Ball], None] = None) -> None:
        if balls is None:
            self.balls['cue'] = Ball(self.line_x - 3*self.ball, self.width/2, 'white')
            self.balls['black'] = Ball(self.length - 324, self.width/2, 'black')
            self.balls['blue'] = Ball(self.length/2, self.width/2, 'blue')
            self.balls['pink'] = Ball(self.length/4*3, self.width/2, 'pink')
            self.balls['yellow'] = Ball(self.line_x, self.width/2 - self.Circle_r, 'yellow')
            self.balls['green'] = Ball(self.line_x, self.width/2 + self.Circle_r, 'green')
            self.balls['brown'] = Ball(self.line_x, self.width/2, 'brown')
            num = 0
            for i in range(5):
                for j in range(i+1):
                    x = self.balls['pink'].x + 2*self.ball + self.ball*i*math.sqrt(3)   # 最左边红球紧贴分球，红球x轴间距为ball*sqrt(3)
                    y = self.width/2 + 2*self.ball*(j - 0.5*i)  # y轴间距为2*ball
                    num += 1
                    self.balls[f'red_{num}'] = (Ball(x, y, 'red'))
        else:
            self.balls = balls

    @ classmethod
    def convert(self, x: float, y: float) -> Tuple[float, float]:
        ''' 将镜像坐标转换为实际坐标，当前x坐标如果出于(2l+1, 2l+2]中，则需要翻转x坐标，如果y坐标处于(2w+1, 2w+2]中，则需要翻转y坐标 '''
        # 这里减去10e-6是为了对齐整除结果,e.g.[1,2)和镜像范围e.g.(1,2]
        # 因为球有体积，实际碰库坐标应该减去球半径，桌子长度减去2倍的球半径
        index_x = (x - self.ball - 10e-6) // (self.length - 2*self.ball)    
        if index_x % 2: # 对称
            # (l-2b) - {x - [b + k(1-2b)]} + 3b
            x = (index_x + 1) * (self.length - 2*self.ball) - x + 2*self.ball
        else:
            x -= index_x * (self.length - 2*self.ball)
        index_y = (y - self.ball - 10e-6) // (self.width - 2*self.ball)
        if index_y % 2: # 对称
            y = (index_y + 1) * (self.width - 2*self.ball) - y + 2*self.ball
        else:
            y -= index_y * (self.width - 2*self.ball)
        return x, y

    def valid(self, solutions: List[Tuple[float, float]], target: Ball) -> bool:
        ''' 判断解是否有效，不能掉袋，不能碰到非目标球 '''
        for i in range(len(solutions) - 1):
            x1, x2, y1, y2 = solutions[i][0], solutions[i+1][0], solutions[i][1], solutions[i+1][1]
            if y1 <= self.ball + 10e-6 or y1 >= self.width - self.ball - 10e-6:    
                if x1 < 2.5*self.hole or \
                    x1 > self.length - 2.5*self.hole or \
                    self.length//2 - 3*self.hole < x1 < self.length//2 + 3*self.hole:
                    return False
            if x1 <= self.ball + 10e-6 or x1 >= self.length - self.ball - 10e-6:
                if y1 < 2.5*self.hole or \
                    y1 > self.width - 2.5*self.hole:
                    return False
            for ball in self.balls.values():
                if ball == target or ball == self.balls['cue']: # 跳过目标球和母球
                    continue
                if inLine(x1, y1, x2, y2, ball.x, ball.y):
                    d = dist(x1, y1, x2, y2, ball.x, ball.y)  
                    if d < 2 * self.ball:    # 如果发生碰撞
                        return False
        return True

    def show(self, solution: List[Tuple[float, float]] = None) -> None:
        ''' 显示球桌 '''
        ax: plt.axes = plt.subplots(figsize=(16, 8))[1]
        margin = 2.7
        Rectangle(ax, -margin*self.hole, -margin*self.hole, self.length+2*margin*self.hole, self.width+2*margin*self.hole, '#00AA00') # 绿色桌布

        brown = '#8B4513'   # 棕色桌边
        Rectangle(ax, -4*self.hole, -4*self.hole, 8*self.hole + self.length, margin*self.hole, brown)    
        Rectangle(ax, -4*self.hole, self.width + (4-margin)*self.hole , 8*self.hole + self.length, margin*self.hole, brown)
        Rectangle(ax, -4*self.hole, -2*self.hole, margin*self.hole, self.width + 4*self.hole, brown)
        Rectangle(ax, self.length + (4-margin)*self.hole, -2*self.hole, margin*self.hole, self.width + 4*self.hole, brown)

        dark_green = "#1A8839"  # 深绿色库边
        Polygon(ax, [[-0.3*self.hole, (margin-4)*self.hole],
                    [1.5*self.hole, 0], [self.length//2-2*self.hole, 0], 
                    [self.length//2-0.7*self.hole, (margin-4)*self.hole]], dark_green)
        Polygon(ax, [[self.length//2+0.7*self.hole, (margin-4)*self.hole],
                    [self.length//2+2*self.hole, 0], 
                    [self.length-1.5*self.hole, 0], 
                    [self.length+0.3*self.hole, (margin-4)*self.hole]], dark_green)
        Polygon(ax, [[-0.3*self.hole, self.width-(margin-4)*self.hole],
                    [1.5*self.hole, self.width], [self.length//2-2*self.hole, self.width], 
                    [self.length//2-0.7*self.hole, self.width-(margin-4)*self.hole]], dark_green)
        Polygon(ax, [[self.length//2+0.7*self.hole, self.width-(margin-4)*self.hole],
                    [self.length//2+2*self.hole, self.width], 
                    [self.length-1.5*self.hole, self.width], 
                    [self.length+0.3*self.hole, self.width-(margin-4)*self.hole]], dark_green)
        Polygon(ax, [[(margin-4)*self.hole, -0.3*self.hole],
                    [0, 1.5*self.hole], [0, self.length//2-1.5*self.hole],
                    [(margin-4)*self.hole, self.length//2+0.3*self.hole]], dark_green)
        Polygon(ax, [[self.length-(margin-4)*self.hole, -0.3*self.hole],
                    [self.length, 1.5*self.hole], [self.length, self.length//2-1.5*self.hole],
                    [self.length-(margin-4)*self.hole, self.length//2+0.3*self.hole]], dark_green)

        Rectangle(ax, self.line_x, 0, 1, self.width, '#DDDDDD')   # 开球线
        Circle(ax, self.line_x, self.width/2, self.Circle_r, '#DDDDDD', 90, 270, fill=False)  # 开球区

        for x in [-self.hole/2, self.length/2, self.length + self.hole/2]:  # 球洞
            for y in [-self.hole/2, self.width + self.hole/2]:
                Circle(ax, x, y, self.hole, 'black')

        for ball in self.balls.values():    # 球
            Circle(ax, ball.x, ball.y, self.ball, ball.color, shade=True)

        if solution:
            for i in range(len(solution) - 1):
                Line(ax, solution[i][0], solution[i][1], solution[i+1][0], solution[i+1][1], color='red')

        plt.axis('equal')
        [ax.spines[loc_ax].set_visible(False) for loc_ax in ['top','right','bottom','left']] # 不显示坐标轴 
        ax.set_xticks([])                   # 不显示x轴刻度 
        ax.get_yaxis().set_visible(False)   # 不显示y轴刻度
        plt.show()

    def solution(self, 
        target: str,    # 目标球的名字
        cursion: int    # 吃库次数
    ) -> List[List[Tuple[float, float]]]:
        ''' 计算解，返回所有可能的解 '''
        target = self.balls[target]
        cue = self.balls["cue"]
        if cursion == 0:    # 如果不吃库
            solutions = [(cue.x, cue.y), (target.x, target.y)]
            if self.valid(solutions, target):
                return [solutions]
        sym_indexs = symmetry(cursion)     # 计算镜像坐标
        left = target.x - self.ball                     # 目标球到左侧库边的距离
        right = self.length - target.x - self.ball      # 目标球到右侧库边的距离
        top = self.width - target.y - self.ball         # 目标球到顶部库边的距离
        bottom = target.y - self.ball                   # 目标球到底部库边的距离
        return_solutions = []
        for idx_x, idx_y in sym_indexs:
            solutions: List[Tuple[float, float]] = [(cue.x, cue.y)]     # solutions存放母球的碰库坐标，包括母球起始坐标和目标球坐标
            # Rectangle(ax, self.ball + idx_x * (self.length - 2*self.ball),   # 显示镜像桌面
            #     self.ball + idx_y * (self.width - 2*self.ball), 
            #     self.length - 2*self.ball, self.width - 2*self.ball, '#00AA00')
            sym_x = idx_x * (self.length - 2*self.ball) + (right if idx_x % 2 else left) + self.ball    # 计算目标球的镜像x坐标
            sym_y = idx_y * (self.width - 2*self.ball) + (top if idx_y % 2 else bottom) + self.ball
            # Circle(ax, sym_x, sym_y, self.ball, target.color, shade=True)    # 显示目标球的镜像
            fx, fy = line(cue.x, cue.y, sym_x, sym_y)   # 计算母球到镜像目标球的直线方程
            crossCoord: List[Tuple[float, float]] = []   # 存放碰撞点坐标
            if fx:  # 如果斜率不为无穷大
                lx, rx = min(cue.x, sym_x), max(cue.x, sym_x)       # lx,rx为线段的左右端点
                lx = int((lx - self.ball) // (self.length - 2*self.ball)) + 1   # 计算lx在镜像坐标系的索引
                rx = int((rx - self.ball) // (self.length - 2*self.ball)) + 1   # 计算rx在镜像坐标系的索引
                for x in range(lx, rx):
                    y = fx(x * (self.length - 2*self.ball) + self.ball)     # 计算线段在镜像桌面左右库边的交点
                    crossCoord.append((x * (self.length - 2*self.ball) + self.ball, y))
            if fy:  # 如果斜率不为0
                ly, ry = min(cue.y, sym_y), max(cue.y, sym_y)
                ly = int((ly - self.ball) // (self.width - 2*self.ball)) + 1
                ry = int((ry - self.ball) // (self.width - 2*self.ball)) + 1
                for y in range(ly, ry):
                    x = fy(y * (self.width - 2*self.ball) + self.ball)
                    crossCoord.append((x, y * (self.width - 2*self.ball) + self.ball))
            if cue.x < sym_x:   # 如果母球在目标球左侧
                crossCoord = sorted(crossCoord, key=lambda x: x[0]) # 按照x坐标从小到大排序
            else:
                crossCoord = sorted(crossCoord, key=lambda x: -x[0])    
            for x, y in crossCoord:
                x, y = self.convert(x, y)   # 将镜像坐标转换为原坐标
                solutions.append((x, y))    # 加入碰撞点坐标
            solutions.append((target.x, target.y))       # 加入目标球坐标
            if self.valid(solutions, target):       # 如果路线不掉库且不碰其他的球
                return_solutions.append(solutions)
        return return_solutions

table = Table()
max_num, num = 1, 0
for cursion in range(8):
    solutions = table.solution("brown", cursion)
    for solution in solutions:
        table.show(solution)
    #     num += 1
    #     if num >= max_num:
    #         break
    # if num >= max_num:
    #     break