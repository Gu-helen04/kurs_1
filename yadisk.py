import requests
import time

class YaDisk:
  hosts = 'https://cloud-api.yandex.net'
  def __init__(self, token):
    self.token = token

  def get_headers(self):
    return {
      'Content-Type': 'application/json',
      'Authorization': f'OAuth {self.token}'
      }

  def upload_file_g(self, id_operation):
    url = f'{self.hosts}/v1/disk/operations/'+id_operation
    headers = self.get_headers()
    res = requests.get(url, headers=headers)
    if res.json()['status'] == 'success':
      return True
    else:
      return False

  def upload_file_(self, url_, file_name):
    url = f'{self.hosts}/v1/disk/resources/upload/'
    params = {'path': file_name, 'url': url_}
    headers = self.get_headers()
    res = requests.post(url, params=params, headers=headers, )
    id_operation = str(res.json().get('href')).partition('operations/')[2]
    time.sleep(3)
    boot_switch = self.upload_file_g(id_operation)
    return(boot_switch)

  def create_folder_yandex_(self, folder_name):
    url = f'{self.hosts}/v1/disk/resources/'
    params = {'path': '/' + folder_name + '/'}
    headers = self.get_headers()
    res = requests.put(url,params=params,headers=headers)
    res.raise_for_status()
    if res.status_code == 201:
      return(True)
    else:
      return (False)
    # try/except ??
    # elif res.status_code == 409:
    #   return ('Ресурс уже существует.')
    # else:
    #   return('Ошибка при создании папки')

