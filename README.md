# myspider

## 京东登录并获取订单

原本想通过requests.session()的方式模拟登录并获取订单页，但由于页面用到了JavaScript，无法获取完整的订单信息，于是换成Selenium + PhantomJS的方式。

## 获取58同城二手手机信息

0. 采用了scrapy-redis做了一个分布式的爬虫。最后用mysql存储数据。需要事先安装以及配置好redis以及mysql。
1. 进入工程后，scrapy crawl 58spider_shouji运行这个命令就会开始爬各手机型号页面以及对应页码直到最后结束。
2. scrapy crawl myspider_58运行这个命令就会开始爬取具体的个人卖家的信息，会存储在相应的mysql表中。
3. 需要在redis中给出初始页面(lpush myspider:58_urls http://su.58.com/shouji/)。
4. 上述2个爬虫都可以多开来达到多进程爬取的效果。
5. 测试使用了3台centos VPS主机，一台作为redis的master端，另两台作为slave端。故需在settings.py文件中分别配置redis信息。
6. master端运行scrapy crawl 58spider_shouji，两台slave端运行scrapy crawl myspider_58，master端redis中给出初始页面，可以看到所有爬虫都动起来。
7. 可在master端的数据库表中查看爬取到的数据。

## 利用cookie直接登录知乎

先使用账号密码登录，在放.py文件的目录会生成一个cookies文件，再次运行则会使用cookie直接登录。
