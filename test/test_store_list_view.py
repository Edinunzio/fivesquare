import unittest

from api.views import *
from api.models import *


class TestStoreListView(unittest.TestCase):
    """
    StoreListView test cases
    """

    def setUp(self):
        self.slv = StoreListView()
        # self.sdv = StoreDetailView()
        #self._get_queryset = self.slv.get_queryset()
        self.model = Store
        self.location = Location
        self.list_template = self.slv.get_template_names()
        #self.detail_template = self.sdv.get_template_names()

    def test_get_list_template_names_is_correct(self):
        self.assertEqual(["list.html"], self.list_template)


if __name__ == '__main__':
    unittest.main()