class Book:
    def __init__(self, id, title, author, img_url):
        self.id = id
        self.title = title
        self.author = author
        self.img_url = img_url

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Book({self.id}, {self.title}, {self.author}, {self.img_url})"