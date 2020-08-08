
resource "ovh_domain_zone_record" "api" {
    zone = "lime-comb.net"
    subdomain = "api"
    fieldtype = "A"
    ttl = "3600"
    target = "0.0.0.0"
}

/*
A	216.239.32.21	
A	216.239.34.21	
A	216.239.36.21	
A	216.239.38.21	
AAAA	2001:4860:4802:32::15	
AAAA	2001:4860:4802:34::15	
AAAA	2001:4860:4802:36::15	
AAAA	2001:4860:4802:38::15	
CNAME	ghs.googlehosted.com	api
CNAME	ghs.googlehosted.com	www.api
*/
