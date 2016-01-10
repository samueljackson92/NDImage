import pandas as pd


class DataLoader(object):

    def __init__(self):
        pass

    def load_csv(self, file_path):
        data_frame = pd.DataFrame.from_csv(file_path)
        return data_frame
