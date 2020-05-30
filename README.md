# Pys-for-ArcGIS

Python Scripts and other Things for simplify graduation work.  
为了简化项目工作而写的一些脚本，部分内容感谢 [@Null233](https://github.com/Null233) 的帮助  

**代码仅仅处于能用的状态,内部充斥着大量可改进部分,欢迎大佬补充,指正. 也欢迎大家fork, pullrequest或者发issue.**

## 本人平台
```
Win10 2004
ArcGIS 10.6 with python 2.7.14(64 bit)
ArcGIS 10.8 with python 2.7.16(32 bit)
Python 3.8.3(64 bit)
```
## 目前文件
[`Spilt.py`](Support/Split.py)(将总数据的CSV裁切为以日为文件的CSV).   
[`Met_Extraction.py`](Support/Met_Extraction.py)(提取.met中的数据并输出为CSV).  
[`BullshitConverter.py`](ArcGIS/BullshitConverter.py/)(将CSV文件转换为散点，再进行插值，裁剪，重采样).  
(如有需要会进行补充，没有需要就不会补充了) 
[`Extract.py`](Support/Extract.py)(将SLiM模型输出结果拆分为以站点为单位的文件以便于Excel分析)  
[`Check.py`](Support/Check.py)(验证两个ASCII文件所含区域是否一致，如不一样则输出结果以备查验，最终尝试填补，生成填补文件)  
[`to0.py`](Support/to0.py)(将Kriging法插值插出的负值修正为0)  
  
## 文件格式说明
[ArcGIS](ArcGIS/)文件夹为需要[Esri ArcGIS arcpy](https://www.esri.com/arcgis-blog/products/arcgis-desktop/uncategorized/whats-new-in-arcmap-10-6/)作为前置.  
[Support](Support/)文件夹为支持类型的文件,具体需求会写在注释中.  
带`_tqdm`的文件为支持[tqdm](https://github.com/tqdm/tqdm)进度条,请检查是否安装.  
带`_Test`的文件夹为样例文件,数据已经改成无关数据,**除表示格式外无任何意义**.  

## TODO
1. 重写`BullshitConverter.py`使其支持多线程操作(一次处理上万个文件就已经暴露性能不足的问题),预计采用Hadoop解决;
2. 模型敏感性分析（估计要花上一年时间）
3. 待续(咕咕咕)

##  一些没用的碎碎念
1.  克里金(Kriging)法无法处理相同的数据列, 只能通过IDW等其他插值方法;  
2.  ETo主要计算方法为[Penman Monteith Equation](https://en.wikipedia.org/wiki/Penman%E2%80%93Monteith_equation),根据Wiki说明,[Priestley-Taylor Equation](https://en.wikipedia.org/wiki/Penman%E2%80%93Monteith_equation)法可以作为补充,在此视为可相互替代;  
3.  `BullshitConverter.py`里存在一个泰森多边形计算雨量的方法,但由于流域空间上的非均质性,无法用泰森多边形的雨量作为输入;  
4.  建议处理流程一致，避免坐标变换，重采样等带来的坐标偏移问题;
5.  模型调节漫漫无期...;
6.  待续...  
