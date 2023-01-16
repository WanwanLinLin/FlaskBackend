# -*- coding：utf-8 -*-
import os

now_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRADEMARK_PATH = os.path.join(now_path, 'static', 'trademark')
CATEGORY_PATH = os.path.join(now_path, 'static', 'category_image')


if __name__ == '__main__':
    print(TRADEMARK_PATH)
    print(CATEGORY_PATH)