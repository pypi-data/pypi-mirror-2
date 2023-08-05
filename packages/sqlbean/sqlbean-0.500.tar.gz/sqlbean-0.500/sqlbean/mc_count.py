#coding:utf-8
from sqlbean.db.mc_connection import mc
class McCount(object):
    def __init__(self, get_count, mc_key):
        self.mc_key = mc_key
        self.get_count = get_count

    def __call__(self, key):
        mk = self.mc_key%key
        count = mc.get(mk)
        if count is None:
            count = self.get_count(key)
        mc.set(mk, count)
        return count

    def incr(self, key):
        mk = self.mc_key%key
        if mc.get(mk) is not None:
            mc.incr(mk)

    def decr(self, key):
        mk = self.mc_key%key
        if mc.get(mk) is not None:
            mc.decr(mk)



