# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tool



class JDlogin(object):
    def __init__(self,un,pw,daterange):
        self.driver = webdriver.PhantomJS()
        self.basegoodsURL = "http://order.jd.com/center/list.action"
        self.login_url = "http://passport.jd.com/uc/login"
        self.un = un
        self.pw = pw
        self.daterange = daterange
        self.tool = tool.Tool() 
        

    
            
    

            
    def main(self):
        try:
            driver = self.driver
            driver.get(self.login_url + "?ReturnUrl=" + self.basegoodsURL)
            elem = driver.find_element_by_id("loginname")
            elem.send_keys(self.un)
            elem = driver.find_element_by_id("nloginpwd")
            elem.send_keys(self.pw)
            if self.daterange == "1":
               driver.find_element_by_id("loginsubmit").click()
               WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='time-list']/ul[1]/li[2]/a")))
               page = driver.page_source
               pageNum = self.tool.getPageNum(page)
               print(u"\n" + u"以下是第" + str(1) + u"页:")
               buydate = self.tool.getbuydate(page)
               orderid = self.tool.getorderid(page)
               shopname = self.tool.getshopname(page)
               cost = self.tool.getcost(page)
               paymethod = self.tool.getpaymethod(page)
               orderstatus = self.tool.getorderstatus(page)
               productnamesandamounts = self.tool.getproductnamesandamounts(page)
               rowspan = self.tool.getrowspan(page)
               self.tool.getGoodsInfo(rowspan,buydate,orderid,shopname,cost,paymethod,orderstatus,productnamesandamounts)
               if int(pageNum) != 1:
                   for x in range(2,int(pageNum)+1):
                       print(u"\n" + u"以下是第" + str(x) + u"页:")
                       
                       driver.find_element_by_xpath("//a[@class='next']").click()
                       time.sleep(10)
                       page = driver.page_source
                       buydate = self.tool.getbuydate(page)
                       orderid = self.tool.getorderid(page)
                       shopname = self.tool.getshopname(page)
                       cost = self.tool.getcost(page)
                       paymethod = self.tool.getpaymethod(page)
                       orderstatus = self.tool.getorderstatus(page)
                       productnamesandamounts = self.tool.getproductnamesandamounts(page)
                       rowspan = self.tool.getrowspan(page)
                       self.tool.getGoodsInfo(rowspan,buydate,orderid,shopname,cost,paymethod,orderstatus,productnamesandamounts)
            elif self.daterange == "2":
                driver.find_element_by_id("loginsubmit").click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='time-list']/ul[1]/li[2]/a")))
                elem = driver.find_element_by_css_selector(".ordertime-cont")
                ActionChains(driver).move_to_element(elem).perform()              
                elem.find_element_by_xpath("//div[2]/ul[1]/li[2]/a").click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='time-list']/ul[1]/li[2]/a[@class='curr']")))
                page = driver.page_source
                pageNum = self.tool.getPageNum(page)
                print(u"\n" + u"以下是第" + str(1) + u"页:")
                buydate = self.tool.getbuydate(page)
                orderid = self.tool.getorderid(page)
                shopname = self.tool.getshopname(page)
                cost = self.tool.getcost(page)
                paymethod = self.tool.getpaymethod(page)
                orderstatus = self.tool.getorderstatus(page)
                productnamesandamounts = self.tool.getproductnamesandamounts(page)
                rowspan = self.tool.getrowspan(page)
                self.tool.getGoodsInfo(rowspan,buydate,orderid,shopname,cost,paymethod,orderstatus,productnamesandamounts)
                if int(pageNum) != 1:
                    for x in range(2,int(pageNum)+1):
                        print(u"\n" + u"以下是第" + str(x) + u"页:")
                        
                        driver.find_element_by_xpath("//a[@class='next']").click()
                        time.sleep(10)
                        page = driver.page_source
                        buydate = self.tool.getbuydate(page)
                        orderid = self.tool.getorderid(page)
                        shopname = self.tool.getshopname(page)
                        cost = self.tool.getcost(page)
                        paymethod = self.tool.getpaymethod(page)
                        orderstatus = self.tool.getorderstatus(page)
                        productnamesandamounts = self.tool.getproductnamesandamounts(page)
                        rowspan = self.tool.getrowspan(page)
                        self.tool.getGoodsInfo(rowspan,buydate,orderid,shopname,cost,paymethod,orderstatus,productnamesandamounts)
                    
            else:
                print(u'您的输入有误!')
                
    
        except Exception as e:
            print (e)   
        finally:
            print(u"\n" + u"Done!")
                    
            
    
                
    
        
    

        


if __name__=="__main__":
    username = raw_input("plz enter username:")
    password = raw_input("plz enter password:")
    daterange = raw_input(unicode("获取近三个月订单，请输入1；获取今年内订单，请输入2\n",'utf-8').encode('gbk'))
    JD = JDlogin(username,password,daterange)
    JD.main()