import requests


class HTTP:
    # 经典类和新式类
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url, headers={'Connection':'close'})
        # restful
        # json
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text