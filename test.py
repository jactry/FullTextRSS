import justrss
_URL = 'http://www.guao.hk/feed'
_BEGIN = '<div class="content">'
_END = 'Related posts'
_RSSNAME = 'guao'
justrss.get_rss(_URL, _BEGIN, _END, _RSSNAME)
