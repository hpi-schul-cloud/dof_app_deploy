import unittest
import yaml
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))


class TestEverything(unittest.TestCase):

    def test_group_vars_all_config(self):
        config_yml_file = os.path.join(PROJECT_DIR, 'ansible', 'group_vars', 'all', 'config.yml')
        with open(config_yml_file, 'r') as file:
            config_all = yaml.safe_load(file)
            useless_declarations = []
            for entry in config_all['configuration_all']:
                res = not config_all['configuration_all'][entry]['server'] \
                      and not config_all['configuration_all'][entry]['client'] \
                      and not config_all['configuration_all'][entry]['nuxtclient']
                if res:
                    useless_declarations.append(entry)

            self.assertEqual([], useless_declarations, 'populating a variable that is never set anywhere')


if __name__ == '__main__':
    unittest.main()
