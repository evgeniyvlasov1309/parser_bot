import os
import traceback

import gspread

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '..', 'utils', 'credentials.json')
gc = gspread.service_account(filename=filename)

sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1mCxcuO7wuhuWdIV-crvhOI6DZTqQQdIZrixyQxxTlzQ/edit?usp=sharing")

worksheet = sh.sheet1


class Settings:
    def __init__(self):
        self.categories = []
        self.time = []
        self.channels = []
        self.admins = []
        self.pagination = 5
        self.users = []
        self.update()
        print('Ready!')

    def update(self):
        try:
            category_labels = worksheet.col_values(1)
            category_hashtags = worksheet.col_values(2)
            category_keywords = worksheet.col_values(3)
            channels = worksheet.col_values(4)
            time_labels = worksheet.col_values(5)
            time_values = worksheet.col_values(6)
            pagination = worksheet.col_values(7)
            admins = worksheet.col_values(8)
            users_username = worksheet.col_values(9)
            users_access_time = worksheet.col_values(10)
            category_labels.pop(0)
            category_hashtags.pop(0)
            category_keywords.pop(0)
            channels.pop(0)
            time_labels.pop(0)
            time_values.pop(0)
            admins.pop(0)
            pagination.pop(0)
            users_username.pop(0)
            users_access_time.pop(0)
            self.admins = admins
            self.channels = channels
            self.categories = []
            self.time = []
            self.users = []
            self.pagination = int(pagination[0])

            diff_len = len(category_labels) - len(category_hashtags)
            lost_part = [''] * diff_len
            category_hashtags.extend(lost_part)

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

            for (index, category) in enumerate(users_username):
                self.users.append({
                    'username': users_username[index],
                    'period': users_access_time[index],
                })
        except Exception:
            print('Ошибка:\n', traceback.format_exc())


settings = Settings()
