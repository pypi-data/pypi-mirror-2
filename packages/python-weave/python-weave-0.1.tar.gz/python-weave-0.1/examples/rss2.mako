## -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:wfw="http://wellformedweb.org/CommentAPI/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
  xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
  xmlns:georss="http://www.georss.org/georss" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:media="http://search.yahoo.com/mrss/">
 <channel>
  <title>Bookmarks</title>
  <atom:link href="http://ziade.org/bookmarks/xml" rel="self" type="application/rss+xml" />
  <link>http://ziade.org/bookmarks</link>
  <description>Tarek's Bookmarks</description>
  <lastBuildDate>${last_build_date}</lastBuildDate>
  <language>en</language>
  <sy:updatePeriod>hourly</sy:updatePeriod>
  <sy:updateFrequency>1</sy:updateFrequency>
  <image>
    <url>http://www.gravatar.com/blavatar/107485281a5c5ceea5df5c78be3fd0d5?s=96&#038;d=http://s2.wp.com/i/buttonw-com.png</url>
    <title>Tarek's bookmark</title>
    <link>http://ziade.org/bookmarks</link>
  </image>
  %for item in items:
    <item>
      <title>${item.title}</title>
      <link>${item.link}</link>
      <pubDate>${item.date}</pubDate>
      <dc:creator>Tarek Ziadé</dc:creator>
      <category>bookmark</category>
      <description>${item.description}</description>
    </item>
  %endfor
 </channel>
</rss>