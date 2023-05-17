
操作顺序：
1: 如果有包没安装，就pip一下 requirements.txt
2: 打开GUI_Main.py


Elastic Deformation:  

1： 把需要处理的mask文件全部放在Mask_folder文件夹内,支持批量处理
2： 配置文件yaml放在config文件夹中
3： 输出文件夹默认位于outpus



注意事项（不断添加）：

如果在deformation后plot时，mask消失或没有达到预期数量，原因可能有一下几点：（2022/02/08）
	
	1：dice range设置的过于挑剔，没有产生达标的图像
	2：mask在某一个slice上太小（只有几个像素），变形之后导致消失

注意一下tk版本问题





