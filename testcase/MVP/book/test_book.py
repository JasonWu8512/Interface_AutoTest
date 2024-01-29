# coding=utf-8
# @Time    : 2022/9/21 2:15 下午
# @Author  : Karen
# @File    : test_book.py


import pytest
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from business.MVP.book.ApiBook import ApiBook
from config.env.domains import Domains


@pytest.mark.MVP
class TestBook(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()#默认fat环境，最终以平台取值为准
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = g().get_guest_token()  # 创建游客并获取token
        ApiBaby(token=cls.guest_token).api_put_baby()  # 创建宝贝
        cls.guest = ApiBook(token=cls.guest_token)  # 创建游客实例

    def test_books_mine_read(self):
        """01）已读书籍列表"""
        resp = self.guest.api_books_mine_read()
        assert resp['code'] == 0
        assert resp['data']['books'] == []

    def test_books_mine_favorite(self):
        """02）我的收藏"""
        resp = self.guest.api_books_mine_favorite()
        assert resp['code'] == 0
        assert resp['data']['books'] == []

    def test_books(self):
        """03）查看某个级别的绘本"""
        resp = self.guest.api_books('L00')
        assert resp['code'] == 0
        assert resp['data']['books'][0]['id'] == 'B0000000000001'
        assert resp['data']['books'][0]['title'] == 'Big A, little a'
        assert resp['data']['books'][0]['level'] == 'L00'

        resp1 = self.guest.api_books('L01')
        assert resp1['code'] == 0
        assert resp1['data']['books'][0]['id'] == 'B0000001010103'
        assert resp1['data']['books'][0]['title'] == 'Playtime'
        assert resp1['data']['books'][0]['level'] == 'L01'

    def test_books_filters(self):
        """04）图书馆查找"""
        resp = self.guest.api_books_filters()
        assert resp['code'] == 0
        assert len(resp['data']['levels']) == 18
        assert len(resp['data']['themes']) == 20
        assert len(resp['data']['series']) == 5

    def test_books_album(self):
        """05）图书馆专辑详情页"""
        resp = self.guest.api_books_album('album_seriesbigcats')
        assert resp['code'] == 0
        assert resp['data']['ttl'] == '大猫英语分级阅读（上）'
        assert resp['data']['progress']['all'] == 69
        assert len(resp['data']['bookIds']) == 69
        assert len(resp['data']['books']) == 69

    def test_books_detail(self):
        """06）课程详情页"""
        resp = self.guest.api_books_detail('B9780007185436')
        assert resp['code'] == 0
        assert resp['data']['title'] == 'The Very Wet Dog'
        assert resp['data']['publisher'] == '柯林斯'
        assert resp['data']['series'] == '大猫分级阅读'
        assert resp['data']['cover'] == 'https://cdn.jiliguala.com/reading/page/cover/B9780007185436_cover.png'
        assert resp['data']['level'] == 'L01'
        assert resp['data']['coreWords'] == ["park", "pond", "car", "yard"]
        assert len(resp['data']['subLessons']) == 4

    def test_collect_book(self):
        """07）收藏绘本"""
        resp = self.guest.api_book_collect('B9780007185436')
        assert resp['code'] == 0
        assert resp['data'] == {}

        resp1 = self.guest.api_books_mine_favorite()
        assert resp1['code'] == 0
        assert resp1['data']['books'][0]['id'] == 'B9780007185436'

    def test_cancel_collect_book(self):
        """08）取消收藏绘本"""

        # 先收藏绘本
        resp = self.guest.api_book_collect('B9780007185436')
        assert resp['code'] == 0
        assert resp['data'] == {}

        # 再取消收藏
        resp1 = self.guest.api_book_cancel_collect('B9780007185436')
        assert resp1['code'] == 0
        assert resp1['data'] == {}

        # 查看收藏列表，应为空
        resp2 = self.guest.api_books_mine_favorite()
        assert resp2['code'] == 0
        assert resp2['data']['books'] == []

    def test_listen_lesson_progress(self):
        """09）听绘本完课上报"""

        sections = [{
            "isSelf": False,
            "id": "B9780007185436_p02b01",
            "realScore": -1,
            "score": -1
        }, {
            "id": "B9780007185436_p03b01",
            "isSelf": False,
            "score": -1,
            "realScore": -1
        }, {
            "score": -1,
            "isSelf": False,
            "id": "B9780007185436_p06b01",
            "realScore": -1
        }, {
            "id": "B9780007185436_p05b01",
            "realScore": -1,
            "score": -1,
            "isSelf": False
        }, {
            "score": -1,
            "id": "B9780007185436_p01b01",
            "realScore": -1,
            "isSelf": False
        }, {
            "isSelf": False,
            "id": "B9780007185436_p08b01",
            "realScore": -1,
            "score": -1
        }, {
            "realScore": -1,
            "score": -1,
            "isSelf": False,
            "id": "B9780007185436_p07b01"
        }, {
            "score": -1,
            "realScore": -1,
            "isSelf": False,
            "id": "B9780007185436_p04b01"
        }]

        words = [{
            "id": "V000334",
            "score": -1,
            "realScore": -1
        }, {
            "id": "V000334",
            "realScore": -1,
            "score": -1
        }, {
            "id": "V000060",
            "score": -1,
            "realScore": -1
        }, {
            "score": -1,
            "realScore": -1,
            "id": "V000060"
        }, {
            "realScore": -1,
            "id": "V001473",
            "score": -1
        }, {
            "realScore": -1,
            "score": -1,
            "id": "V001473"
        }, {
            "id": "V002625",
            "score": -1,
            "realScore": -1
        }, {
            "score": -1,
            "realScore": -1,
            "id": "V002625"
        }]

        resp = self.guest.api_book_progress('B9780007185436', 'B9780007185436B01', sections, words)
        assert resp['code'] == 0
        assert resp['data']['score'] == -1
        assert resp['data']['realScore'] == -1
        assert resp['data']['coin'] != ''

        # 听绘本完课结果页
        resp1 = self.guest.api_book_progress_result('B9780007185436', 'B9780007185436B01')
        assert resp1['code'] == 0
        assert resp1['data']['title'] == 'The Very Wet Dog'
        assert resp1['data']['cover'] == 'https://cdn.jiliguala.com/reading/page/cover/B9780007185436_cover.png'

    def test_record_lesson_progress(self):
        """10）录绘本完课上报"""
        sections = [{
            "score": 83,
            "realScore": 73,
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/B9780007185436_p04b01\/44ecb1367d094c9182a0f85c837374a8\/1663757595.mp3",
            "detail": [{
                "realScore": 89,
                "score": 89,
                "char": "in"
            }, {
                "score": 87,
                "char": "the",
                "realScore": 87
            }, {
                "char": "mud",
                "realScore": 43,
                "score": 43
            }],
            "id": "B9780007185436_p04b01",
            "isSelf": True
        }, {
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/B9780007185436_p01b01\/44ecb1367d094c9182a0f85c837374a8\/1663757578.mp3",
            "detail": [{
                "score": 55,
                "char": "the",
                "realScore": 55
            }, {
                "realScore": 94,
                "char": "very",
                "score": 94
            }, {
                "char": "wet",
                "realScore": 45,
                "score": 45
            }, {
                "realScore": 52,
                "char": "dog",
                "score": 52
            }],
            "score": 71,
            "id": "B9780007185436_p01b01",
            "isSelf": False,
            "realScore": 61
        }, {
            "score": 100,
            "id": "B9780007185436_p02b01",
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/B9780007185436_p02b01\/44ecb1367d094c9182a0f85c837374a8\/1663757585.mp3",
            "detail": [{
                "char": "in",
                "realScore": 88,
                "score": 88
            }, {
                "score": 93,
                "char": "the",
                "realScore": 93
            }, {
                "char": "car",
                "realScore": 93,
                "score": 93
            }],
            "realScore": 91,
            "isSelf": True
        }, {
            "id": "B9780007185436_p06b01",
            "realScore": 95,
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/B9780007185436_p06b01\/44ecb1367d094c9182a0f85c837374a8\/1663757605.mp3",
            "detail": [{
                "realScore": 96,
                "char": "in",
                "score": 96
            }, {
                "score": 96,
                "char": "the",
                "realScore": 96
            }, {
                "score": 94,
                "char": "car",
                "realScore": 94
            }],
            "score": 100,
            "isSelf": True
        }, {
            "id": "B9780007185436_p03b01",
            "realScore": 95,
            "score": 100,
            "isSelf": True,
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/B9780007185436_p03b01\/44ecb1367d094c9182a0f85c837374a8\/1663757590.mp3",
            "detail": [{
                "realScore": 96,
                "char": "in",
                "score": 96
            }, {
                "char": "the",
                "realScore": 98,
                "score": 98
            }, {
                "char": "park",
                "score": 92,
                "realScore": 92
            }]
        }, {
            "id": "B9780007185436_p07b01",
            "realScore": 41,
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/B9780007185436_p07b01\/44ecb1367d094c9182a0f85c837374a8\/1663757611.mp3",
            "isSelf": True,
            "score": 51,
            "detail": [{
                "score": 75,
                "char": "in",
                "realScore": 75
            }, {
                "score": 19,
                "realScore": 19,
                "char": "the"
            }, {
                "score": 29,
                "char": "yard",
                "realScore": 29
            }]
        }, {
            "detail": [{
                "realScore": 95,
                "score": 95,
                "char": "in"
            }, {
                "score": 96,
                "realScore": 96,
                "char": "the"
            }, {
                "score": 55,
                "char": "pond",
                "realScore": 55
            }],
            "score": 92,
            "realScore": 82,
            "id": "B9780007185436_p05b01",
            "isSelf": True,
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/B9780007185436_p05b01\/44ecb1367d094c9182a0f85c837374a8\/1663757600.mp3"
        }]

        words = [{
            "id": "V000060",
            "score": 94,
            "realScore": 94
        }, {
            "id": "V000060",
            "score": 94,
            "realScore": 94
        }, {
            "score": 92,
            "realScore": 92,
            "id": "V000334"
        }, {
            "score": 92,
            "id": "V000334",
            "realScore": 92
        }, {
            "score": 29,
            "realScore": 29,
            "id": "V002625"
        }, {
            "score": 29,
            "id": "V002625",
            "realScore": 29
        }, {
            "score": 55,
            "id": "V001473",
            "realScore": 55
        }, {
            "id": "V001473",
            "realScore": 55,
            "score": 55
        }]

        resp = self.guest.api_book_progress('B9780007185436', 'B9780007185436B02', sections, words)
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['score'] != ''
        assert resp['data']['realScore'] != ''
        assert resp['data']['coin'] != ''

        # 录绘本完课结果页
        resp1 = self.guest.api_book_progress_result('B9780007185436', 'B9780007185436B02')
        assert resp1['code'] == 0
        assert resp1['data']['title'] == 'The Very Wet Dog'
        assert resp1['data']['cover'] == 'https://cdn.jiliguala.com/reading/page/cover/B9780007185436_cover.png'
        assert resp1['data']['nReadDays'] == 1
        assert resp1['data']['nRecordedBooks'] == 1
        assert resp1['data']['shareCoin'] != ''
        assert resp1['data']['audios'] != ''

    def test_preview_lesson_progress(self):
        """11）单词预习完课上报"""
        sections = [{
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V002234/903073898cdf4c3da97aff6673a34f4d/1664264063153.mp3",
            "detail": [{
                "char": "ant",
                "realScore": 96,
                "score": 100
            }],
            "id": "V002234",
            "realScore": 96,
            "score": 100
        }, {
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V000011/903073898cdf4c3da97aff6673a34f4d/1664264039603.mp3",
            "detail": [{
                "char": "hat",
                "realScore": 0,
                "score": 10
            }],
            "id": "V000011",
            "realScore": 0,
            "score": 10
        }, {
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V000055/903073898cdf4c3da97aff6673a34f4d/1664264055393.mp3",
            "detail": [{
                "char": "apple",
                "realScore": 98,
                "score": 100
            }],
            "id": "V000055",
            "realScore": 98,
            "score": 100
        }, {
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V000043/903073898cdf4c3da97aff6673a34f4d/1664264047341.mp3",
            "detail": [{
                "char": "cat",
                "realScore": 95,
                "score": 100
            }],
            "id": "V000043",
            "realScore": 95,
            "score": 100
        }]
        words = [{
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V002234/903073898cdf4c3da97aff6673a34f4d/1664264063153.mp3",
            "id": "V002234",
            "realScore": 96,
            "score": 100
        }, {
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V000011/903073898cdf4c3da97aff6673a34f4d/1664264039603.mp3",
            "id": "V000011",
            "realScore": 0,
            "score": 10
        }, {
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V000055/903073898cdf4c3da97aff6673a34f4d/1664264055393.mp3",
            "id": "V000055",
            "realScore": 98,
            "score": 100
        }, {
            "audio": "https://qiniucdn.jiliguala.com/ggr/user_audio/V000043/903073898cdf4c3da97aff6673a34f4d/1664264047341.mp3",
            "id": "V000043",
            "realScore": 95,
            "score": 100
        }]
        resp = self.guest.api_book_progress('B0000000000001', 'B0000000000001W01', sections, words)
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['score'] == -1
        assert resp['data']['realScore'] == -1
        assert resp['data']['isSelf'] == True

    def test_wordgame_lesson_progress(self):
        """12）趣味练习完课上报"""
        sections = [{
            "id": "B0000000000001E02_sec05",
            "realScore": 100,
            "score": 100
        }, {
            "id": "B0000000000001E02_sec04",
            "knowledge": [{
                "type": "word",
                "id": "V000043"
            }],
            "realScore": 100,
            "score": 100
        }, {
            "id": "B0000000000001E02_sec03",
            "knowledge": [{
                "type": "word",
                "id": "V000055"
            }],
            "realScore": 100,
            "score": 100
        }, {
            "id": "B0000000000001E02_sec02",
            "knowledge": [{
                "type": "word",
                "id": "V001383"
            }],
            "realScore": 100,
            "score": 100
        }, {
            "id": "B0000000000001E02_sec01",
            "knowledge": [{
                "type": "word",
                "id": "V000043"
            }],
            "realScore": 100,
            "score": 100
        }]
        words = []
        resp = self.guest.api_book_progress('B0000000000001', 'B0000000000001E02', sections, words)
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['score'] == 100
        assert resp['data']['realScore'] == 100
        assert resp['data']['coin'] != ''

        # 趣味练习完课结果页
        resp1 = self.guest.api_book_progress_result('B0000000000001', 'B0000000000001E02')
        assert resp1['code'] == 0
        assert resp1['data']['title'] == 'Big A, little a'
        assert resp1['data']['cover'] == 'https://cdn.jiliguala.com/reading/page/cover/B0000000000001_cover.png?versionId=gSfXqCSp2TXpcL4_A1x478W5Eh8z.w0c'
        assert resp1['data']['nReadDays'] == 1
        assert resp1['data']['nRecordedBooks'] == 1
        assert resp1['data']['shareCoin'] != ''
        assert resp1['data']['audios'] == []

    def test_exercise_lesson_progress(self):
        """13）阅读理解完课上报"""
        sections = [{
            "id": "B0000000000001_sec01_01",
            "realScore": 100,
            "score": 100
        }]
        words = []
        resp = self.guest.api_book_progress('B0000000000001', 'B0000000000001E01', sections, words)
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['score'] == 100
        assert resp['data']['realScore'] == 100
        assert resp['data']['coin'] != ''

        # 阅读理解完课结果页
        resp1 = self.guest.api_book_progress_result('B0000000000001', 'B0000000000001E02')
        assert resp1['code'] == 0
        assert resp1['data']['title'] == 'Big A, little a'
        assert resp1['data']['cover'] == 'https://cdn.jiliguala.com/reading/page/cover/B0000000000001_cover.png?versionId=gSfXqCSp2TXpcL4_A1x478W5Eh8z.w0c'
        assert resp1['data']['nReadDays'] == 1
        assert resp1['data']['nRecordedBooks'] == 0
        assert resp1['data']['shareCoin'] != ''
        assert resp1['data']['audios'] == []

    def test_books_word(self):
        """14）课程详情页核心单词"""
        resp = self.guest.api_books_word('B0000000000001')
        assert resp['code'] == 0
        assert resp['data']['words'][0]['text'] == 'hat'