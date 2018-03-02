#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
from scrapy.http.request import Request
from scrapy.http import TextResponse
import time
import questionsManagement as qm

RUNNING_TIMES=10
CORRECT=True
class BotSpiders(scrapy.Spider):

    name = "bot"

    start_urls = [
        "https://www.frikitrivial.com/game.php",
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.qM = qm.QuestionsManagement()

    def parse(self,response):

        init_page = "https://www.frikitrivial.com"
        url = "https://www.frikitrivial.com/game.php"

        self.driver.get(init_page)
        i=0
        time.sleep(60)

        self.driver.get(url)

        while i < RUNNING_TIMES:
            CORRECT=True
            while CORRECT:

                d1 = self.driver.page_source.encode('utf-8')
                html = str(d1)
                response = TextResponse('none',200,{},html,[],None)

                question = response.xpath('/html/body/div[1]/div/div[3]/text()').extract_first()
                first_answer = response.xpath('/html/body/div[1]/div/a[1]/text()').extract_first()
                second_answer = response.xpath('/html/body/div[1]/div/a[2]/text()').extract_first()
                third_answer = response.xpath('/html/body/div[1]/div/a[3]/text()').extract_first()
                forth_answer = response.xpath('/html/body/div[1]/div/a[4]/text()').extract_first()

                qMResponse = self.qM.getAnswer(question, first_answer, second_answer, third_answer, forth_answer)

                if qMResponse[1] == -1:
                    answer = 4
                else:
                    answer = qMResponse[1]

                next = self.driver.find_element_by_xpath('/html/body/div[1]/div/a['+str(answer)+']')
                next.click()

                if self.driver.current_url == 'https://www.frikitrivial.com/end.php':
                    self.qM.processQuestion(qMResponse[1], qMResponse[0], 0)
                    CORRECT=False
                else:
                    self.qM.processQuestion(qMResponse[1], qMResponse[0], 1)

            self.driver.get(url)
            i+=1

        self.qM.backup()
        self.driver.close()
