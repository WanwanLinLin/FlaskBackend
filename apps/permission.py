# -*- coding: utf-8 -*-
import enum


@enum.unique
class Permission(enum.Enum):
    p0 = "权限管理"
    p1 = "使用后台"

    @property
    def flag(self):
        return int(self.name[1:])