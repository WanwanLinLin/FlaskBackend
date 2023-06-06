# encoding:utf-8
from db import SessionLocal

session = SessionLocal()
from goods import CategoryListModel, SeCategoryListModel, ThCategoryListModel

# with session:
#     new_category3 = ThCategoryListModel(
#         name="奶茶",
#         category_par=session.query(SeCategoryListModel).filter(SeCategoryListModel.name == "美美的团").first().id
#     )
#     session.add(new_category3)
#     session.commit()
with session:
    a = session.query(CategoryListModel).filter(CategoryListModel.name == "服装服饰").first()
    if a:
        print("yes")