# 2022-12-05 11:15
import requests, unittest, json

class Testing(unittest.TestCase):
    def test_get_status_statuscode (self):
        result = requests.get("http://0.0.0.0/reservations/status/")
        self.assertEqual(result.status_code, 200)

    def test_get_status_body (self):
        result = requests.get("http://0.0.0.0/reservations/status/")
        result = json.loads(result.content)
        status:json = {"apiversion": "1.3.0", "authors": ["Jakob Vollmer", "Louis Müller"]}
        self.assertEqual(result, status)

if __name__ == '__main__':
    unittest.main()
