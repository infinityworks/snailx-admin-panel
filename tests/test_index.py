import unittest
from globals.globals import app


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index_page_response(self):
        with self.client as client:
            response = client.get("/")
            print(response)
            self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
