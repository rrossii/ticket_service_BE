def category_name_to_id(category_name):
    category_name = category_name.lower()

    categories = ["theater", "festival", "sport", "concert"]
    categ_id = [1, 2, 3, 4]
    category_id_with_names = dict(map(lambda key, val: (key, val), categories, categ_id))

    return category_id_with_names.get(category_name)
