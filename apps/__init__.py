# -*- coding: utf-8 -*-
from .extension import init_swagger
from .auth import create_jwt, login_required
from .db import db, init_database