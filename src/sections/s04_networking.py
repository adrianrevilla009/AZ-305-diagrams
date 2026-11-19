from azdiag import Book

DOM = "Infrastructure (30-35%)"


def build():
    b = Book("04-networking.drawio", "Networking and connectivity", DOM)

    # ------------------------------------------------------------------ 4.1
    d = b.D("4.1", "Hub-and-spoke network", "A",
            "A hub VNet holds shared services (gateways, firewall, DNS, Bastion). Each workload lives in its own spoke VNet peered to the hub. "
            "You run the routing yourself because peering is not transitive.",
            [("One region, or you want full control", "hub-spoke"), ("Many branches and regions, transitive routing", "Virtual WAN"),
             ("TLS inspection / IDPS", "Azure Firewall Premium"), ("Centralised Internet egress", "UDR 0.0.0.0/0 to the firewall")])
    d.box("onp", "On-premises network", -0.15, 1, w=140, color="gray")
    d.icon("gw", "Virtual_Network_Gateways", "VPN / ExpressRoute gateway", "VGW / Transit Gateway attachment", 1.25, 1)
    d.icon("fw", "Firewalls", "Azure Firewall", "Network Firewall", 2.25, 1)
    d.icon("dnsr", "DNS_Private_Resolver", "DNS Private Resolver", "Route 53 Resolver endpoints", 1.25, 2.1)
    d.icon("bas", "Bastions", "Azure Bastion", "SSM Session Manager", 2.25, 2.1)
    d.group("hub", "Hub VNet - shared services  (AWS: hub VPC / Transit Gateway)", ["gw", "fw", "bas", "dnsr"], "blue")
    d.icon("vm", "Virtual_Machine", "Workload VMs", "EC2", 4.0, 0)
    d.icon("udr", "Route_Tables", "UDR 0.0.0.0/0 to firewall", "Route table", 5.0, 0)
    d.group("spA", "Spoke A VNet - workload  (AWS: VPC)", ["vm", "udr"], "green")
    d.icon("aks", "Kubernetes_Services", "AKS cluster", "EKS", 4.0, 2.1)
    d.icon("nsg", "Network_Security_Groups", "NSG", "Security Group + NACL", 5.0, 2.1)
    d.group("spB", "Spoke B VNet - workload  (AWS: VPC)", ["aks", "nsg"], "green")
    d.edge("onp", "gw", "VPN / ER", "private")
    d.edge("gw", "fw", "inspect")
    d.edge("fw", "vm", "peering + UDR", "ok")
    d.edge("fw", "aks", "peering + UDR", "ok")
    d.note("n1", "VNet peering is NOT transitive: spoke-to-spoke traffic must go through the hub firewall / NVA with UDRs. Global peering connects VNets across regions.", 0.2, 3.35, w=430)
    d.note("n2", "A VNet is regional. Subnets span the whole region (in AWS each subnet lives in one AZ). Bastion gives browser RDP/SSH to VMs in peered spokes without public IPs.", 2.4, 3.35, w=480)

    # ------------------------------------------------------------------ 4.2
    d = b.D("4.2", "Virtual WAN", "A",
            "Virtual WAN is a Microsoft-managed hub with automatic transitive routing between VNets, VPN and ExpressRoute. "
            "It scales to multi-hub global networks and is the answer for many branches or many regions.",
            [("Many branches and regions, transitive routing", "Virtual WAN"), ("SD-WAN branches", "Virtual WAN"),
             ("Join on-prem sites over Microsoft's backbone", "ExpressRoute Global Reach"), ("Only one region, full control", "hub-spoke")])
    d.box("br1", "Branch offices (SD-WAN / VPN)", 0, 0.2, w=170, color="gray")
    d.box("br2", "Datacenter on ExpressRoute", 0, 1.6, w=170, color="gray")
    d.box("usr", "Remote users (P2S VPN)", 0, 2.8, w=170, color="gray")
    d.icon("hub1", "Virtual_WAN_Hub", "Virtual hub - region A", "Transit Gateway", 1.7, 1.4)
    d.icon("fw1", "Firewalls", "Secured hub: Azure Firewall", "Network Firewall", 1.7, 2.8)
    d.group("hA", "Region A - Virtual WAN hub  (Microsoft-managed)", ["hub1", "fw1"], "blue")
    d.icon("hub2", "Virtual_WAN_Hub", "Virtual hub - region B", "Transit Gateway (peered)", 3.5, 1.4)
    d.group("hB", "Region B - Virtual WAN hub", ["hub2"], "blue")
    d.icon("v1", "Virtual_Networks", "Spoke VNets (region A)", "VPC attachments", 5.3, 0.4)
    d.icon("v2", "Virtual_Networks", "Spoke VNets (region B)", "VPC attachments", 5.3, 2.4)
    d.edge("br1", "hub1", "VPN / SD-WAN", "data")
    d.edge("br2", "hub1", "ExpressRoute", "private")
    d.edge("usr", "hub1", "P2S", "data")
    d.edge("hub1", "hub2", "hub-to-hub (automatic)", "ok", both=True)
    d.edge("hub2", "v1", "auto routing", "ok")
    d.edge("hub2", "v2", "auto routing", "ok")
    d.note("n1", "Scale per hub: S2S VPN up to 20 Gbps, P2S 20 Gbps with 100,000 clients, VNet-to-VNet up to 50 Gbps. In the hub you can only deploy Microsoft-managed resources.", 0, 4.0, w=620, dx=140)

    # ------------------------------------------------------------------ 4.3
    d = b.D("4.3", "Hub-spoke vs Virtual WAN", "D",
            "Both build a hub network. Pick by size and by how much control you want over routing.",
            [("Many branches (SD-WAN) or multi-region", "Virtual WAN"), ("One region, or you want total control", "hub-spoke"),
             ("Peering is not transitive", "you must build routes (UDR / NVA)")])
    d.table(0, 0, [dict(title="Traditional hub-spoke", icon="Virtual_Networks", aws="hub VPC / Transit Gateway", w=400),
                   dict(title="Virtual WAN", icon="Virtual_WANs", aws="Transit Gateway + Cloud WAN", w=400)],
            [("Who manages the hub", ["You deploy and operate gateways, firewall and DNS in the hub VNet",
                                      "Microsoft manages the hub; only Microsoft-managed resources can be deployed in it"]),
             ("Routing between VNets", ["✗ Peering is not transitive: you build UDRs and run an NVA/firewall",
                                        "✓ Automatic transitive routing between VNets, VPN and ExpressRoute"]),
             ("Scale", ["Limited by your gateway SKUs and your design",
                        "Multi-hub global. S2S VPN up to 20 Gbps, P2S 20 Gbps with 100,000 clients per hub, VNet-to-VNet up to 50 Gbps"]),
             ("Best fit", ["★ One region, or when you want full control", "★ Many branches (SD-WAN) or multi-region"]),
             ("Exam keywords", ["'one region', 'full control', 'custom NVA'", "'many branches', 'transitive', 'SD-WAN', 'multi-region'"])],
            label_w=170)

    # ------------------------------------------------------------------ 4.4
    d = b.D("4.4", "Hybrid connectivity: VPN and ExpressRoute", "A",
            "Site-to-site VPN rides the Internet (cheap, quick, also the backup). ExpressRoute is a private circuit with predictable latency and an SLA. "
            "Combine them for resilience.",
            [("Private, not over the Internet", "ExpressRoute"), ("Quick to set up, or backup for ExpressRoute", "VPN"),
             ("Join two on-prem sites over Microsoft's backbone", "Global Reach"), ("Lower latency from on-prem to VMs", "FastPath (Ultra Performance / ErGw3Az)"),
             ("L2 encryption on dedicated ports", "ExpressRoute Direct + MACsec")])
    d.box("hq", "HQ datacenter", 0, 0.3, w=130, color="gray")
    d.box("br", "Branch datacenter", 0, 1.8, w=130, color="gray")
    d.box("usr", "Remote users", 0, 3.2, w=130, color="gray")
    d.icon("lng", "Local_Network_Gateways", "Site-to-Site VPN (IPsec over Internet)", "Site-to-Site VPN", 1.5, 0.3)
    d.icon("er", "ExpressRoute_Circuits", "ExpressRoute circuit (private, SLA)", "Direct Connect", 1.5, 1.8)
    d.icon("p2s", "VPN_Client_Windows", "Point-to-Site (OpenVPN, IKEv2, Entra auth)", "Client VPN", 1.5, 3.2)
    d.icon("gw", "Virtual_Network_Gateways", "VPN / ExpressRoute gateway", "Virtual Private Gateway", 3.3, 1.6)
    d.icon("vnet", "Virtual_Networks", "Azure VNets (several share one circuit)", "VPC", 4.8, 1.6)
    d.edge("hq", "lng"); d.edge("lng", "gw", "IPsec", "data")
    d.edge("br", "er", "", "private"); d.edge("er", "gw", "private", "private")
    d.edge("usr", "p2s"); d.edge("p2s", "gw", "", "data")
    d.edge("gw", "vnet", "", "data")
    d.edge("hq", "br", "Global Reach: sites talk over the Microsoft backbone", "private", src="b", dst="t")
    d.table(0, 4.3, [dict(title="Standard / ERGw1Az", w=250), dict(title="High Performance / ERGw2Az", w=250), dict(title="Ultra Performance / ErGw3Az", w=250)],
            [("ExpressRoute gateway SKU", ["4 connections, no FastPath", "8 connections", "16 connections, with FastPath"]),
             ("Good to know", ["Gateway creation takes about 30-45 min", "One circuit connects many VNets, which share the bandwidth", "ExpressRoute Direct = 10/100 Gbps ports + MACsec"])],
            label_w=170)

    # ------------------------------------------------------------------ 4.5
    d = b.D("4.5", "Private access to PaaS: Private Endpoint vs Service Endpoint", "A",
            "A Private Endpoint gives a PaaS resource a private IP inside your VNet (works from on-prem too). A Service Endpoint only optimises the route; the service keeps its public IP.",
            [("PaaS with no public endpoint", "Private Endpoint"), ("Restrict Storage to a subnet at no cost", "Service Endpoint"),
             ("Private Endpoint is failing", "check DNS (privatelink.* zone linked to the VNet)"), ("Resolve Private Endpoints from on-prem", "DNS Private Resolver")])
    d.box("onp", "On-premises", -0.2, 1.7, w=130, color="gray")
    d.icon("vm", "Virtual_Machine", "VM / app in the VNet", "EC2", 1.4, 0.2)
    d.icon("pe", "Private_Endpoint", "Private Endpoint (private IP)", "VPC interface endpoint", 3.0, 0.2)
    d.icon("res", "DNS_Private_Resolver", "DNS Private Resolver", "Route 53 Resolver endpoints", 1.4, 1.7)
    d.icon("dnsz", "DNS_Zones", "Private DNS zone privatelink.*", "Route 53 private hosted zone", 3.0, 1.7)
    d.group("vn", "Your VNet", ["vm", "pe", "res", "dnsz"], "blue")
    d.icon("sa", "Storage_Accounts", "Storage Account", "S3", 4.8, 0.2)
    d.icon("sql", "SQL_Database", "SQL Database", "RDS", 4.8, 1.4)
    d.edge("vm", "pe", "private IP", "private"); d.edge("pe", "sa", "Private Link", "private"); d.edge("pe", "sql", "Private Link", "private")
    d.edge("vm", "dnsz", "resolves to private IP", "ctrl")
    d.edge("onp", "res", "VPN/ER + DNS forwarding", "private")
    d.edge("res", "dnsz", "", "ctrl")
    d.note("n1", "Service Endpoint (AWS: gateway endpoint for S3/DynamoDB): traffic stays on the Microsoft backbone but the service keeps its public IP. Only from VNets, not from on-prem. No extra cost.", 0, 3.1, w=470, dx=60)
    d.note("n2", "App Service: VNet Integration = outbound; Private Endpoint = inbound. They complement each other.", 2.7, 3.1, w=330, dx=60)

    # ------------------------------------------------------------------ 4.6
    d = b.D("4.6", "Network security stack", "A",
            "Defence in depth on the network: DDoS and WAF at the edge, a central firewall for inspection, NSGs on every subnet, Bastion for admin access, NAT Gateway for fixed outbound IPs.",
            [("SQLi / XSS", "WAF"), ("TLS inspection / IDPS", "Azure Firewall Premium"), ("L3/L4 flood protection", "DDoS Protection"),
             ("Admin RDP/SSH without a public IP", "Azure Bastion"), ("Fixed outbound IP, no SNAT exhaustion", "NAT Gateway")])
    d.box("net", "Internet", -0.2, 1, w=110, color="gray")
    d.icon("ddos", "DDoS_Protection_Plans", "DDoS Protection (L3/L4)", "Shield Advanced", 0.9, 1)
    d.icon("waf", "Web_Application_Firewall_Policies_WAF", "WAF on App Gateway / Front Door (L7)", "AWS WAF", 2.0, 1)
    d.icon("fw", "Firewalls", "Azure Firewall (L3-L7)", "Network Firewall", 3.1, 1)
    d.icon("nsg", "Network_Security_Groups", "NSG per subnet / NIC (L3-L4, stateful)", "Security Group + NACL", 4.2, 1)
    d.icon("vm", "Virtual_Machine", "Workloads", "EC2", 5.3, 1)
    d.icon("nat", "NAT", "NAT Gateway (outbound)", "NAT Gateway", 6.4, 1)
    d.icon("fwm", "Azure_Firewall_Manager", "Firewall Manager (central policy)", "Firewall Manager", 2.0, 2.3)
    d.icon("bas", "Bastions", "Azure Bastion (admin access)", "SSM Session Manager", 4.2, 2.3)
    d.edge("net", "ddos"); d.edge("ddos", "waf"); d.edge("waf", "fw"); d.edge("fw", "nsg"); d.edge("nsg", "vm")
    d.edge("vm", "nat", "outbound", "async")
    d.edge("bas", "vm", "RDP/SSH", "ctrl")
    d.edge("fwm", "fw", "policy", "ctrl")
    d.table(0, 3.55, [dict(title="Basic", w=300), dict(title="Standard", w=300), dict(title="Premium", w=300)],
            [("Azure Firewall tiers (each includes the previous)", ["SMBs, about 250 Mbps", "General use: network + application (FQDN) rules, NAT, threat intelligence",
                                                                    "Adds TLS inspection, IDPS and URL / category filtering"])],
            label_w=190)

    # ------------------------------------------------------------------ 4.7
    d = b.D("4.7", "Hybrid DNS and name resolution", "A",
            "Public names live in Azure DNS. Private names live in Private DNS zones linked to VNets. DNS Private Resolver forwards queries between on-prem and Azure so you don't run DNS VMs.",
            [("Resolve Private Endpoints from on-prem", "DNS Private Resolver"), ("Domain apex pointing to Front Door / Traffic Manager", "Azure DNS alias record"),
             ("privatelink.* names", "Private DNS zone linked to the VNet")])
    d.box("onp", "On-prem DNS servers", 0, 1.3, w=150, color="gray")
    d.icon("res", "DNS_Private_Resolver", "DNS Private Resolver (inbound + outbound endpoints)", "Route 53 Resolver endpoints", 1.5, 1.3)
    d.icon("pdns", "DNS_Zones", "Azure Private DNS zones (virtual network links)", "Route 53 private hosted zones", 3.3, 1.3)
    d.icon("vnet", "Virtual_Networks", "VNets / spokes", "VPC", 5.0, 1.3)
    d.icon("pub", "DNS_Zones", "Azure DNS public zone", "Route 53 hosted zones", 1.5, 3.0)
    d.icon("fd", "Front_Doors", "Front Door / Traffic Manager / Public IP", "CloudFront / Route 53 policies", 3.3, 3.0)
    d.edge("onp", "res", "conditional forwarding", "private", both=True)
    d.edge("res", "pdns", "", "data", both=True)
    d.edge("pdns", "vnet", "linked", "ok")
    d.edge("pub", "fd", "alias record (works at the apex)", "data")
    d.note("n1", "Private Endpoint zones (privatelink.*) belong in Private DNS and must be linked to every VNet that needs to resolve them.", 0, 0.1, w=520, dx=140)

    # ------------------------------------------------------------------ 4.8
    d = b.D("4.8", "Azure Virtual Network Manager and Route Server (added)", "A",
            "Two services that are not in your study document but fit this topic. Virtual Network Manager applies connectivity and security rules to many VNets at once; Route Server lets an NVA exchange routes with Azure over BGP.",
            [("Central connectivity and security admin rules for many VNets", "Virtual Network Manager"), ("NVA / SD-WAN appliance needs dynamic routing", "Route Server (BGP)")])
    d.icon("avnm", "Azure_Network_Manager", "Virtual Network Manager", "Network Manager / Firewall Manager (partial)", 0.6, 0.6, tag="+ added")
    d.icon("ng1", "Virtual_Networks", "Network group: Prod VNets", "VPCs", 2.4, 0.0)
    d.icon("ng2", "Virtual_Networks", "Network group: Dev VNets", "VPCs", 2.4, 1.3)
    d.icon("cfg", "Subnet", "Hub-spoke or mesh connectivity configuration", "Transit Gateway attachments", 4.2, 0.0)
    d.icon("sec", "Network_Security_Groups", "Security admin rules (override NSGs)", "Firewall Manager SG policy", 4.2, 1.3)
    d.edge("avnm", "ng1", "", "ctrl"); d.edge("avnm", "ng2", "", "ctrl"); d.edge("ng1", "cfg", "applies"); d.edge("ng2", "sec", "applies")
    d.icon("nva", "VNet_Appliance", "NVA / SD-WAN appliance", "third-party appliance", 0.6, 3.0)
    d.icon("rs", "Virtual_Router", "Azure Route Server", "VPC Route Server", 2.4, 3.0, tag="+ added")
    d.icon("vn", "Virtual_Networks", "VNet route table", "VPC route table", 4.2, 3.0)
    d.edge("nva", "rs", "BGP peering", "data", both=True); d.edge("rs", "vn", "injects learned routes", "ok")
    return b
