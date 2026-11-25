import unittest
import yaml
import os
from glob import glob

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

ALLOWED_API_V1_SERVER_ROUTES = {
    '/api/v1/classes',
    '/api/v1/consentVersions',
    '/api/v1/courses',
    '/api/v1/ldap-config',
    '/api/v1/roster',
    '/api/v1/users',
}


def find_api_v1_server_routes(value):
    routes = set()
    if isinstance(value, dict):
        if value.get('serviceName') == 'api-svc':
            path = value.get('path', '')
            if isinstance(path, str) and path.startswith('/api/v1/'):
                routes.add(path)
        for child in value.values():
            routes.update(find_api_v1_server_routes(child))
    elif isinstance(value, list):
        for child in value:
            routes.update(find_api_v1_server_routes(child))
    return routes


class TestEverything(unittest.TestCase):

    def test_group_vars_all_config(self):
        config_yml_file = os.path.join(PROJECT_DIR, 'ansible', 'group_vars', 'all', 'config.yml')
        with open(config_yml_file, 'r') as file:
            config_all = yaml.safe_load(file)
            useless_declarations = []
            for entry in config_all['configuration_all']:
                res = not config_all['configuration_all'][entry]['server'] \
                      and not config_all['configuration_all'][entry]['client']
                if res:
                    useless_declarations.append(entry)

            self.assertEqual([], useless_declarations, 'populating a variable that is never set anywhere')

    def test_no_new_api_v1_routes_to_legacy_server(self):
        ingress_config_files = []
        for pattern in (
            'ansible/group_vars/**/x_ingress.yml',
            'ansible/group_vars/**/instance_cfg.yml',
            'ansible/host_vars/**/cfg.yml',
        ):
            ingress_config_files.extend(glob(os.path.join(PROJECT_DIR, pattern), recursive=True))

        configured_routes = set()
        for config_file in ingress_config_files:
            with open(config_file, 'r') as file:
                configured_routes.update(find_api_v1_server_routes(yaml.safe_load(file)))

        new_routes = configured_routes - ALLOWED_API_V1_SERVER_ROUTES
        self.assertEqual(
            set(),
            new_routes,
            'New API v1 routes to api-svc are forbidden; rewrite APIs in NestJS instead: '
            + ', '.join(sorted(new_routes)),
        )


if __name__ == '__main__':
    unittest.main()
