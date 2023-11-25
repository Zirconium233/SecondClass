### 第二课堂自动刷分脚本
#### 介绍：
这是`合肥工业大学`第二课堂小程序网络学习自动刷题脚本，主打轻量化电脑开机点一下就把今天的2点积分刷完。

---

*(原本想找一个改改凑合用的，但没发现这学校的，就自己搓了一个。)*
#### 使用教程：

首先说明：我没有做登录模块，这个登录跳转来跳转去的，一会重定向一会验证码，很麻烦，做这个登录搞不好登录占一半代码，还要用其他包，就不是很轻量化了。

---
使用步骤：
##### 1. 安装需求(前提你有python)。
```bash
pip install -r requirements.txt
```
或者
```bash
pip install requests
```
##### 2. 抓包
PS：如果你有好的手机抓包软件，那欢迎你使用，但是这里推荐用`fiddler`抓包，因为这个小程序支持电脑版，到时候复制粘贴也简单。
1. 安装fiddler，配置证书，过程可以参考：
https://zhuanlan.zhihu.com/p/410150022
2. 安装电脑版本微信，点第二课堂成绩单进入小程序就可以抓包了
3. 开着抓包，首先登录，用统一认证平台登录就可以了，进去后点进去网络学习模块，随便点一篇文章进去后，退出去。 *(进文章header才有secret)* 
4. 包抓完了，去每一个包请求头找有key session和secret二参数的(一般就是最后几个)，把值复制下来，粘贴到config.ini对应参数的后面，别忘了保存。
##### 3. 跑脚本
在此处打开终端：
```bash
python main.py
```
就跑起来了，如果没有报错，验收你的积分吧。
##### 4. 自动刷的方法
如果你经常忘记打开脚本，就像经常忘记刷分一样，那你可以尝试把整个脚本设置成开机自启动.
1. 一个我用过的方法是计划任务程序，打开任务计划程序，创建基本任务，把触发器选成登录时，执行的脚本选这个`main.py`，但请确认你这个`.py`的打开方式是`python.exe`而不是代码编辑程序。
2. 其他方法可以自己百度，比如注册表、启动文件夹这样的，我没专门试过，但你可以尝试。

---
#### 后续更新：
1. 有空可能会去补上`login`函数方便各位不抓包直接使用。
2. 如果文章类型不够，我会测试`视频类型`的答题代码，只不过每天最多得2分，更新的文章肯定不止2篇吧，应该数量是够的。
#### 关于代码的一些说明：
0. 这代码这么简单自己看也就明白了。
1. 学校的计时是本地开始的，服务器并不会关心你提交的时间，因此可以放心遍历每一个选项试错，直到通过为止。
*(原本打算接入GPT来答题的，结果：就这？)*
2. 代码目前遇到视频是自动跳过的，因为我没有抓过视频的包 
*(等3分钟不能切屏给我恶心到了，这辈子都不想看这个视频)*
但你可以尝试直接把跳转删了，大概率视频的答题自己就成功了，只不过文章类型的也很多，没必要这么做就是了。
3. 遍历多选题采用回溯法生成组合数，然后遍历每一个选项组合。