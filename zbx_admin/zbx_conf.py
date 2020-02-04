class zabbix_conf():
    """ Class to get all config from Zabbix Rest API """

    def __init__(self, _conf):
        """ Init some vars """

        self.conn = None
        self.conf = _conf
        self.conf_type = {
            'groups': ('hostgroup.get', 'groupid'),
            'hosts':  ('host.get', 'hostid'),
            'images': ('image.get', 'imageid'),
            'maps': ('map.get', 'sysmapid'),
            'screens': ('screen.get', 'screenid'),
            'templates': ('template.get', 'templateid'),
            'valuemaps': ('valuemap.get', 'valuemapid')
        }

    def connect_login(self):
        """ Connect on Zabbix Web """

        try:
            _conn = ZabbixAPI(server=f"http://{self.conf['ZABBIX_HOST']}", timeout=int(self.conf['timeout']))
            _conn.login(self.conf['ZABBIX_USER'], self.conf['ZABBIX_PASS'])
        except ZabbixAPIException:
            _conn = ZabbixAPI(server=f"https://{self.conf['ZABBIX_HOST']}", timeout=int(self.conf['timeout']))
            _conn.login(self.conf['ZABBIX_USER'], self.conf['ZABBIX_PASS'])
        except Exception as error:
            if self.conf['verbose']:
                print(error)
                sys.exit(0)
        
        return _conn
        
    def get_ids(self):
        """ Get the source type ids from the Zabbix Data """

        _json = self.conn.json_obj(self.conf_type[self.conf['type']][0], {'output': 'extend'})
        _result = self.conn.do_request(_json)
        _ids = [item[self.conf_type[self.conf['type']][1]] for item in _result['result']]

        if len(_ids) > 0:
            return _ids
        
        if self.conf['verbose']:
            print("The source type return with no value ids!")
        
        sys.exit(0)

    def get_conf(self):
        """ Get conf data from the Zabbix Server """

        _json = self.conn.json_obj("configuration.export", {"options": {self.conf['type']: self.get_ids()}, 'format': self.conf['format']})
        _result = self.conn.do_request(_json)
        _conf = _result['result']

        return _conf
        
    def write_conf(self):
        """ Write conf data in a file with same name of source type in json format """

        with open(f"{self.conf['path']}/{self.conf['type']}.{self.conf['format']}", "w") as json_file:
            json_file.write(str(self.get_conf()))

    def run(self):
        self.conn = self.connect_login()
        if self.conf['type'] == "all":
            for _type in self.conf_type.keys():
                self.conf['type'] = _type
                self.write_conf()
        self.write_conf()