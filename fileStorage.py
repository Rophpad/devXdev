import json
import os


class FileStorage:
    """File Storage to manage user datas"""
    __filename = "file.json"

    def __init__(self):
        pass

    def create_file(self):
        """ Create file that serve as storage """
        if not os.path.exists(self.__filename):
            open(self.__filename, 'w').close()

    def save_data(self, data):
        """Save data to the file """
        self.create_file()
        with open(self.__filename, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        """ Loads datad in the file """
        try:
            with open(self.__filename) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"File {self.__filename} not found or empty")
            return []

    def find_by_key(self, key, value):
        """Finds a element in the file """
        datas = self.load_data()
        for data in datas:
            if data.get(key) == value:
                return data
        return None

    def append_data(self, new_data):
        """ Appends new data to the file """
        datas = self.load_data()
        if len(datas) != 0:
            for data in datas:
                if data['login'] == new_data['login']:
                    print("Data with same login already exists, not appending")
                    return
        datas.append(new_data)
        self.save_data(datas)

    def count_data(self):
        """ Return the numbers of users in the storage """
        datas = self.load_data()
        return len(datas)

    def filterby(self, filters):
        datas = self.load_data()

        if 'prog_lang' in filters:
            datas = [
                data for data in datas
                if filters['prog_lang'] in data['top_languages']
            ]
            if len(filters) == 1 and len(datas) == 0:
                datas = self.load_data()

        if 'coding_freq' in filters:
            ranges = {
                'Low': range(0, 11),
                'Medium': range(11, 26),
                'High': range(26, 100)
            }
            try:
                datas = [
                    data for data in datas
                    if data['activity_count'] in ranges[filters['coding_freq']]
                ]
            except KeyError:
                datas = datas

        if 'country' in filters:
            datas = [
                data for data in datas
                if data['location'] == filters['country']
            ]
            if len(filters) == 1 and len(datas) == 0:
                datas = self.load_data()
        return datas
