# -*- coding: utf-8 -*-
import scrapy
import re

class SpiderShenzhenSpider(scrapy.Spider):
    name = 'spider_shenzhen'

    start_urls = ['http://www.szjs.gov.cn/bsfw/jggs/sgxk/']
    # urls = 'http://portal.szjs.gov.cn:8888/gongshi/sgxkList.html?page=1&qymc=&ann_serial=&pro_name='
    # urls = 'http://portal.szjs.gov.cn:8888/gongshi/sgxkList.html?page=1369&qymc=&ann_serial=&pro_name='
    def start_requests(self):
        for i in range(400,600):
            urls = 'http://portal.szjs.gov.cn:8888/gongshi/sgxkList.html?page={}&qymc=&ann_serial=&pro_name='.format(str(i))
            yield scrapy.Request(url=urls,callback=self.get_parse,priority=1)
    def get_parse(self, response):
        r = response.xpath('//tr/td/a/@onclick').extract()
        for rs in r:
            r = re.match("serachbyId\('(.*?)','(.*?)'\)",rs)
            result1 = r.group(1)
            result2 = r.group(2)
            # print(result1,result2)
            content_url = 'http://portal.szjs.gov.cn:8888/gongshi/sgxkz.html?instanceGuid={}&yxtywlsh={}'.format(result1,result2)
            # print(content_url)
            test_url = 'http://portal.szjs.gov.cn:8888/gongshi/sgxkz.html?instanceGuid=4403062018002301&yxtywlsh=2018-0214'
            yield scrapy.Request(url=content_url,callback=self.get_one,priority=4)
    def get_one(self,response):
        result = response.xpath('//tr/td/text()').extract()
        print(result)
        # result_list = '_'.join(result)
        # re.findall()
        print(len(result))
        with open('test400-600.xlsx','a+',encoding='utf-8') as f:
            f.write(response.url+'\t')
            i = 1
            while i<len(result):
                # print(result[i-1].replace('\xa0',''),result[i].replace('\xa0',''))
                f.write(result[i].replace('\xa0','').replace('\n','').replace('\r','').replace('\t','')+'\t')
                i += 2
            f.write('\n')
