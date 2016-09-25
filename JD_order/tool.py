# -*- coding:utf-8 -*-

import re


class Tool:
 
    #初始化
    def __init__(self):
        pass
 
 
    #获得页码数
    def getPageNum(self,page):
        pattern = re.compile(u'<div class="pagin fr">.*?</span>.*?"text">共(.)页</span>',re.S)
        result = re.search(pattern,page)
        if result:
            pageNum = result.group(1).strip()
            print(u"共有" + str(pageNum) + u"页订单")
            return pageNum
        
    def getshopname(self,page):
        pattern = re.compile(u'<.*?class="shop-.*?>(.*?)</.*?"联系.*?</a>',re.S)
        shopname = re.findall(pattern,page)
        return shopname
        
    def getbuydate(self,page):
        pattern = re.compile(u'<tbody id="tb-.*?"dealtime".*?>(.*?)</span>',re.S)
        buydate = re.findall(pattern,page)
        return buydate
        
        
    def getorderid(self,page):
        pattern = re.compile(u'<a.*?orderIdLinks.*?>(.*?)</a>',re.S)
        orderid = re.findall(pattern,page)       
        return orderid
        
    def getpaymethod(self,page):
        pattern = re.compile(u'<span class="ftx-13">(.*?)</span>',re.S)
        paymethod = re.findall(pattern,page)
        return paymethod
        
    def getcost(self,page):
        pattern = re.compile(u'<span>总额 ¥(.*?)</span>',re.S)
        cost = re.findall(pattern,page)
        return cost
        
    def getorderstatus(self,page):
        pattern = re.compile(u'<div class="status.*?span class="order-status.*?>(.*?)</span>',re.S)
        orderstatus = re.findall(pattern,page)
        return orderstatus
        
    def getproductnamesandamounts(self,page):
        patterna = re.compile(u'<a href=.*?class="a-link".*?>(.*?)</a>',re.S)        
        productnames = re.findall(patterna,page)
        patternb = re.compile(u'<div class="goods-number">(.*?)</div>',re.S)
        productamounts = re.findall(patternb,page)
        productnamesandamounts = []
        for x in range(len(productnames)):
            content = [productnames[x],productamounts[x]]
            productnamesandamounts.append(content)
        
        return productnamesandamounts       
        
    def getrowspan(self,page):
        pattern = re.compile(u'<td rowspan="(.)" id="operate.*?>',re.S)
        rowspan = re.findall(pattern,page)
        return rowspan
        
        
        
    def getGoodsInfo(self,rowspan,buydate,orderid,shopname,cost,paymethod,orderstatus,productnamesandamounts):
        
        for x in range(len(buydate)):
            print(u'------------------------------------------------------------')
            print u"购买日期:" + buydate[x].strip().encode('utf-8').decode('utf-8') + u"\0" + u"订单号:" + orderid[x].strip().encode('utf-8').decode('utf-8') + u"\0" + u"卖家店铺:" + shopname[x].strip().encode('utf-8').decode('utf-8') + u"\n"
            print u'宝贝名称:' 
            if int(rowspan[x].strip()) > 5:
                for i in range(5):
                    nameandamout = productnamesandamounts[i]
                    print nameandamout[0].strip().encode('utf-8').decode('utf-8') + u"\0" + u"\0" + nameandamout[1].strip().encode('utf-8').decode('utf-8')
                length = len(productnamesandamounts)
                productnamesandamounts = productnamesandamounts[5-int(length):]
            else:
                for i in range(int(rowspan[x].strip())):
                    nameandamout = productnamesandamounts[i]
                    print nameandamout[0].strip().encode('utf-8').decode('utf-8') + u"\0" + u"\0" + nameandamout[1].strip().encode('utf-8').decode('utf-8')
                length = len(productnamesandamounts)
                productnamesandamounts = productnamesandamounts[int(rowspan[x].strip())-int(length):]
            print u"\n" + u'总额:' + cost[x].strip().encode('utf-8').decode('utf-8') + u"元" + u"\0" + u'支付方式:' + paymethod[x].strip().encode('utf-8').decode('utf-8') + u"\0" + u'交易状态:' + orderstatus[x].strip().encode('utf-8').decode('utf-8')
    
    
 
    