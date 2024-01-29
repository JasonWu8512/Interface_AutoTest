# coding=utf-8
# @Time    : 2020/8/3 4:27 下午
# @Author  : keith
# @File    : domains

import inspect
import os
import sys

import yaml
from pandas.conftest import cls
from pytest_testconfig import config as conf
from pathlib import Path
# os.path.abspath(__file__)
ROOT_PATH = Path(__file__).resolve().parent.parent.parent

class Domains(object):
    config: None = None
    domain = None
    DbKey = None
    Env = 'fat'

    @classmethod
    def set_domain(cls, domain):
        Domains.domain = domain

    def update_file_path(self, uri):
        try:
            config = self.config
        except AttributeError:
            if "dev" in Domains.domain:
                env = "dev"
            elif "rc" in Domains.domain:
                env = "rc"
            elif "fat" in Domains.domain:
                env = "fat"
            else:
                env = "prod"
            config = self.set_env_path(env)
        return config[uri]

    # http://gateway-dev.jlgltech.com
    @classmethod
    def get_gateway_host(self):
        host = Domains.domain.replace("https://", "http://gateway-").replace("jiliguala", "jlgltech")
        return host

    @classmethod
    def get_gaga_host(cls) -> object:
        # Domains.Env=env
        host = Domains.config['url'].replace( "https://" + Domains.Env + ".jiliguala", "https://" + Domains.Env + ".jiligaga" )
        return host
        # if sys.platform == "darwin" or sys.platform == "win32":
        # path = os.path.split ( inspect.stack ()[0][1] )[0]
        # filename = os.path.join ( path, "{}.yaml".format ( env ) ).replace ( "\\", "/" )
        # f = open ( filename, "rb" )
        # config = yaml.load ( f, Loader=yaml.FullLoader )
        # else:
        #     config = conf
        # cls.config = config
        # return config

    # @classmethod
    # def get_ggr_host(self):
    #     host = Domains.domain.replace("https://" + Domains.Env, "https://" + Domains.Env + "ggr")
    #     return host

    @classmethod
    def set_env_path(cls, env='fat') -> object:
        Domains.Env = env
        # if sys.platform == "darwin" or sys.platform == "win32":
        #     path = os.path.split(inspect.stack()[0][1])[0]
        #     filename = os.path.join(path, "{}.yaml".format(env)).replace("\\", "/")
        #     f = open(filename, "rb")
        #     config = yaml.load(f, Loader=yaml.FullLoader)
        # else:
        #     config = conf
        # cls.config = config
        if conf:
            config = conf
        else:
            path = os.path.split(inspect.stack()[0][1])[0]
            filename = os.path.join(path, "{0}.yaml".format(env)).replace("\\", "/")
            f = open(filename, "rb")
            config = yaml.load(f, Loader=yaml.FullLoader)
        cls.config = config
        return config
