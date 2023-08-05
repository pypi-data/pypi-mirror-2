
from api_interface import interface as api_interface

from api_google_unit_env import env

# ------------------------------------------------------------------------------
# url generation
# ------------------------------------------------------------------------------

@env.depend(
  topic__url = api_interface.topic__url,
)
def test_url( topic__url ):
  url = topic__url( sample_topic )
  assert url == sample_url

# ------------------------------------------------------------------------------
# doc parsing
# ------------------------------------------------------------------------------

@env.depend(
  doc__images = api_interface.doc__images,
)
def test_parse( doc__images ):
  
  images = doc__images( sample_json )
    
  assert images == sample_images

# ------------------------------------------------------------------------------
# sample_data
# ------------------------------------------------------------------------------

sample_topic = 'obama'

sample_url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=obama&key=ABQIAAAA0hBN_e4XHbgeCGsAICczJxRvKsJ_v0SeGr5x17BErgd0djNAphRx7pdUBMI1jejS9TCsWeswxHAPJg'

sample_json = '''{"responseData": {"results":[{"GsearchResultClass":"GimageSearch","width":"350","height":"473","imageId":"rrTXR5huX-C_fM:","tbWidth":"95","tbHeight":"129","unescapedUrl":"http://robtshepherd.tripod.com/barack-obama.jpg","url":"http://robtshepherd.tripod.com/barack-obama.jpg","visibleUrl":"robtshepherd.tripod.com","title":"\u003cb\u003eBarack Obama\u003c/b\u003e","titleNoFormatting":"Barack Obama","originalContextUrl":"http://robtshepherd.tripod.com/illinois.html","content":"\u003cb\u003eBarack Obama\u003c/b\u003e","contentNoFormatting":"Barack Obama","tbUrl":"http://images.google.com/images?q\u003dtbn:rrTXR5huX-C_fM::robtshepherd.tripod.com/barack-obama.jpg"},{"GsearchResultClass":"GimageSearch","width":"800","height":"1000","imageId":"Kk2YHg2QDSqz6M:","tbWidth":"119","tbHeight":"149","unescapedUrl":"http://eev.liu.edu/KK/election/meetthecandidates/images/Barack%20Obama%20Capitol.jpg","url":"http://eev.liu.edu/KK/election/meetthecandidates/images/Barack%2520Obama%2520Capitol.jpg","visibleUrl":"eev.liu.edu","title":"Task","titleNoFormatting":"Task","originalContextUrl":"http://eev.liu.edu/KK/election/meetthecandidates/task.htm","content":"\u003cb\u003eBarack Obama\u003c/b\u003e","contentNoFormatting":"Barack Obama","tbUrl":"http://images.google.com/images?q\u003dtbn:Kk2YHg2QDSqz6M::eev.liu.edu/KK/election/meetthecandidates/images/Barack%2520Obama%2520Capitol.jpg"},{"GsearchResultClass":"GimageSearch","width":"407","height":"516","imageId":"wFOnQgcbwuGj6M:","tbWidth":"103","tbHeight":"131","unescapedUrl":"http://bpo.biz/bpo-news-blog/wp-content/uploads/2008/11/barack-obama1.jpg","url":"http://bpo.biz/bpo-news-blog/wp-content/uploads/2008/11/barack-obama1.jpg","visibleUrl":"www.bpo.biz","title":"BPO.biz : BPO Blog, BPO News, BPO Updates, Business Process \u003cb\u003e...\u003c/b\u003e","titleNoFormatting":"BPO.biz : BPO Blog, BPO News, BPO Updates, Business Process ...","originalContextUrl":"http://www.bpo.biz/bpo-news-blog/2008/11/","content":"\u003cb\u003ebarack\u003c/b\u003e-obama1.jpg","contentNoFormatting":"barack-obama1.jpg","tbUrl":"http://images.google.com/images?q\u003dtbn:wFOnQgcbwuGj6M::bpo.biz/bpo-news-blog/wp-content/uploads/2008/11/barack-obama1.jpg"},{"GsearchResultClass":"GimageSearch","width":"402","height":"477","imageId":"IulYvWe5X3xDkM:","tbWidth":"109","tbHeight":"129","unescapedUrl":"http://www.portlandart.net/archives/barack-obama-bw.png","url":"http://www.portlandart.net/archives/barack-obama-bw.png","visibleUrl":"www.portlandart.net","title":"PORT - Portland art + news + reviews","titleNoFormatting":"PORT - Portland art + news + reviews","originalContextUrl":"http://www.portlandart.net/archives/2009/04/interview_with_4.html","content":"\u003cb\u003eBarack Obama\u003c/b\u003e","contentNoFormatting":"Barack Obama","tbUrl":"http://images.google.com/images?q\u003dtbn:IulYvWe5X3xDkM::www.portlandart.net/archives/barack-obama-bw.png"}],"cursor":{"pages":[{"start":"0","label":1},{"start":"4","label":2},{"start":"8","label":3},{"start":"12","label":4},{"start":"16","label":5},{"start":"20","label":6},{"start":"24","label":7},{"start":"28","label":8}],"estimatedResultCount":"25300000","currentPageIndex":0,"moreResultsUrl":"http://www.google.com/images?oe\u003dutf8\u0026ie\u003dutf8\u0026source\u003duds\u0026start\u003d0\u0026hl\u003den\u0026q\u003dbarack+obama"}}, "responseDetails": null, "responseStatus": 200}'''

sample_images = [
  {'url': 'http://robtshepherd.tripod.com/barack-obama.jpg', 'title': u'<b>Barack Obama</b>'},
  {'url': 'http://eev.liu.edu/KK/election/meetthecandidates/images/Barack%2520Obama%2520Capitol.jpg', 'title': 'Task'},
  {'url': 'http://bpo.biz/bpo-news-blog/wp-content/uploads/2008/11/barack-obama1.jpg', 'title': u'BPO.biz : BPO Blog, BPO News, BPO Updates, Business Process <b>...</b>'},
  {'url': 'http://www.portlandart.net/archives/barack-obama-bw.png', 'title': 'PORT - Portland art + news + reviews'},
  ]

