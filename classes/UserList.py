class UserList:
    def __init__(self, users):
        self.users = users

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user

    def add_user(self, user):
        current_user = self.get_user(user.user_id)
        if current_user:
            current_user = user
        else:
            self.users.append(user)

        return current_user
