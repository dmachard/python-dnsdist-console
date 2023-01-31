
import re

class Statistics:
    def __init__(self, console, top_num=10):
        """statistics class"""
        self.c = console
        self.top_num = top_num
        self.__stats__ = {"global": {}, "backends": [] }
        
        self.fetch()
        
    def __repr__(self):
        """print stats"""
        return "%s" % self.__stats__
        
    def __getitem__(self, key):
        """get stats"""
        return self.__stats__[key]
        
    def fetch(self):
        """Get statistics from dnsdist"""
        
        # dump all stats
        o = self.c.send_command(cmd="dumpStats()")

        for l in o.splitlines():
              r = re.findall("\S+", l)
              for i in range(0, len(r), 2):
                   self.__stats__["global"][r[i]] = r[i+1]
                 
        # dump servers stats        
        o = self.c.send_command(cmd="showServers()")
        o_list = o.splitlines()[:-1]

        svr_hdr = o_list[0]
        
        svr_stats = []
        headers = re.sub('\s+', ' ', svr_hdr).split(' ')

        # Validate expectations about fields
        if 'Name' not in headers:
            raise ValueError("Missing Name field in dnsdist showServers()")
        if headers[0] != '#':
            raise ValueError("Unexpected first header in dnsdist showServers()")

        for s in o_list[1:]:
            # Find out the server name, expect it at pos 0
            server_id = s.split(' ')[0]
            srv_name_o = self.c.send_command(cmd="getServer("+server_id+")")
            srv_name = srv_name_o.rstrip()
            # The name output by showServers() is limited to 20 chars
            srv_name_trunc = srv_name[:20]
            # Sub with a copy that removes spaces to allow spliting the other fields
            srv_name_nowsp = srv_name_trunc.replace(' ','_')
            s = s.replace(srv_name_trunc, srv_name_nowsp)
            # Split, except the last fields (Pools), which contains spaces too
            svr = dict(zip(headers, re.sub('\s+', ' ', s).split(' ', len(headers) - 1)))
            # Restore name as output by showServers()
            svr['Name'] = srv_name_trunc
            svr_stats.append(svr)
            
        self.__stats__["backends"] = svr_stats
        
        self.__stats__["top-queries"] = self.top_queries(num=self.top_num)
        
        self.__stats__["top-nxdomain"] = self.top_nxdomain(num=self.top_num)
        
        self.__stats__["top-clients"] = self.top_clients(num=self.top_num)
        
    def top_queries(self, num=10):
        """get top queries"""
        o = self.c.send_command(cmd="topQueries(%s)" % num)
        return self.decode_top_output(o=o)
        
    def top_nxdomain(self, num=10):
        """get top non-existent domain"""
        o = self.c.send_command(cmd="topResponses(%s,DNSRCode.NXDOMAIN)" % num)
        return self.decode_top_output(o=o)
        
    def top_clients(self, num=10):
        """get top clients"""
        o = self.c.send_command(cmd="topClients(%s)" % num)
        return self.decode_top_output(o=o)
        
    def decode_top_output(self, o):
        """decode top output"""
        o_list = []
        for l in o.splitlines()[:-1]:
            r = re.findall("\S+", l)
            o_list.append({"entry": r[1], "hits": r[2]})
        return o_list