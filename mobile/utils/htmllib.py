#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''

import logging
from BeautifulSoup import BeautifulSoup
from BTSelector import findAll
from urllib2 import urlopen
from urllib2 import URLError
from HTMLParser import HTMLParser
import exceptions
import re
import urlparse
import mimetypes
import datetime
import StringIO
import struct
import gbtools

def parsehtml(html_content, feed, feed_url, url):
		start_target = feed.start_target
		allow_target = feed.allow_target
		mid_target = feed.mid_target
		end_target = feed.end_target
		stop_target = feed.stop_target
		pagehtml = decoding(html_content)
		target = decoding(start_target)
		if not stop_target or stop_target == 'nohtml':
				stop_target = None
		else:
				stop_target = encoding(stop_target, 'utf-8')
		ret = ''
		try:
			"""
			解析元数据和url
			"""
			soup = BeautifulSoup(pagehtml, fromEncoding="utf-8")
			try:
				tret = findAll(target, soup)
				"""
				may be somethimes,when we type the tag like p,there will raise error
				because the tret is a list and str(tret) is not fit for us,
				so there we use join to change it
				"""
				tret = ''.join('%s' % tmpstr for tmpstr in list(tret))
				if stop_target:
					tret = tret.split(stop_target)[0]
				minisoup = BeautifulSoup(tret, fromEncoding="utf-8")
				minisoup.prettify()
				ret = GetAllclean(mid_target, end_target, allow_target, url, minisoup)
				if len(ret) == 0:
					logging.error('The feed %s `s target %s is bad target', feed_url, target)
					return None
				else:
					logging.info('add the new article now,the new one len to %s,type to %s', len(ret), type(ret))
					return ret
			except  Exception, data:
				logging.error('something is wrong at url %s ,the error is %s ', feed_url, data)
				return None

		except Exception:
			logging.error('Could not parse this,the html has misstake is %s', feed_url)
			return None


def encoding(s, dtype=None, ftype=False):
	"""
	this def is used for Automatic encode string
	s:the string
	dtype:the encode type,like str.encode(dtype)
	ftype:the bool,if True,it will force Transform
	"""
	if ftype == False:
		if not isinstance(s, unicode):
			s = decoding(s)
			logging.info('not unicode')
		if dtype != None:
			try:
				ce = s.encode(dtype)
				return ce
			except UnicodeEncodeError:
				return s
		else:
			cl = ['utf-8', 'gb2312', 'GB18030']
			ce = s
			for a in cl:
				try:
					ce = s.encode(a)
					break
				except UnicodeEncodeError:
					pass
			return ce
	else:
			try:
				if dtype == None:
					dtype = 'utf-8'
					ce = decoding(s).encode(dtype)
				return ce

			except Exception, date:
				return s






def decoding(s):
	if isinstance(s, unicode):
		return s
	else:
		ce = ''
		cl = ['utf-8', 'gb2312', 'GB18030']
		s = gbtools.stringQ2B(s)
		result = False
		for a in cl:
			try:
				ce = s.decode(a)
				result = True
				break
			except UnicodeDecodeError, data:
				result = False
				pass
		if result:
				return ce
		else:
				return s



def GetAllclean(mid_target, end_target, allow_target, url, soup, open=None):
			soup = do_imgclean(url, soup)
			if mid_target != 'nohtml':
					mid_clean = do_midclean(mid_target, soup)
					if end_target != 'nohtml':
							end_clean = do_endclean(end_target, mid_clean, allow_target)
							soup = end_clean
					else:
							soup = mid_clean
			else:
					if end_target != 'nohtml':
							end_clean = do_endclean(end_target, soup, allow_target)
							soup = end_clean
					else:
							soup = soup
			soup.prettify()
			return do_str(soup)

def GetFeedclean(url, pagehtml, stop_target):
		if stop_target:
					pagehtml = pagehtml.split(stop_target)[0]
		soup = BeautifulSoup(pagehtml, fromEncoding="utf-8")
		url = geturl(url)
		soup = do_imgclean(url, soup)
		soup = do_midclean('nohtml', soup)
		soup = do_endclean('nohtml', soup, 'nohtml')
		soup.prettify()
		return do_str(soup)


def do_endclean(end_target, soup, allow_target):
		if allow_target == 'nohtml':
			valid_tags = u'p i strong b u a h1 h2 h3 br img div embed span'.split()
		else:
			valid_tags = decoding(allow_target).split()
		if end_target != 'nohtml' or len(end_target) != 0:
				valid_attrs = decoding(end_target).split()
		else:
				valid_attrs = u'src allowscriptaccess allowNetworking pluginspage width allowScriptAccess type wmode height quality invokeurls allownetworking invokeURLs'.split()
		for tag in soup.findAll(True):
				if tag.name not in valid_tags:
						#tag.hidden = True
						tag.attrs = [(attr, val) for attr, val in tag.attrs
						if attr in valid_attrs]
						tag.extract()
		return soup

