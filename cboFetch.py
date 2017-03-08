#!/usr/bin/env python
#coding:utf-8
#Author:tenghou
import requests
from pyquery import PyQuery as pq
import csv
import os
import time

class cbograsp:
    """
    Attributes:
    filename: A csv file used for storing the data we get
    url: The website we fetch data from
    year_start: A integer store data of the year you need
                to fetch start
    year_end: A integer store data of the year you need
                to stop fetch
    """
    def __init__(self):
        self.filename = 'cboscvtest.csv'
        self.url = 'http://www.cbooo.cn/year?year=2012'
        self.year_start = 2012
        self.year_end = 2017

    def writecsv(self, data):
        '''
        write data into csv file
        a+ means add the data instead of cover it

        Args:
            data: A list used for temp data store
        '''
        csvfile = file(self.filename, 'ab+')
        writer = csv.writer(csvfile)
        writer.writerow(data)
        csvfile.close()

    def findByTag(self, tag):
        '''
        from the html source code we can know
        that the data we are interested
        are all contained in the td and th tag,
        and there is no other td and th tag
        so we can use this method to aquire the useful data

        Args:
            tag: A String store html tag we interested

        Returns:
             A unicode html source fetched
        '''
        result = requests.get(self.url)
        resultText = pq(result.text)
        tagContent = resultText(tag)

        return tagContent

    def insertinfo(self):
        '''
        list[0].split('') cost a lot of time!
        Args:
	        i: When data is stored 7 data, fresh data[]
	        which is to change another line in csv file
        '''
        th = self.findByTag('th')
        i = 0
        j = 0

        data = []
        title = []

        for nun in th:
            titleuni = pq(nun).text()
            titleRes = titleuni.encode('utf-8')
            #type(titleuni) : unicode
            title.append(titleRes)
            #print type(nun)
            if j == 0:
                title = title[0].split('\xef\xbc\x9a')
                j += 1
                #print title
        self.writecsv(title)

        for year in range(self.year_start, self.year_end+1):
            self.url = 'http://www.cbooo.cn/year?year=%d' % (year)
            td = self.findByTag('td')
            for num in td:
                datauni = pq(num).text()		
                data.append(datauni.encode('utf-8'))
                #print data

                if i % 7 == 0:
                    data = data[0].split(' ')

                i += 1
                if i % 7 == 0:
                    self.writecsv(data)
                    data = []

        print 'Data grasp and write successful!'

    def main(self):
        '''
        time.clock(): only calculate the cpu time that the program run
                      so time.sleep() will make no influence on it
        time.time(): calculate the whole run time 
        '''
        start = time.time()
        #time.sleep(3)

        #if the csvfile already exits, delete it
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.insertinfo()

        end = time.time()
        print 'It takes %f senconds to write csv file' % (end - start)

cbograsp = cbograsp()
cbograsp.main()
