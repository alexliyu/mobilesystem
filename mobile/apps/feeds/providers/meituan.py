#-*- coding:utf-8 -*-
"""
用于解析美团网xml接口.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

       
"""
from datetime import datetime, timedelta
import urllib, urllib2, re, email, feedparser, time, random, traceback, logging

from external_media import sanitise_html
from conf.settings import batch

from apps.feeds.providers import BaseFeedsProvider

__all__ = ['MeituanFeedsProvider']

def parse_date(s):
    return struct_to_datetime(feedparser._parse_date(s))
def struct_to_datetime(s):
    return datetime.fromtimestamp(time.mktime(s))

logger = logging.getLogger('apps.providers.feeds.rss')

class MeituanFeedsProvider(BaseFeedsProvider):
    verbose_name = 'MeiTuan'
    
    @batch('%d * * * *' % random.randint(0, 59))
    def import_data(self, metadata, output):
        "Pulls RSS feeds"

        from apps.feeds.models import Feed
        for feed in Feed.objects.filter(provider=self.class_path):
            output.write("Importing %s\n" % feed.title)
            try:
                self.import_feed(feed)
            except Exception, e:
                output.write("Error importing %s\n" % feed.title)
                traceback.print_exc(file=output)
                output.write('\n')
                logger.warn("Error importing feed %r" % feed.title, exc_info=True, extra={'url': feed.rss_url})
            
        return metadata
    def result_content(self, feed_data):
        html = ''
        html = "<li>商家名称:%s</li>" % feed_data.find('vendor_name').text
        html += "<li>商家网址：%s</li>" % feed_data.find('vendor_website_url').text
        html += "<li>开始时间:%s</li>" % parse_date(feed_data.find('start_date').text)
        html += "<li>结束时间：%s</li>" % parse_date(feed_data.find('end_date').text)
        html += "<li>已参与团购人数:%s人</li>" % feed_data.find('quantity_sold').text
        html += "<li>现价：%s元</li>" % feed_data.find('price').text
        html += "<li>原价：%s元</li>" % feed_data.find('value').text
        html += "<li>立即节省：%s元</li>" % feed_data.find('discount_amount').text
        html += "<li>折扣率：%s</li>" % feed_data.find('discount_percent').text
        html += "<li>图片：<img src=%s></li>" % feed_data.find('large_image_url').text
        html += "<li>简介:%s</li>" % feed_data.find('conditions').find('details').find('detail').text
        
        return html
        
    def import_feed(self, feed):
        from apps.feeds.models import Item
        import xml.etree.ElementTree as ET
        """
        获取美团网xml
        """  
        feed_tmp = urllib2.urlopen(feed.rss_url, timeout=30).read()
        """
        获取根
        """
        feed_xml = ET.fromstring(feed_tmp)
        feed_data = feed_xml.getchildren()[0].findall('deal')
        """
        获取xml发布日期
        """
        try:
            feed.last_modified = struct_to_datetime(feed_xml.attrib['date'])
        except:
            feed.last_modified = parse_date(feed_xml.attrib['date'])
            
        feed.save()
        
        items = set()
        """
        提取xml中的内容
        """
        for x_item in feed_data:
            guid, last_modified = x_item.find('title').text, parse_date(feed_xml.attrib['date'])
            
            for i in items:
                if i.guid == guid:
                    item = i
                    break
            else:
                try:
                    item = Item.objects.get(guid=guid, feed=feed)
                except Item.DoesNotExist:
                    item = Item(guid=guid, last_modified=datetime(1900, 1, 1), feed=feed)

            if True or item.last_modified < last_modified:
                item.title = x_item.find('title').text
                item.description = sanitise_html(self.result_content(x_item))
                item.link = x_item.find('deal_url').text
                item.small_image = x_item.find('medium_image_url').text
                item.big_image = x_item.find('large_image_url').text
                item.last_modified = last_modified
                item.save()
            
            items.add(item)
        
        for item in Item.objects.filter(feed=feed):
            if item not in items:
                item.delete()
        
        return items
