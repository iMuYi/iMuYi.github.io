---
title: 将Django搭建在Apache上
date: 2016-04-06 10:47:57
tags: Python,Django
categories: Django

---
前段时间，由于实验室项目的需要，要搭建一个web服务器，可怜我只会写python，所以就去研究了一下Django。学习Django是一个愉快的过程，本来就该如此嘛，Python提倡INTERESTING TO CODE，所以很快，我就完成了Django的本地部署，然而在把Django搭到服务器上的是，却是让我捣鼓了一个星期，真真是把我坑苦了。
<!--more-->
***
### 1.我的环境
在把Django搭建到Apache上时候，首先你需要明确你使用的**Django**和**Apache**的版本，嗯，还有**Python**的版本（<font color="gray">这很重要</font>）！

很多人依照网上的教程，BALABALA的输入`pip install Django`、`sudo apt-get install Apache2`，改了Apache配置文件，调了Django的setting，最后弄完了发现一直不成功，对着**命令**和**配置文件**看了半天也没发现有什么错误，怎么就一直不行呢？**很可能你一开始就错了呀！**人家是**Python2**，你的是**Python3**；人家的是**Apache2.2**，你的是**Apache2.4**。底子都不一样，搭起来能用才怪，所以第一步，一定要清楚自己的环境，具体的说就是你使用的版本号！

如果你是看我的文章，从头开始安装的话，那么我建议你使用`pip install Django==1.x`来代替`pip install Django`，甚至在你安装pip的时候，我都建议你明确的指明是用python2或者python3来安装（现在大多数的云服务器都包含Py2和Py3两个版本）。

接下来，我告诉你我搭建的环境，我的配置都是在此环境基础上配置的，如果其他环境，我了解我也会提一句。
* OS: Ubuntu 14.04
* Apache: Apache2.4
   `sudo apt-get install apache2  #安装Apache`
   `apachectl -v  #检查Apache版本，ubunt 14.04没经过其他设置，默认应该是Apache2.4`
* Python: Python2 
* Django: Django1.8
`pip install Django==1.8`
***
### 2.建立Python与Apache的链接
简单的来说就是**Apache**如何识别你的**Django**代码。无论如何，你的**Django**都是用Python写的，所以不恰当的说法就是给你的**Apache**安装**Python**解释器。

``` bash
sudo apt-get install libapache2-mod-wsgi      #Python2
sudo apt-get install libapache2-mod-wsgi-py3  #Python3
```

第一条是对于**Python2**用户的，第二条是对于**Python3**用户的。
>如果你是**Python2**用户又恰巧不小心输入了第二条命令，那么不要怕，再输入第一条命令就好啦，同样的**Python3**也可以通过再输入第二条命令来重置**Apache**的**Python**解释器（这种说法不一定对，但是我相信你懂我意思！）！

***
### 3.为Django安家，让Apache找到它
大致可以分为四步：
1. 将Django工程放在`/var/www/`下；
2. `sudo vi /etc/apache2/sites-available/yoursite.conf` 修改配置文件；
3. `sudo a2ensite yoursite.conf` 配置文件生效；
4. `sudo service apache2 restart` 重启Apache。

**Apache**默认的网站目录是`/var/www/`。通常来说，如果你只是自己搭着玩玩也没有必要更改这个目录，直接就将你的**Django工程文件夹**放在这就行了。

