# Hydro-Toolbox

[^_^]: # (For the girl who I missed and still miss now.)
[^_^]: # (Glad to see everything get well on you. Please carry it on, and be yourself.)
[^_^]: # (Sticking to the dream is a privilege, so jealious that you have that.)
[^_^]: # (Sadly but luckily end it before the gaps get beyond accross.)
[^_^]: # (All best wishes to you, HZC.)

Scripts and other Things for simplify graduation work, python takes the most part.  
为了简化项目工作而写的一些脚本，部分内容感谢 [@Null233](https://github.com/Null233) 的帮助  

**代码仅仅处于能用的状态,内部充斥着大量可改进部分,欢迎大佬补充,指正. 也欢迎大家fork, pull request或者发issue.**

## 重要声明
[`BullshitConverterRelease.py`](ArcGIS/BullshitConverterRelease.py)已经在中华人民共和国被申请为软件著作权登记（编号：2020SR1837990），其著作权归属[吉林大学](https://jlu.edu.cn)所有，在Github平台开源仅可为非商业使用，如需商业使用，请联系[吉林大学无形资产管理科](http://zchq.jlu.edu.cn/)。

## IMPORTANT STATEMENT

[`BullshitConverterRelease.py`](ArcGIS/BullshitConverterRelease.py) has been registered as a software copyright in PRC(No. 2020SR1837990). And the copyright belongs to [Jilin University](https://jlu.edu.cn). GitHub Version is only for non-commercial use. If there do be a commercial demand, please contact [Department of Intangible Asset Management, Jilin University](http://zchq.jlu.edu.cn/) FIRST.

## 本人平台
```
Win10 21h1
//ArcGIS 10.6 with python 2.7.14(64 bit)
ArcGIS 10.8 with python 2.7.16(32 bit)
ArcGIS Pro with python 3.3
Python 3.8.3(64 bit)
R 4.1.0(64 bit)
```
## 目前文件
[`Spilt.py`](Support/Split.py)(将总数据的CSV裁切为以日为文件的CSV).   
[`Met_Extraction.py`](Support/Met_Extraction.py)(提取.met中的数据并输出为CSV).  
[`BullshitConverter.py`](ArcGIS/BullshitConverter.py/)(将CSV文件转换为散点，再进行插值，裁剪，重采样).  
[`BullshitConverterRelease.py`](ArcGIS/BullshitConverterRelease.py)(为了完成软件著作权及提高实用性开发的功能较为齐全的版本).   
[`Extract.py`](Support/Extract.py)(将SLiM模型输出结果拆分为以站点为单位的文件以便于Excel分析).  
[`Check.py`](Support/Check.py)(验证两个ASCII文件所含区域是否一致，如不一样则输出结果以备查验，最终尝试填补，生成填补文件).   
[`to0.py`](Support/to0.py)(将Kriging法插值插出的负值修正为0).      
~~[`Raster_Mean_Calculation.py`](ArcGIS/Raster_Mean_Calculation.py)(计算栅格平均值并输出至csv文件中)~~.  
~~[`Raster_Mean_Calculation_with_Extraction.py`](ArcGIS/Raster_Mean_Calculation_with_Extraction.py)(计算根据指定区域裁剪完毕后输出的栅格平均值并输出至csv文件中).~~    
[`Raster_Calculator.py`](ArcGIS/Raster_Calculator.py)(调用栅格计算器进行一特定表达式计算).       
[`GLUE.py`](Support/GLUE.py)(采用似然函数法验证待选模型参数合理性，进而得出指定参数范围).  
[`ESA_Calculation`](ArcGIS/ESA_Calculation.py)(受CSDN大佬启发，结合Raster_Mean_Calculation_with_Extraction编写的批处理欧航局雪量数据程序).  
[`Extract_Interpolation`](ArcGIS/Extract_Interpolation.py)(为解决低分辨率数据造成的误差问题，将较低分辨率的数据提取至点，再进行插值裁切，间接提升分辨率).  
[`PointsGen.py`](ArcGIS/PointsGen.py)(为[`Extract_Interpolation`](ArcGIS/Extract_Interpolation.py)生成所需提取值-插值点).  
[`CMA_Extract.py`](Support/CMA_Exract.py)(针对中国国家气象科学数据中心的[中国地面气候资料日值数据集](http://data.cma.cn/data/cdcdetail/dataCode/SURF_CLI_CHN_MUL_DAY.html)提取指定要素，使之符合[SWAT Weather Generator](https://www.researchgate.net/publication/294535100_SWAT_Weather_Database)的数据输入要求).  
[`Another_CMA_Extract_R.r`](Support/Another_CMA_Extract_R.r)(为另外一种格式的中国国家气象科学数据中心的地面资料日值数据集，应师姐所需，采用R语言进行编写).   
[`Extract_Mean_Calc.py`](ArcGIS/Extract_Mean_Calc.py)(丢弃了上述划线脚本，重写了该脚本，其可将TXT的asc文件转为tif，按掩膜提取并计算提取后均值，并支持提取值至指定点).  
[`ClipH5.py`](Support/ClipH5.py)(提取指定H5文件的横纵坐标格,合并成为一行到csv).  
[`Pipe_Leak.py`](Support/Pipe_Leak.py)(按照指定坐标点，分割实测值数据，求解指定点组的方程并求出所有潜在交点，最终绘制到图上).  
[`Pipe_Pressure.py`](Support/Pipe_Pressure.py)(为阐明管道漏点位置-漏点大小对水流影响的软件，现已废弃，有结果文件作为参考).  
[`FixHeader.py`](Support/FixHeader.py)(为缺失文件头的.asc/txt文件添加文件头).  
## 文件格式说明
[ArcGIS](ArcGIS/)文件夹为需要[Esri ArcGIS arcpy](https://www.esri.com/arcgis-blog/products/arcgis-desktop/uncategorized/whats-new-in-arcmap-10-6/)作为前置.  
[Support](Support/)文件夹为支持类型的文件,具体需求会写在注释中.  
带`_tqdm`的文件为支持[tqdm](https://github.com/tqdm/tqdm)进度条,请检查是否安装.  
带`_Test`的文件夹为样例文件,数据已经改成无关数据,**除表示格式外无任何意义**.  

## TODO
1. √ 重写`BullshitConverter.py`使其支持多线程操作(一次处理上万个文件就已经暴露性能不足的问题),~~预计采用Hadoop解决~~;
2. 为`BullshitConverterRelease.py`等代码写一个用户友好的文档;
3. ~~模型敏感性分析(估计要花上一年时间);~~
4. 收集使用反馈和PR(梦里);
5. 待续(咕咕咕)

##  一些没用的碎碎念
1.  克里金(Kriging)法无法处理相同的数据列, 只能通过IDW等其他插值方法;  
2.  ETo主要计算方法为[Penman Monteith Equation](https://en.wikipedia.org/wiki/Penman%E2%80%93Monteith_equation),根据Wiki说明,[Priestley-Taylor Equation](https://en.wikipedia.org/wiki/Penman%E2%80%93Monteith_equation)法可以作为补充,在此视为可相互替代;  
3.  `BullshitConverter.py`里存在一个泰森多边形计算雨量的方法,但由于流域空间上的非均质性,无法用泰森多边形的雨量作为输入。在`BullshitConveterRelease.py`中删除了这个算法，请自行迁移;  
4.  建议处理流程一致，避免坐标变换，重采样等带来的坐标偏移问题;
5.  需要首先进行计算栅格统计参数后方可求栅格最大值，最小值等；
6.  栅格计算器(`RasterCalculator`)调用并不在`arcpy.sa`包中，需要在`arcpy.gp.RasterCalculator_sa`中引用；
7.  ArcGIS Python UI不支持多进程操作，大大拖慢了程序效率；
8.  在传递参数计算时采用了将数组置于方法内计算的方法将二维数组压缩为一维数组；
9.  多线程操作将尽可能采用根据CPU逻辑处理器数指定的线程池实现;
10. [GLUE(Generalised likelihood uncertainty estimation)](https://en.wikipedia.org/wiki/Generalised_likelihood_uncertainty_estimation)是一种水文模型不确定性分析的方法，由于wiki介绍过少，本人大体理解过程分为几个步骤：生成一系列参数组，并采用指定方法采样，将其作为模型输入；构造似然函数，求解出结果，验证估计值是否在置信区间内；统计符合要求的参数，观察分布特征；
11. 如根据掩膜提取等需要返回栅格的ArcGIS操作，并发多进程极易引发冲突。其原因为ArcGIS先在同一目录下处理缓存文件，后根据是否调用save方法决定是否转存或直接删除，其命名格式较为单一，因此在多进程并发操作中，极易引发文件冲突而导致进程阻塞或提前终止。在代码中，采用分别建立子文件夹并在每一次操作时单独指定工作空间可有效避免这一问题;
12. ArcGIS 10.2 涉及到sa包的时候，需要加入代码`arcpy.CheckOutExtension("spatial")`防止出现错误；
13. Python多进程操作map函数，传递参数仅为一个。如有需要请考虑封装成一个参数进行执行。其函数返回值可通过get方法获取以List为单位的数据;
14. Python的`Extend`和`Append`在处理多维数组时存在一定区别，如想追加到已有记录尾部，请考虑使用`Append`方法;  
15. R语言和pandas有点意思嗷;
16. 屌我唔想返工啊！  
17. 待续...  
