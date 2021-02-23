import os

import gspread

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '..', 'utils', 'credentials.json')
gc = gspread.service_account(filename=filename)

sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1A3W5Lbs-R3ed6OdVMBkeqzIVEplWO6I9DLiche9zj_s/edit#gid=0")

worksheet = sh.sheet1


class Settings:
    def __init__(self):
        self.categories = []
        self.time = []
        self.channels = []
        self.admins = []
        self.pagination = 5
        self.update()
        print('Ready!')

    def update(self):
        category_labels = worksheet.col_values(1)
        category_hashtags = worksheet.col_values(2)
        category_keywords = worksheet.col_values(3)
        channels = worksheet.col_values(4)
        time_labels = worksheet.col_values(5)
        time_values = worksheet.col_values(6)
        pagination = worksheet.col_values(7)
        admins = worksheet.col_values(8)
        category_labels.pop(0)
        category_hashtags.pop(0)
        category_keywords.pop(0)
        channels.pop(0)
        time_labels.pop(0)
        time_values.pop(0)
        admins.pop(0)
        pagination.pop(0)
        self.admins = admins
        self.channels = channels
        self.categories = []
        self.time = []
        self.pagination = int(pagination[0])

        for (index, category) in enumerate(category_labels):
            self.categories.append({
                'label': category_labels[index],
                'hashtags': category_hashtags[index].split(',', -1),
                'keywords': category_keywords[index].split(',', -1),
            })

        for (index, category) in enumerate(time_labels):
            self.time.append({
                'label': time_labels[index],
                'value': time_values[index],
            })


settings = Settings()
