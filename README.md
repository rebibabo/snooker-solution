![66074333f92130937e56f14100a01f1](https://github.com/user-attachments/assets/d12e31cf-5716-43db-a815-5132a0484c65)# 求解斯诺克解球线路

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
![微信图片_20240801142036](https://github.com/user-attachments/assets/f77c2095-1296-4afc-b420-4506322f0bd5)

### solution.symmetry
解球的原理就是反射角等于入射角，按照下面的方式就可以求解出碰库点的坐标，注意由于球有体积，因此实际翻转的桌面的宽度应该是width - 2 * ball

![289c9b3a3ceb187db09f1205abdf763](https://github.com/user-attachments/assets/8512f1d1-928e-4d12-988c-e76e5bed1241)

这个函数的功能将翻转n次所有的情况返回，例如当n=1的时候，表示可以弹一库，桌面可以镜像1次，镜像桌面和桌面坐标如下所示，其中(0,1)表示沿着右侧库边翻转1次
![image](https://github.com/user-attachments/assets/3ed3e822-cdde-4cec-850e-3b9a679a7409)


n=2时，表示可以弹2库，镜像桌面和坐标如下图所示
![image](https://github.com/user-attachments/assets/90f6f7ae-5d76-4096-9838-380facb5081b)

n=3时的坐标如下
![image](https://github.com/user-attachments/assets/873d114e-28e0-4ba8-aaf1-ed29a873e179)

可以找出来规律，首先一定包含(0,n), (n,0), (0,-n), (-n,0)的情况，然后依次可以和1, 2, 3...组合，直到n//2为止

例如3可以等于1+2，则由1和2可以构建8个镜像坐标：

(1,2), (1,-2), (-1,2), (-1,-2)

(2,1), (2,-1), (-2,1), (-2,-1)

当两个数相等时，则只能构建4个镜像坐标：

(2,2), (2,-2), (-2,2), (-2,-2)

这个symmetry函数输入n，返回所有镜像坐标列表，可以通过Table.show_symmetry显示镜像桌面

### 找到目标球的镜像坐标
如下图所示，镜像桌面(0,1)中的镜像目标球的y坐标可以通过镜像桌面的长度w'(=w-2*ball) + top + ball，x坐标不变

桌面(1,0)的目标球的x坐标的等于l'(=l-w*ball) + right + ball，y坐标不变

![微信图片_20240801150914](https://github.com/user-attachments/assets/8a5cdce2-0d1b-4edc-84f5-3e4add87e8bf)

当镜像坐标为2的倍数时，两次镜像效果抵消，如下图所示，镜像桌面(2,0)的镜像目标球的坐标为2*l' + left + ball
![微信图片_20240801152133](https://github.com/user-attachments/assets/8b9e085a-c8c2-4da9-b090-21825b91898b)

### solution.line
该函数输入两点的坐标，返回f(x)和f(y)，用于求解目标镜像球和母球的连线与镜像库边的焦点，如下图所示，为了求解碰库点1、2、3的坐标，通过连接镜像目标球和母球的连线与库边的交点可以1',2',3'而快速求得，在前面也分析到，当镜像桌面的坐标为偶数倍数时，镜像效果可以抵消，具体地，当镜像坐标位于(2k+1, 2k+2]之间，需要翻转坐标，在(2k, 2k+1]之间不变

例如在下图中，2’位于镜像库边的顶端，而实际的2’位于底端，而3’在镜像库边的底端，和3所处的一样
y
返回的第一个元素是f(x)，用于求解和y轴方向库边的y轴坐标，第二个元素是f(y)，用于求解x轴方向库边的x轴坐标

![66074333f92130937e56f14100a01f1](https://github.com/user-attachments/assets/d59ed1b0-8a82-48ab-8492-3fb1312d6600)

### Table.convert
该函数将连线焦点镜像坐标还原为在原始桌面的坐标，对于位于对称区间的坐标，无论x还是y，都可以通过下面的图片获得公式

x' = (k+1) * l' - x + 2 * ball

其中的k表示镜像桌面的坐标

k = (x - ball - 10e-6) // l'

这里减去10e-6是为了对齐整数区间[n, n+1)和对称区间(n, n+1]

![d6beb5ec3627cd07c55c15069e1f0ab](https://github.com/user-attachments/assets/e1984219-775e-4cf7-83f4-2f29ca16e6a8)

### Table.solution
这个函数综合了前面所有的计算过程，首先计算镜像桌面，求得镜像目标球坐标，然后连接母球和镜像目标球，求出来和镜像桌面的交点坐标，然后将交点坐标按照顺序排列，加入到solution解当中，solution以母球坐标开始，中间为碰库点坐标，最后一个元素为目标球坐标，然后就要验证每一个解是否符合以下要求：
1. 是否掉袋
2. 是否和球桌上其他球接触

#### Table.valid
该函数用于判断一组解是否符合要求，首先判断是否会调入6个袋，如果不是，再遍历除了母球、目标球之外所有的球，假设遍历球b，然后遍历求解线路，假设当前线段由(x1, y1), (x2, y2)组成，球b的坐标为(x,y)，首先要判断(x,y)是否在两线段的区域之间，

