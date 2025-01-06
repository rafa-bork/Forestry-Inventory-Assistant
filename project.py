import pandas as pd

def welcome_message():


def read_my_data():
    df = pd.read_csv("tree_data_blueprint.csv")
    return df

class Tree:
    def init(self, species, dbh, height, cod_status='ALIVE', bark_width=0.0):
        self.species = species
        self.dbh = dbh
        self.height = height
        self.cod_status = cod_status
        self.bark_width = bark_width

def main():
    welcome_message()
    data = read_my_data()
    print(data.head())