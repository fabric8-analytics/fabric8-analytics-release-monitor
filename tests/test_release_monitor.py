"""Unit tests for the release_monitor."""

# import pytest
import uuid
import os

from unittest import mock

from release_monitor.release_monitor import AbstractMonitor, Package, PypiMonitor, NPMMonitor

PYPI_FEED_EXAMPLE_OLD = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN"
 "http://www.rssboard.org/rss-0.91.dtd">
<rss version="0.91">
  <channel>
    <title>PyPI recent updates</title>
    <link>https://pypi.org/</link>
    <description>Recent updates to the Python Package Index</description>
    <language>en</language>
    <item>
      <title>rabird.qt 0.2.7</title>
      <link>https://pypi.org/project/rabird-qt/0.2.7/</link>
      <description>An extension library for Qt library</description>
      <pubDate>Wed, 09 Jan 2019 06:30:50 GMT</pubDate>
    </item>
    <item>
      <title>flask-forms 0.0.1</title>
      <link>https://pypi.org/project/flask-forms/0.0.1/</link>
      <description>JSON Support.</description>
      <pubDate>Wed, 09 Jan 2019 06:29:24 GMT</pubDate>
    </item>
    <item>
      <title>pymyob 1.1</title>
      <link>https://pypi.org/project/pymyob/1.1/</link>
      <description>A Python API around MYOB&#39;s AccountRight API.</description>
      <pubDate>Wed, 09 Jan 2019 06:27:48 GMT</pubDate>
    </item>
    <item>
      <title>peak-analysis-modified 0.2</title>
      <link>https://pypi.org/project/peak-analysis-modified/0.2/</link>
      <description>Gaussian Peak Analysis</description>
      <pubDate>Wed, 09 Jan 2019 06:24:08 GMT</pubDate>
    </item>
  </channel>
</rss>⏎"""

PYPI_FEED_EXAMPLE_NEW = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN"
 "http://www.rssboard.org/rss-0.91.dtd">
<rss version="0.91">
  <channel>
    <title>PyPI recent updates</title>
    <link>https://pypi.org/</link>
    <description>Recent updates to the Python Package Index</description>
    <language>en</language>
    <item>
      <title>bss-python 0.0.1</title>
      <link>https://pypi.org/project/bss-python/0.0.1/</link>
      <description>A small example package</description>
      <pubDate>Wed, 09 Jan 2019 06:31:47 GMT</pubDate>
    </item>
    <item>
      <title>rabird.qt 0.2.7</title>
      <link>https://pypi.org/project/rabird-qt/0.2.7/</link>
      <description>An extension library for Qt library</description>
      <pubDate>Wed, 09 Jan 2019 06:30:50 GMT</pubDate>
    </item>
    <item>
      <title>flask-forms 0.0.1</title>
      <link>https://pypi.org/project/flask-forms/0.0.1/</link>
      <description>JSON Support.</description>
      <pubDate>Wed, 09 Jan 2019 06:29:24 GMT</pubDate>
    </item>
    <item>
      <title>pymyob 1.1</title>
      <link>https://pypi.org/project/pymyob/1.1/</link>
      <description>A Python API around MYOB&#39;s AccountRight API.</description>
      <pubDate>Wed, 09 Jan 2019 06:27:48 GMT</pubDate>
    </item>
  </channel>
</rss>⏎"""

