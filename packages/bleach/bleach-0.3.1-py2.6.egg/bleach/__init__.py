import re
import string
import urllib

import html5lib
from sanitizer import BleachSanitizer
from encoding import force_unicode

ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
}

TLDS = (
    'ac',
    'ad',
    'ae',
    'aero',
    'af',
    'ag',
    'ai',
    'al',
    'am',
    'an',
    'ao',
    'aq',
    'ar',
    'arpa',
    'as',
    'asia',
    'at',
    'au',
    'aw',
    'ax',
    'az',
    'ba',
    'bb',
    'bd',
    'be',
    'bf',
    'bg',
    'bh',
    'bi',
    'biz',
    'bj',
    'bm',
    'bn',
    'bo',
    'br',
    'bs',
    'bt',
    'bv',
    'bw',
    'by',
    'bz',
    'ca',
    'cat',
    'cc',
    'cd',
    'cf',
    'cg',
    'ch',
    'ci',
    'ck',
    'cl',
    'cm',
    'cn',
    'co',
    'com',
    'coop',
    'cr',
    'cu',
    'cv',
    'cx',
    'cy',
    'cz',
    'de',
    'dj',
    'dk',
    'dm',
    'do',
    'dz',
    'ec',
    'edu',
    'ee',
    'eg',
    'er',
    'es',
    'et',
    'eu',
    'fi',
    'fj',
    'fk',
    'fm',
    'fo',
    'fr',
    'ga',
    'gb',
    'gd',
    'ge',
    'gf',
    'gg',
    'gh',
    'gi',
    'gl',
    'gm',
    'gn',
    'gov',
    'gp',
    'gq',
    'gr',
    'gs',
    'gt',
    'gu',
    'gw',
    'gy',
    'hk',
    'hm',
    'hn',
    'hr',
    'ht',
    'hu',
    'id',
    'ie',
    'il',
    'im',
    'in',
    'info',
    'int',
    'io',
    'iq',
    'ir',
    'is',
    'it',
    'je',
    'jm',
    'jo',
    'jobs',
    'jp',
    'ke',
    'kg',
    'kh',
    'ki',
    'km',
    'kn',
    'kp',
    'kr',
    'kw',
    'ky',
    'kz',
    'la',
    'lb',
    'lc',
    'li',
    'lk',
    'lr',
    'ls',
    'lt',
    'lu',
    'lv',
    'ly',
    'ma',
    'mc',
    'md',
    'me',
    'mg',
    'mh',
    'mil',
    'mk',
    'ml',
    'mm',
    'mn',
    'mo',
    'mobi',
    'mp',
    'mq',
    'mr',
    'ms',
    'mt',
    'mu',
    'museum',
    'mv',
    'mw',
    'mx',
    'my',
    'mz',
    'na',
    'name',
    'nc',
    'ne',
    'net',
    'nf',
    'ng',
    'ni',
    'nl',
    'no',
    'np',
    'nr',
    'nu',
    'nz',
    'om',
    'org',
    'pa',
    'pe',
    'pf',
    'pg',
    'ph',
    'pk',
    'pl',
    'pm',
    'pn',
    'pr',
    'pro',
    'ps',
    'pt',
    'pw',
    'py',
    'qa',
    're',
    'ro',
    'rs',
    'ru',
    'rw',
    'sa',
    'sb',
    'sc',
    'sd',
    'se',
    'sg',
    'sh',
    'si',
    'sj',
    'sk',
    'sl',
    'sm',
    'sn',
    'so',
    'sr',
    'st',
    'su',
    'sv',
    'sy',
    'sz',
    'tc',
    'td',
    'tel',
    'tf',
    'tg',
    'th',
    'tj',
    'tk',
    'tl',
    'tm',
    'tn',
    'to',
    'tp',
    'tr',
    'travel',
    'tt',
    'tv',
    'tw',
    'tz',
    'ua',
    'ug',
    'uk',
    'us',
    'uy',
    'uz',
    'va',
    'vc',
    've',
    'vg',
    'vi',
    'vn',
    'vu',
    'wf',
    'ws',
    'xn',
    'ye',
    'yt',
    'yu',
    'za',
    'zm',
    'zw',
)


url_re = re.compile(r'\b(?:[\w-]+:/{0,3})?(?<!@)[\w.-]+\.(?:(?:%s)\w*)(?:(?:\/|\?)\S*)?' % u'|'.join(TLDS))
proto_re = re.compile(r'^[\w-]+:/{0,3}')


NODE_TEXT = 4 # the numeric ID of a text node in simpletree


class Bleach:


    def bleach(self, string):
        """A shortcut to clean and linkify a string in one quick motion.

        Trade-off: only default configuration options."""

        return self.linkify(self.clean(string))


    def clean(self, string, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES):
        """Clean an HTML string and return it"""

        class s(BleachSanitizer):
            allowed_elements = tags
            allowed_attributes = attributes

        parser = html5lib.HTMLParser(tokenizer=s)

        return force_unicode(parser.parseFragment(string).toxml())


    def linkify(self, text, nofollow=True):
        """Convert URL-like strings in an HTML fragment to links.

        linkify() converts strings that look like URLs or domain names in a
        blob of text that may be an HTML fragment to links, while preserving
        (a) links already in the string, (b) urls found in attributes, and
        (c) email addresses.

        If the nofollow argument is True (the default) then rel="nofollow"
        will be added to links created by linkify() as well as links already
        found in the text.

        linkify() uses up to two filters on each link. For links created by
        linkify(), the href attribute is passed through Bleach.filter_url()
        and the text of the link is passed through filter_text(). For links
        already found in the document, the href attribute is passed through
        filter_url(), but the text is untouched.

        To implement custom filters, you should create a subclass of Bleach
        and override these functions.
        """

        parser = html5lib.HTMLParser()

        forest = parser.parseFragment(text)

        if nofollow:
            rel = u' rel="nofollow"'
        else:
            rel = u''

        def linkify_nodes(tree):
            for node in tree.childNodes:
                if node.type == NODE_TEXT:
                    new_frag = re.sub(url_re, link_repl, node.toxml())
                    new_tree = parser.parseFragment(new_frag)
                    for n in new_tree.childNodes:
                        tree.insertBefore(n, node)
                    tree.removeChild(node)
                else:
                    if node.name == 'a':
                        if nofollow:
                            node.attributes['rel'] = 'nofollow'
                        href = self.filter_url(node.attributes['href'])
                        node.attributes['href'] = href
                    else:
                        linkify_nodes(node)

        def link_repl(match):
            url = match.group(0)
            if re.search(proto_re, url):
                href = url
            else:
                href = u''.join(['http://', url])

            repl = u'<a href="%s"%s>%s</a>'

            return repl % (self.filter_url(href), rel,
                           self.filter_text(url))

        linkify_nodes(forest)

        return force_unicode(forest.toxml())


    def filter_url(self, url):
        """Applied to the href attribute of an autolinked URL"""
        return url


    def filter_text(self, url):
        """Applied to the innerText of an autolinked URL"""
        return url
