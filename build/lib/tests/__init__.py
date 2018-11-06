from unittest import TestCase
from pydatabase.env.environment import Environment
import pydatabase
class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        pydatabase.init(Environment.ENV_LOCAL)


