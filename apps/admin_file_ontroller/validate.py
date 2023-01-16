# -*- coding: utf-8 -*-
from pydantic import BaseModel


class XApiKey(BaseModel):
    Xapikey: str


