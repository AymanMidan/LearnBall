class Utilisateur:
    def __init__(self, id, username, email, password, role, profile_image):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.profile_image = profile_image

    def to_dict(self):
        return self.__dict__
