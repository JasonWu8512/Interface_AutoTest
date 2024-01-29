from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Jiliguala.operationAdmin.ApiCommonConfigInfo import ApiCommonConfigInfo
from utils.format.format import get_all_page, dateToTimeStamp, get_any_time, timeStampToTimeStr
from business.businessQuery import xshareQuery
import pytest
import random


@pytest.mark.xShareConfig
class TestCommonConfigInfo:
    xshareQuery = xshareQuery()
    plan_id = []

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.commonconfiginfo = ApiCommonConfigInfo(a_token)

    @classmethod
    def teardown_class(cls):
        """删除新增投放计划及其具体渠道"""
        cls.xshareQuery.delete_xshare_common_config(cls.plan_id)
        cls.xshareQuery.delete_xshare_advertising_plan(cls.plan_id)

    @pytest.fixture(scope='class')
    def get_one_commonconfig(self):
        """获取一个投放计划的配置"""
        res = self.commonconfiginfo.api_get_all_config()['data']
        print(self.commonconfiginfo.api_get_inner_config_detail(res['configs'][0]['id']))
        configdetail = self.commonconfiginfo.api_get_inner_config_detail(res['configs'][0]['id'])['data']
        return configdetail

    @pytest.fixture(scope='class')
    def get_backup_config(self):
        """获取兜底配置"""
        res = self.commonconfiginfo.api_get_inner_config_detail('0')['data']
        return res

    def test_add_config_all(self,get_one_commonconfig):
        """
        测试新增投放计划（不传id默认所有渠道）
        """
        before_res = get_one_commonconfig
        title = "新增投放" + ''.join(random.sample('0123456789',4))
        after_res = dict(before_res, **{"title": title, "sts": timeStampToTimeStr(int(dateToTimeStamp(min=-30))), "ets": timeStampToTimeStr(int(dateToTimeStamp(day=3, min=-10)))})
        del after_res['id']
        create_res = self.commonconfiginfo.api_edit_config(payload=after_res)
        recent_plan = self.commonconfiginfo.api_get_all_config()['data']['configs'][0]
        self.plan_id.append(recent_plan['id'])
        assert create_res['code'] == 0
        assert create_res['data']['campaign'] == recent_plan['id']
        assert recent_plan['title'] == title

    # @pytest.mark.parametrize("channel", ["unwechat", "unwechat_group", "wechat_mini", "wechat_mini_group", "wechat_web"])
    # def test_add_config_one_channel(self,get_one_commonconfig, channel):
    #     """
    #     测试新增投放计划（单个渠道）
    #     """
    #     before_res = get_one_commonconfig
    #     title = "新增单渠道投放" + ''.join(random.sample('0123456789', 4))
    #     after_res = dict(before_res, **{"title": title, "channel": channel,  "sts": timeStampToTimeStr(int(dateToTimeStamp(min=-30))), "ets": timeStampToTimeStr(int(dateToTimeStamp(day=3, min=-10)))})
    #     del after_res['id']
    #     create_res = self.commonconfiginfo.api_edit_config(payload=after_res)
    #     recent_plan = self.commonconfiginfo.api_get_all_config()['data']['configs'][0]
    #     self.plan_id.append(recent_plan['id'])
    #     assert create_res['code'] == 0
    #     assert create_res['data']['campaign'] == recent_plan['id']
    #     assert recent_plan['title'] == title

    def test_edit_config(self,get_one_commonconfig):
        """
        测试修改投放计划
        """
        channel_config = get_one_commonconfig
        title = "修改投放" + ''.join(random.sample('0123456789', 4))
        startAt, endAt = timeStampToTimeStr(int(dateToTimeStamp(min=-30))), timeStampToTimeStr(int(dateToTimeStamp(day=3, min=-10)))
        # 修改投放计划的有效时间和名称
        channel_config.update({"sts": startAt, "ets": endAt, "title": title})
        edit_res = self.commonconfiginfo.api_edit_config(payload=channel_config)
        recent_plan = self.commonconfiginfo.api_get_inner_config_detail(channel_config['id'])['data']
        assert edit_res['code'] == 0
        assert recent_plan['title'] == title


    @pytest.mark.parametrize("status", [True, False, True])
    def test_edit_plan_status(self, status):
        """
        测试修改投放计划有效性
        """
        resp = self.commonconfiginfo.api_get_all_config()
        plan_res = self.commonconfiginfo.api_edit_config_status(id=resp['data']['configs'][0]['id'], status=status)
        new_plan_status = self.commonconfiginfo.api_get_all_config()['data']['configs'][0]['status']
        # 去数据库获取对应渠道的status，用于后面比较
        plan_status = self.xshareQuery.get_xshare_advertising_plan(campaign=resp['data']['configs'][0]['id'])['status']
        assert plan_res['data']['success'] == True
        assert plan_status == status
        assert new_plan_status == status

    @pytest.mark.parametrize("status", [True, False, True])
    def test_edit_channel_status(self, status):
        """
        测试修改投放计划渠道的有效性
        """
        resp = self.commonconfiginfo.api_get_all_config()
        channel_config = self.xshareQuery.get_xshare_common_config(campaign=resp['data']['configs'][0]['id'])
        plan_res = self.commonconfiginfo.api_edit_config_status(id=resp['data']['configs'][0]['id'], status=status, channel=channel_config['channel'])
        # 去数据库获取对应渠道的status，用于后面比较
        channel_status = self.xshareQuery.get_xshare_common_config(campaign=resp['data']['configs'][0]['id'])['status']
        plan_channels_res = self.commonconfiginfo.api_get_config_channel_status(resp['data']['configs'][0]['id'])
        for conf in plan_channels_res['data']['configs']:
            if conf['channel'] == channel_config['channel']:
                p_c_status = conf['status']
        assert plan_res['data']['success'] == True
        assert channel_status == status
        assert channel_status == p_c_status

    def test_group_pagination(self):
        """
        投放列表 分页
        :return:
        """
        all_data, res_obj = get_all_page(self.commonconfiginfo, "api_get_all_config", page_size=20)
        ids = set([group['id'] for group in all_data])
        assert len(ids) == res_obj['totalCount']

    @pytest.mark.parametrize("campaign_status", [True, False])
    @pytest.mark.parametrize("channel_status", [True, False])
    @pytest.mark.parametrize("ets", [1, -1])
    # @pytest.mark.parametrize("channel", ["unwechat", "unwechat_group", "wechat_mini", "wechat_mini_group", "wechat_web"])
    def test_get_backup_config(self, get_one_commonconfig,get_backup_config, campaign_status, channel_status, ets):
        """测试外部获取配置项接口按规则判断是否走兜底项配置"""
        update_config = dict(get_one_commonconfig, **{'ets': get_any_time(day=ets), 'sts': get_any_time(day=ets-2)})
        self.commonconfiginfo.api_edit_config(payload=update_config)
        self.commonconfiginfo.api_edit_config_status(id=update_config['id'], status=campaign_status)
        self.commonconfiginfo.api_edit_config_status(id=update_config['id'], status=channel_status, channel='wechat_web')
        # 外部获取配置
        outer_config = self.commonconfiginfo.api_get_config_detail(id=update_config['id'], channel='wechat_web', lv='L0_1TC')
        # 投放计划无效或当前时间不在投放有效时间、或投放链接无效，都获取兜底项配置
        if campaign_status and channel_status and ets > 0:
            assert outer_config['data']['id'] == update_config['id']
            assert outer_config['data']['skuDetail'] == update_config['skuDetail']
        else:
            assert outer_config['data']['id'] == get_backup_config['id']
            # assert outer_config['data']['configDetails']['type'] == get_backup_config['configDetails'][-1]['type']
            # assert outer_config['data']['configDetails']['fakeColor'] == get_backup_config['configDetails'][-1]['fakeColor']
            # assert outer_config['data']['configDetails']['fakeShow'] == get_backup_config['configDetails'][-1]['fakeShow']
            # assert outer_config['data']['configDetails']['banner'] == get_backup_config['configDetails'][-1]['banner']
            # assert outer_config['data']['configDetails']['skuDesc'] == get_backup_config['configDetails'][-1]['skuDesc']
            assert outer_config['data']['skuDetail'] == get_backup_config['skuDetail']

    def test_add_config_failed(self, get_one_commonconfig):
        """
        测试新增投放计划失败
        """
        before_res = get_one_commonconfig
        after_res = dict(before_res, **{"sts": timeStampToTimeStr(int(dateToTimeStamp(min=-30))), "ets": timeStampToTimeStr(int(dateToTimeStamp(day=3, min=-10)))})
        del after_res['id']
        del after_res['title']
        create_res = self.commonconfiginfo.api_edit_config(payload=after_res)
        assert create_res['code'] == 10400
        assert create_res['msg'] == 'request validation error'

    def test_edit_config_failed(self,get_one_commonconfig):
        """
        测试修改投放计划失败
        """
        channel_config = get_one_commonconfig
        title = ''
        startAt, endAt = timeStampToTimeStr(int(dateToTimeStamp(min=-30))), timeStampToTimeStr(int(dateToTimeStamp(day=3, min=-10)))
        channel_config.update({"sts": startAt, "ets": endAt, "title": title})
        edit_res = self.commonconfiginfo.api_edit_config(payload=channel_config)
        assert edit_res['code'] == 10400
        assert edit_res['msg'] == 'request validation error'






