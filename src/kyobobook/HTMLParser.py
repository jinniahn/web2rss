''' 
교보문고 신간 책 목록 분석

Feature:
  - 신간 페이지의 책들을 분석해서 데이터로 만든다.
     - 항목들:
'''

import requests
from pprint import pprint
from pyquery import PyQuery as pq

class HTMLParser(object):
    def __init__(self):
        this.url = 'http://www.kyobobook.co.kr/category/newCategoryBookKorList.laf?linkClass=33&mallGb=KOR&orderClick=da2&tabName=NewBook&targetPage='
    def get_page(self, page = 1):
        "파싱한 데이터를 가져온다."
        
        req = requests.get(this.url + page)
        html = req.text
        return html

    def parse_nextpage(self, page):
        "다음 페이지 번호를 가져온다. 만약 다음 페이지가 억으면 None을 리턴한다."

        h = pq(page)

        books = h('#detailList tr')
        next_page_num = None
        is_exists_nextpage = h('.paging_num img[alt="다음 페이지로 이동"]')[0].getparent().tag == a
        if is_exists_nextpage:
            #javascript:_go_targetPage('12')
            js = a.attrib('href')
            next_page_num = js.split("'")[1]
        return next_page_num

    def parse_page(self, page):
        "페이지에서 책 정보를 찾아서 리스트로 반환한다."
        
        h = pq(page)
        
        curpage = 1
        books = h('#detailList tr')

        book_list = []
        for book in books:
            book = pq(book)

            item = {}

            item["barcode"] = book('input[name="barcode"]')[0].attrib["value"]
            item["title"]   = book('dl.book_title dt a strong')[0].text
          
            d = book('dl.book_title dd')[0].text_content().replace("\t","").replace("\n","").replace("\xa0","").replace(" ","").split("|")
            item["author"]  = d[:-2]
            item["publisher"] = d[-2]
            item["pubDate"] = d[-1]
            item["description"] = book('dd.info')[0].text_content().replace("\t","").replace("\n","")
            item["image"] = book('.book_image img')[0].attrib['src']
            item["link"] = "http://www.kyobobook.co.kr/product/detailViewKor.laf?barcode=" + item['barcode']

            book_list.append(item)

        return book_list

        
    
        
        
