1、对于正在capping的机器，我们不能迁移任务也不能向上面调度任务  



2、首先我们对机器进行功率监控，服务器功率超过一定阈值，我们开始进行迁移，否则不用迁移  


![](./img/2.png) 


3、我们迁移num次，num次以内，功率减低到一定阈值之下，则迁移成功  

![](./img/1.png) 

4、超过num次，则迁移失败，我们进行power capping  

![](./img/3.png) 