NPM_FEED_EXAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
    <channel>
        <title><![CDATA[npm recent updates]]></title>
        <description><![CDATA[Updates to the npm package registry]]></description>
        <link>https://www.npmjs.com/</link>
        <generator>RSS for Node</generator>
        <lastBuildDate>Thu, 10 Jan 2019 08:10:28 GMT</lastBuildDate>
        <atom:link href="https://registry.npmjs.org/-/rss" rel="self" type="application/rss+xml"/>
        <pubDate>Thu, 10 Jan 2019 08:10:28 GMT</pubDate>
        <language><![CDATA[en]]></language>
        <ttl>600</ttl>
        <item>
            <title><![CDATA[react-native-gizwits-sdk]]></title>
            <description><![CDATA[## Getting started]]></description>
            <link>https://npmjs.com/package/react-native-gizwits-sdk</link>
            <guid isPermaLink="true">https://npmjs.com/package/react-native-gizwits-sdk</guid>
            <dc:creator><![CDATA[gizwits-rbwang]]></dc:creator>
            <pubDate>Thu, 10 Jan 2019 08:09:58 GMT</pubDate>
        </item>
        <item>
            <title><![CDATA[dyn-formiojs]]></title>
            <description><![CDATA[Common js library for client side interaction with <form.io>]]>
            </description>
            <link>https://npmjs.com/package/dyn-formiojs</link>
            <guid isPermaLink="true">https://npmjs.com/package/dyn-formiojs</guid>
            <dc:creator><![CDATA[vchirkou]]></dc:creator>
            <pubDate>Thu, 10 Jan 2019 08:09:40 GMT</pubDate>
        </item>
        <item>
            <title><![CDATA[dynamo-entity-manager]]></title>
            <description><![CDATA[Entity manager for Amazon DynamoDB NoSQL database]]></description>
            <link>https://npmjs.com/package/dynamo-entity-manager</link>
            <guid isPermaLink="true">https://npmjs.com/package/dynamo-entity-manager</guid>
            <dc:creator><![CDATA[aitor.guerrero]]></dc:creator>
            <pubDate>Thu, 10 Jan 2019 08:09:37 GMT</pubDate>
        </item>
        <item>
            <title><![CDATA[react-native-apply-permission]]></title>
            <description><![CDATA[`$ npm install react-native-permission --save`]]></description>
            <link>https://npmjs.com/package/react-native-apply-permission</link>
            <guid isPermaLink="true">https://npmjs.com/package/react-native-apply-permission</guid>
            <dc:creator><![CDATA[imay]]></dc:creator>
            <pubDate>Thu, 10 Jan 2019 08:09:22 GMT</pubDate>
        </item>
        <item>
            <title><![CDATA[lemurro-client-metronic-core-frontend]]></title>
            <description><![CDATA[Javascript-ядро для Lemurro Web Client]]></description>
            <link>https://npmjs.com/package/lemurro-client-metronic-core-frontend</link>
            <guid isPermaLink="true">https://npmjs.com/package/lemurro-client-metronic-core-frontend
            </guid>
            <dc:creator><![CDATA[dimns]]></dc:creator>
            <pubDate>Thu, 10 Jan 2019 08:09:18 GMT</pubDate>
        </item>
    </channel>
</rss>
"""


class _TestingMonitor(AbstractMonitor):

    run = 0

    def fetch_feed(self):
        if _TestingMonitor.run == 0:
            _TestingMonitor.run += 1
            return set()
        elif _TestingMonitor.run == 1:
            _TestingMonitor.run += 1
            return {Package('a', '1'), Package('b', '2')}
        else:
            return {Package('a', '2'), Package('b', '2')}


def test_abstract_monitor_get_updated_packages():
    """Test set operations."""
    m = _TestingMonitor()
    assert len(m.get_updated_packages()) == 2
    assert len(m.get_updated_packages()) == 1
    assert len(m.get_updated_packages()) == 0


def test_pypi_monitor():
    """Test Pypi monitor using local files instead of the online feed."""
    dirname = '/tmp/' + str(uuid.uuid4()) + '/'
    rss_feed_dir = dirname + 'rss/'
    rss_feed_file = rss_feed_dir + 'updates.xml'
    os.mkdir(dirname)
    os.mkdir(rss_feed_dir)
    with open(rss_feed_file, 'w') as f:
        f.write(PYPI_FEED_EXAMPLE_OLD)

    url = 'file://' + dirname
    monitor = PypiMonitor(url)

    assert len(monitor.get_updated_packages()) == 0

    with open(rss_feed_file, 'w') as f:
        f.write(PYPI_FEED_EXAMPLE_NEW)

    assert len(monitor.get_updated_packages()) == 1
    assert len(monitor.get_updated_packages()) == 0


def test_npm_monitor_fetch_names():
    """Try to get names from the list above."""
    dirname = '/tmp/' + str(uuid.uuid4()) + '/'
    rss_feed_dir = dirname + 'rss/'
    rss_feed_file = rss_feed_dir + 'updates.rss'
    os.makedirs(rss_feed_dir)
    with open(rss_feed_file, 'w') as f:
        f.write(NPM_FEED_EXAMPLE)

    url = 'file://' + rss_feed_file
    monitor = NPMMonitor(url)

    pkgs = monitor.fetch_pkg_names_from_feed()

    assert 'dynamo-entity-manager' in pkgs
    assert 'lemurro-client-metronic-core-frontend' in pkgs


class MockRequestResponse:
    """Response similar to what you get from requests library. Duck typing in its beauty."""

    def __init__(self):
        """Mock member variables."""
        self.status_code = 200

    @staticmethod
    def json():
        """Mock method."""
        return {'latest': '1.3.5'}


def _mocked_npm_latest_version_request(_x, headers):
    assert headers
    return MockRequestResponse()


@mock.patch('requests.get', side_effect=_mocked_npm_latest_version_request)
def test_npm_latest_version_request(_foo):
    """Check the function for fetching the latest version."""
    version = NPMMonitor.fetch_latest_package_version('foobar')
    assert version == '1.3.5'


@mock.patch('requests.get', side_effect=_mocked_npm_latest_version_request)
def test_npm_monitor_fetch_feed(_foo):
    """Try to get packages from feed."""
    dirname = '/tmp/' + str(uuid.uuid4()) + '/'
    rss_feed_dir = dirname + 'rss/'
    rss_feed_file = rss_feed_dir + 'updates.rss'
    os.makedirs(rss_feed_dir)
    with open(rss_feed_file, 'w') as f:
        f.write(NPM_FEED_EXAMPLE)

    url = 'file://' + rss_feed_file
    monitor = NPMMonitor(url)

    pkgs = monitor.fetch_feed()

    assert Package('dynamo-entity-manager', '1.3.5') in pkgs
    assert Package('lemurro-client-metronic-core-frontend', '1.3.5') in pkgs


if __name__ == '__main__':
    pass
