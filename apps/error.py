# -*- coding: utf-8 -*-
from flask import jsonify


class ApiError(Exception):
    _ERRORS = {
        -100001: (501, "The interface has not been implemented"),
        -100404: (404, "Request URL does not exist"),
        -100405: (405, "The requested URL does not allow access to this method"),
        -100500: (500, "Network error"),
        -101001: (400, "Field cannot be empty"),
        -101002: (400, "Field format error"),
        -101003: (400, "Error parsing request json"),
        -101004: (400, "The parameter is wrong"),
        -101010: (400, "Object does not exist"),
        -101011: (400, "Object already exists"),
        -101012: (400, "Object is not unique"),
        -101013: (400, "Object mismatch"),
        -101014: (400, "Object deleted"),
        -101020: (401, "You are not logged in"),
        -101026: (
            403,
            "The user has not given this permission, please contact the system administrator",
        ),
        -101028: (400, "The input contains sensitive words"),
        -101030: (403, "Not authorized to perform this operation"),
        -101040: (400, "The operation failed, please try again later"),
        -101070: (401, "Authentication failed"),
        -101080: (400, "Service call failed"),
    }

    def __init__(self, code, msg=None, status=None):
        super().__init__()
        self.code = code
        self.status = status if status is not None else self._ERRORS[self.code][0]
        self.msg = msg if msg is not None else self._ERRORS[self.code][1]

    def __repr__(self):
        return f"XTeError: [{self.code}:{self.status}] {self.msg}"

    def __str__(self):
        return self.msg

    @property
    def response(self):
        return jsonify({"code": self.code, "error": self.msg}), self.status