import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests

from robyn import Robyn
app = Robyn(__file__)


resp = requests.post("https://192.168.200.211:53317/api/localsend/v2/register",verify=False)
print(resp.json().get('alias'))

requests.post()