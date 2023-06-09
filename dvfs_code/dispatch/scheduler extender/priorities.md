1、优选阶段首先看一下有没有cpu状态不处于powersave模式的，有的话优先选择这样的节点，给其打比较高的分数。  

![img](./img/1.png)  

![img](./img/2.png)  


2、当选择到的节点是处于powersave模式下时，我们为该节点设置一个label，表示希望该节点的cpu所处的状态。  

![img](./img/3.png)  

![img](./img/4.png)  

![img](./img/5.png)  

