from xml.etree import ElementTree as ET
from datetime import datetime
import urllib, re, email, random, logging
import traceback

from django.template.defaultfilters import slugify

from mobile.molly.conf.settings import batch
from mobile.molly.apps.podcasts.providers import BasePodcastsProvider
from mobile.molly.apps.podcasts.models import Podcast, PodcastItem, PodcastCategory, PodcastEnclosure

from mobile.molly.apps.podcasts.providers.rss import RSSPodcastsProvider

logger = logging.getLogger(__name__)

class OPMLPodcastsProvider(RSSPodcastsProvider):
    def __init__(self, url, rss_re):
        self.url = url
        self.medium = None
        self.rss_re = re.compile(rss_re)
        self._category = None

    CATEGORY_ORDERS = {}

    CATEGORY_RE = re.compile('/([^\/]+)/([^,]+)')
    
    def extract_medium(self, url):
        return 'audio'
    
    def extract_slug(self, url):
        match_groups = self.rss_re.match(url).groups()
        return match_groups[0]
    
    def decode_category(self, attrib):
        if self._category is None:
            cat = 'Uncategorised'
        else:
            cat = self._category
        
        slug = slugify(cat)
        
        podcast_category, created = PodcastCategory.objects.get_or_create(slug=slug,name=cat)
        
        try:
            podcast_category.order = self.CATEGORY_ORDERS[slug]
        except KeyError:
            self.CATEGORY_ORDERS[slug] = len(self.CATEGORY_ORDERS)
            podcast_category.order = self.CATEGORY_ORDERS[slug]
        
        podcast_category.save()
        return podcast_category

    def parse_outline(self, outline):
        attrib = outline.attrib
        podcast, created = Podcast.objects.get_or_create(
            provider=self.class_path,
            rss_url=attrib['xmlUrl'])
        
        podcast.medium = self.extract_medium(attrib['xmlUrl'])
        podcast.category = self.decode_category(attrib)
        podcast.slug = self.extract_slug(attrib['xmlUrl'])
        
        self.update_podcast(podcast)

    @batch('%d * * * *' % random.randint(0, 59))
    def import_data(self, metadata, output):
        
        self._category = None

        xml = ET.parse(urllib.urlopen(self.url))

        rss_urls = []

        podcast_elems = xml.findall('.//body/outline')

        failure_logged = False

        for outline in podcast_elems:
            if 'xmlUrl' in outline.attrib:
                try:
                    self.parse_outline(outline)
                    rss_urls.append(outline.attrib['xmlUrl'])
                except Exception, e:
                    output.write("Update of podcast %r failed." % outline.attrib['xmlUrl'])
                    traceback.print_exc(file=output)
                    if not failure_logged:
                        logger.exception("Update of podcast %r failed.", outline.attrib['xmlUrl'])
                        failure_logged = True
            else:
                self._category = outline.attrib['text']
                # Assume this is an outline which contains other outlines
                for outline in outline.findall('./outline'):
                    if 'xmlUrl' in outline.attrib:
                        try:
                            self.parse_outline(outline)
                            rss_urls.append(outline.attrib['xmlUrl'])
                        except Exception, e:
                            output.write("Update of podcast %r failed." % outline.attrib['xmlUrl'])
                            traceback.print_exc(file=output)
                            if not failure_logged:
                                logger.exception("Update of podcast %r failed.", outline.attrib['xmlUrl'])
                                failure_logged = True
                self._category = None

        for podcast in Podcast.objects.filter(provider=self.class_path):
            if not podcast.rss_url in rss_urls:
                podcast.delete()
        
        return metadata