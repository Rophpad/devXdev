import json
import os

class FileStorage:
  """File Storage to manage user datas"""

  __filename = "file.json"

  def __init__(self):
    pass
  
  def create_file(self):
    if not os.path.exists(self.__filename):
      open(self.__filename, 'w').close()

  def save_data(self, data):
    self.create_file()
    with open(self.__filename, 'w') as f:
        json.dump(data, f)

  def load_data(self):
    try:
        with open(self.__filename) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {self.__filename} not found")
        return []
    
  def find_by_key(self, key, value):
    datas = self.load_data()
    for data in datas:
        if data.get(key) == value:
            return data
    return None

  def append_data(self, new_data):
    datas = self.load_data()
    """
    if new_data not in datas:
        datas.append(new_data)
        self.save_data(datas)
    else:
        print("Data already exists, not appending")
    """
    if len(datas) != 0:
        for data in datas:
            if data['login'] == new_data['login']:
                print("Data with same login already exists, not appending")  
                return
    datas.append(new_data)
    self.save_data(datas)
    

  def count_data(self):
    datas = self.load_data()
    return len(datas)