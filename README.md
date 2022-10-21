# 图像混合

一个适用于HoshinoBot的图像混合插件

### ★ 如果你喜欢的话，请给仓库点一个star支持一下23333 ★

## 本项目地址：

https://github.com/BeiYazi0/Img_Mix

## 部署教程：

1.下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

git clone https://github.com/BeiYazi0/Img_Mix

2.启用：

在 HoshinoBot\hoshino\config\ **bot**.py 文件的 MODULES_ON 加入 'Img_Mix'

然后重启 HoshinoBot

## 指令

【混合】 +序号+图片1+图片2

指定mask来对两张图片进行混合

【查模板】 +序号

查看指定的mask

【添加模板】 +模板名+图片

添加mask

## 效果

原图
![image](https://github.com/BeiYazi0/Img_Mix/blob/main/images/example/black1.jpg)
![image](https://github.com/BeiYazi0/Img_Mix/blob/main/images/example/white1.jpg)

指令
![image](https://github.com/BeiYazi0/Img_Mix/blob/main/images/example/mask5.png)
![image](https://github.com/BeiYazi0/Img_Mix/blob/main/images/example/mix5.png)

效果
![image](https://github.com/BeiYazi0/Img_Mix/blob/main/images/example/mix5_res.jpg)

## 备注

添加模板可以添加自己的mask，但是mask应当只能是是黑(0,0,0)白(255,255,255)两色。
