# 求解斯诺克解球线路

## 样例
2库解黑球线路（虽然一般不会解黑球，这只是做一个样例）

![image](https://github.com/user-attachments/assets/02c11bee-c729-4f35-a2f3-4127f0abd193)

3库解黑球线路

![image](https://github.com/user-attachments/assets/112f6c38-de18-44e0-b8fe-a7bcb4eabd94)

![image](https://github.com/user-attachments/assets/72a32337-c235-4767-b689-8decef58e37d)

![image](https://github.com/user-attachments/assets/562c66ce-df2b-4206-9be4-5e59a485f20a)

还有好几种解，就不放在这里了

4库解黑球线路

![image](https://github.com/user-attachments/assets/87b4ce65-721d-49c8-892a-62787e488c8a)

![image](https://github.com/user-attachments/assets/a937a872-ceed-48c7-84e1-216c1e7581b1)

没有5库线路，6库解球线路

![image](https://github.com/user-attachments/assets/b9213018-c67c-44f7-8edb-7355b1e560a8)

## 文件介绍
这是一个比较小的项目，使用了python的matpolotlib来画图，Table.py构建了斯诺克桌面的类，里面的参数设置按照了斯诺克标准设定
定义了Ball类，表示桌球

shape.py用来画图的，包括画圆Circle、矩形Rectangle、多边形Polygon、线Line

solution.py用来求解数学问题

## 函数功能
### shape.Circle
在shape.py中的Circle画圆，参数False指定了是否添加光影，想法就是在圆的左上角依次画亮度逐渐增加、半径逐渐减小的圆，先计算到最亮
rgb之间的差距，再将其等分为n分，构成rs，gs，bs，第i个圆圈的圆心到大圆中心x,y的距离为等比数列的求和，即1/2 + 1/4 + ... + 1/2^i，半径大小为大圆半径r*0.6/(i+1)
然后在(x+1, y-1)处绘制一个半径为r的黑色圆构成阴影，在(x-1,y+1)处绘制半径为r的白色圆构成亮圈，构成的效果如下图

![image](https://github.com/user-attachments/assets/2dfd4c8c-8afe-4b37-9fb6-338b15b78481)

### Table.__init__
__init__函数构建了所有球的字典，键为球的名称，值为Ball类型，可以自定义桌面的球的分布

### Table.show
show函数根据斯诺克桌子参数构建了球桌，依次构建球桌、棕色桌边、深绿色库边、开球区域、球洞以及球，如果solutions不是None，则将解球线路画出
球桌各个位置坐标如下图所示
