import unittest
from spotify._mockspotify import mock_artistbrowse, mock_artist, mock_session
from tests import SkipTest

callback_called = False
callback_userdata = None

class TestArtistbrowser(unittest.TestCase):

    session = mock_session()
    artist = mock_artist("foo0", 1)

    def callback(browser, userdata):
        callback_called = True
        callback_userdata = userdata

    def test_is_loaded(self):
        browser = mock_artistbrowse(self.session, self.artist, 1, self.callback)
        assert browser.is_loaded()

    def test_is_not_loaded(self):
        browser = mock_artistbrowse(self.session, self.artist, 0, self.callback)
        assert not browser.is_loaded()

    def test_sequence(self):
        browser = mock_artistbrowse(self.session, self.artist, 1, self.callback)
        assert len(browser) == 3
        assert browser[0].name() == 'foo'
        assert browser[1].name() == 'bar'
        assert browser[2].name() == 'baz'

    def test_callback(self):
        raise SkipTest
        callback_called = False
        browser = mock_artistbrowse(self.session, self.artist, 0, self.callback,
                                   self)
        assert callback_called
        assert userdata is self