def do_midclean(mid_target, soup):
		if mid_target != 'nohtml' or len(mid_target) != 0:
				nvalid_vals = decoding(mid_target).split()
		else:
				nvalid_vals = u'ad1 ad2 href text/javascript st-related-posts h4 tags meta crinfo style randompost subscribe-af'.split()
		soup.findAll(nvalid_vals)
		soup.extract()
		for tags in soup.findAll(True):

				for attr, val in tags.attrs:
						if (val in nvalid_vals) or (attr in nvalid_vals):
								tags.extract()
		return soup
def Filter_html(content):
		tmpstr = re.sub(r'<[^>]+>', '', content)
		tmpstr = re.sub(r'&[^&]+;', '', tmpstr)
		tmpstr = re.sub(r'&copy;', '', tmpstr)
		return tmpstr

def Filter_content(content):
		tmpstr = re.sub(r'&nbsp;', '', content)
		tmpstr = re.sub(r'&copy;', '', tmpstr)
		return tmpstr
def do_str(soup):
		result = soup.renderContents().decode('utf8')
		if isinstance(result, list):
			return result[0]
		else:
			return result

def do_imgclean(url, soup):
		oldsrc = ''
		newimg = ''
		for cimg in soup.findAll('img'):
				if 'http://' in cimg['src']:
						pass
				else:
						oldsrc = cimg['src']
						newimg = urlparse.urljoin(url, oldsrc)
						cimg['src'] = newimg
		return soup

def geturl(url):
		parsedTuple = urlparse.urlparse(url)
		url = "http://" + parsedTuple.hostname
		return url


def send_data(name, filename, fd, ordurl):
		boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
		buffer_len = 0
		buffer = ''
		buffer += '--%s\r\n' % boundary
		buffer += 'Content-Disposition: form-data; name=ordurl\r\n'
		buffer += '\r\n'
		buffer += ordurl + '\r\n'
		buffer += '--%s\r\n' % boundary
		if isinstance(filename, unicode):
			filename = name.encode('UTF-8')
		buffer += '--%s\r\n' % boundary
		buffer += 'Content-Disposition: form-data; name="%s"; filename="%s";\r\n' \
				% (name, filename)
		buffer += 'Content-Type: %s\r\n' % get_content_type(filename)
		buffer += 'Content-Length: %s\r\n' % len(fd)
		buffer += '\r\n'
		buffer += fd
		buffer += '\r\n'
		buffer += '--%s--\r\n' % boundary
		buffer += '\r\n'
		buffer_len = len(buffer)
		return buffer_len, buffer

def sid():
		now = datetime.datetime.now()
		return now.strftime('%y%m%d%H%M%S') + str(now.microsecond)

def get_content_type(filename):
		return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def Parse_images_url(content):
		try:
			content = gbtools.stringQ2B(encoding(content))
			img = re.compile(r"""<img\s.*?\s?src\s*=\s*['|"]?([^\s'"]+).*?>""", re.I)

			m = img.findall(content)
			return m
		except Exception, data:
			logging.info('the error of Parse_images is %s', data)
			return None

def getImageInfo(data):
	data = str(data)
	size = len(data)
	height = -1
	width = -1
	content_type = ''
	# handle GIFs
	if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
		# Check to see if content_type is correct
		content_type = 'image/gif'
		w, h = struct.unpack("<HH", data[6:10])
		width = int(w)
		height = int(h)
	
	elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n') and (data[12:16] == 'IHDR')):
		content_type = 'image/png'
		w, h = struct.unpack(">LL", data[16:24])
		width = int(w)
		height = int(h)
	# Maybe this is for an older PNG version.
	elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
		# Check to see if we have the right content type
		content_type = 'image/png'
		w, h = struct.unpack(">LL", data[8:16])
		width = int(w)
		height = int(h)
		
	# handle JPEGs
	elif (size >= 2) and data.startswith('\377\330'):
		content_type = 'image/jpeg'
		jpeg = StringIO.StringIO(data)
		jpeg.read(2)
		b = jpeg.read(1)
		try:
			while (b and ord(b) != 0xDA):
				while (ord(b) != 0xFF): b = jpeg.read(1)
				while (ord(b) == 0xFF): b = jpeg.read(1)
				if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
					jpeg.read(3)
					h, w = struct.unpack(">HH", jpeg.read(4))
					break
				else:
					jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0]) - 2)
				b = jpeg.read(1)
			width = int(w)
			height = int(h)
		except struct.error:
			pass
		except ValueError:
			pass


	
	return content_type, width, height


class HTMLStripper(HTMLParser):

	def __init__(self):
		self.reset()
		self.fed = []
	
	def handle_data(self, d):
		self.fed.append(d)
	
	def get_data(self):
		text = ' '.join(self.fed)
		return re.sub(r'\s\s+', ' ', text)
	
	def get_edata(self):
		text = ' '.join(self.fed)
		return text