如果你想要放在别处的话，可以通过修改`/etc/apache2/apache2.conf`中的`<Directory /var/www>`，将其改为`<Directory /where/you/want>`，不过配套的你需要修改其权限。具体的修改方法[这里](http://www.ziqiangxuetang.com/django/django-deploy.html)。

以上只是完成了**为Django安家**这一步，但是我们还需要让**Apache找到Django**（方便查水表）。

新建一个网站配置文件：
``` bash    
sudo vi /etc/apache2/sites-available/yoursite.conf。
```
这里边包含了你所有的网站配置信息，包括Apache如何查找静态文件(`js/css/images`)，网站上传的文件存在哪里，最重要的，包含了**Apache**识别**Django**的**wsgi**文件。
``` bash
    #<VirtualHost *:80>
    ServerName www.yourdomain.com 
    #ServerAlias otherdomain.com
    #ServerAdmin youremail@gmail.com 

    # 存放用户上传图片等文件的位置，注意去掉#号
    #Alias /media/ /var/www/ProjectName/media/ 
                
    # 静态文件(js/css/images)的存放位置
    Alias /static/ /var/www/ProjectName/static/                
  
    # 允许通过网络获取static的内容
    <Directory /var/www/ProjectName/static/>                  
        Require all granted
    </Directory>

    # 最重要的！通过wsgi.py让Apache识别这是一个Django工程，别漏掉前边的 /
    WSGIScriptAlias / /var/www/ProjectName/ProjectName/wsgi.py     
    # wsgi.py文件的父级目录，第一个ProjectName为Django工程目录，第二个ProjectName为Django自建的与工程同名的目录
    <Directory /var/www/ProjectName/ProjectName/>                  
    <Files wsgi.py>
        Require all granted
    </Files>
    </Directory>

    </VirtualHost>
```
通过修改上面的文件，你就可以让**Apache**找到你的**Django**工程，上边可以修改的内容包括：

* 80：修改80为其他数字，可以更改你的端口号，国内的电信貌似把80端口给封了（如果你的域名没有备案的话）。**注意，还要修改`/etc/apache2/port.conf`文件中的`Listen port`**。
* ServerName：后边改成你自己的域名，如果没有的话就用IP代替。**注意，如果改成了域名，还需要修改Django工程下的`seeting.py`文件，将其`ALLOWED_HOSTS=[]`改为`ALLOWED_HOSTS=['www.yourdomain.com']`，多个域名可以通过逗号隔开**。
* ServerAlias：你的其他域名或IP。

最后要让这个配置文件生效，你需要运行
``` bash
sudo a2ensite yoursite.conf
```
有时候，你可能需要让它失效（因为你将yoursite.conf改名为其他名字？），可以运行
``` bash         
sudo a2dissite yoursite.conf
```
做完以上步骤，Apache会提醒你要执行`sudo service apache2 relaod`，这条命令主要是你手动**命令Apache根据你刚才配置的yoursite.conf去寻找Django工程**，当然我一般都是**restart**，如果你的**Apache**不为其他的网站提供服务，那么你也**restart**吧，因为**重启大法好**！
>每次你修改**Django**工程文件之后，都要**restart**一下，它才会生效。

***
### 4.修改Django的wsgi.py文件 
修改上面说的`/var/www/ProjectName/ProjectName/wsgi.py`为如下格式
``` python
        import os
        from os.path import join,dirname,abspath
        PROJECT_DIR = dirname(dirname(abspath(__file__)))

        import sys
        sys.path.insert(0,PROJECT_DIR)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examsys.settings")

        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
```
这个配置文件的作用也是让**Apache**找到**Djanog**，毕竟不能一厢情愿吗，**Apache**同意和**Django**“交往”了，但是万一人家**Django**不乐意呢？
最后，还记得我说的嘛？
>每次你修改**Django**工程文件之后，都要**restart**一下，它才会生效。

***
### 5.调试错误
1. 如果你的网站没有加载静态文件(`js/css/images`)，请检查你的静态文件是不是在`ProjectName/static`下，而不是在`ProjectName/AppName/static`下（改这里边的文件是不用重启**Apache**的）。
2. 不知道啥问题，就是不管用，请查看**Apache**的错误文档。
`cat /var/log/apache2/error.log`
3. **No module named xxxx**。首先检查一下你所依赖的库是否安装全了，没有的话就`pip install`。
4. **No module named django或者其他含django的错误**。这说明你的环境搭错了。往上翻error.log，找到AH00489开头的错误，看看你到底用的是什么环境。一般都是你第二步**Apache**的**Python**解释器安装错误。

以上皆参考涂伟忠老师的[自强学堂](http://www.ziqiangxuetang.com/django/django-deploy.html)，我自己搭建Django+Apache2时的心得，如果还不明白，可以去[自强学堂](http://www.ziqiangxuetang.com/django/django-deploy.html)看看。