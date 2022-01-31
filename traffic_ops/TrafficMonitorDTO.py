class TrafficMonitorDTO:
    def __init__(self, fqdn):
        self.fqdn = fqdn

    def get_fqdn(self):
        return self.fqdn

    def __str__(self):
        return str(self.fqdn)
