# def always_load_func_dec(func):
#     def inner_func(reference, *args, **kwargs):
#         func(*args, **kwargs)
#         for load_func in reference.always_load_funcs:
#             load_func()
#         return inner_func
#
#     return always_load_func_dec
