class Candidate:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Candidate {} with {} votes>".format(self.name, len(self.votes))

    def __str__(self):
        return self.name
