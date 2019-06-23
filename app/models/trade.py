# from app.models.gift import Gift
# from app.models.wish import Wish
# from sqlalchemy import desc

# class Trade_gift(Gift):
#     @classmethod
#     def my_gifts(cls):
#         # uid = current_user.id
#         uid = 6
#         mygifts = Gift.query.filter_by(uid=uid, launched=False).all()
#         for gift in mygifts:
#             isbn = gift.isbn
#             count_wishes = len(Wish.query.filter_by(launched=False, isbn=gift.isbn).all())
#             gift.count_wishes = count_wishes
#         return mygifts

# class Trade_wish(Wish):
# #     @classmethod
# #     def get_user_wishes(cls):
# #         # uid = current_user.id
# #         uid = 6
# #         wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
# #             desc(Wish.create_time)).all()
# #         for wish in wishes:
# #             wish.count_gift = len(Gift.query.filter_by(launched=False, isbn=wish.isbn).all())
# #         return wishes