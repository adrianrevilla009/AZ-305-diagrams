from azdiag import Book

DOM = "Infrastructure (30-35%)"


def build():
    b = Book("05-lb-cdn-apis.drawio", "DNS, CDN, load balancing and APIs", DOM)

    # ---------------------------------------------------------------- 5.1
    d = b.D("5.1", "Load-balancing decision map", "D",
            "Two axes decide the service: global or regional, and HTTP(S) or not. Traffic Manager is DNS-only; Front Door and Application Gateway understand HTTP; Load Balancer is plain TCP/UDP.",
            [("Global web with WAF at the edge", "Front Door"), ("Regional web with URL / host routing", "Application Gateway"),
             ("TCP / UDP traffic", "Load Balancer"), ("Global failover via DNS", "Traffic Manager"),
             ("Kubernetes L7 ingress", "Application Gateway for Containers / AGIC")])
    d.table(0, 0, [
        dict(title="Front Door", icon="Front_Doors", aws="CloudFront + Global Accelerator + WAF", w=190),
        dict(title="Traffic Manager", icon="Traffic_Manager_Profiles", aws="Route 53 routing policies", w=190),
        dict(title="Application Gateway", icon="Application_Gateways", aws="ALB", w=190),
        dict(title="Load Balancer", icon="Load_Balancers", aws="NLB / Gateway LB", w=190),
        dict(title="App Gateway for Containers", icon="Application_Gateway_Containers", aws="AWS Load Balancer Controller", w=190)],
        [("Scope", ["★ Global (anycast at the Microsoft edge)", "★ Global (DNS)", "★ Regional", "★ Regional (cross-region variant makes it global)", "★ Regional, for Kubernetes"]),
         ("Layer", ["L7 HTTP(S)", "DNS only: does not touch the traffic", "L7 HTTP(S)", "L4 TCP / UDP", "L7, Kubernetes-native"]),
         ("What it gives you", ["Acceleration, caching (it is the current CDN), WAF, TLS, latency routing, failover. Premium reaches the origin through Private Link",
                                "Priority, weighted, performance, geographic, multivalue and subnet policies",
                                "URL / host routing, WAF v2, end-to-end TLS, session affinity. Needs a dedicated subnet. AGIC = ingress controller for AKS",
                                "Low latency, high throughput, internal or external, zone support. Standard SKU has an SLA",
                                "Gateway API / ingress for AKS workloads"]),
         ("Watch out", ["Typical chain: Front Door (WAF) > App Gateway > Load Balancer > VMs. For PaaS, Front Door alone is usually enough",
                        "⚠ No TLS termination and no cache. Failover speed depends on the DNS TTL",
                        "Pair with APIM: App Gateway goes in front of APIM",
                        "No L7 awareness (no URL routing, no WAF)",
                        "Prefer it over AGIC for new AKS designs that need L7"])],
        label_w=110)

    # ---------------------------------------------------------------- 5.2
    d = b.D("5.2", "Layered web front end", "A",
            "Global edge first, regional services behind it. Front Door terminates the user connection near them and applies WAF; Application Gateway routes inside the region; Load Balancer spreads TCP to the VMs.",
            [("Web global with WAF at the edge", "Front Door"), ("Origin must not be public", "Front Door Premium + Private Link"),
             ("Azure CDN (classic) is being retired", "migrate to Front Door Standard/Premium ⚠ verify dates")])
    d.box("usr", "Users worldwide", -0.1, 1, w=120, color="gray")
    d.icon("fd", "Front_Doors", "Front Door + WAF (global)", "CloudFront + WAF", 1, 1)
    d.icon("agw", "Application_Gateways", "Application Gateway (URL routing, WAF v2)", "ALB", 2.4, 1)
    d.icon("lb", "Load_Balancers", "Load Balancer Standard (zone-redundant)", "NLB", 3.8, 1)
    d.icon("vm", "Virtual_Machine", "VMs / VM Scale Set", "EC2 Auto Scaling", 5.2, 1)
    d.group("reg", "Region (VNet)", ["agw", "lb", "vm"], "blue")
    d.icon("app", "App_Services", "App Service (PaaS origin)", "Elastic Beanstalk / App Runner", 2.4, 2.6)
    d.edge("usr", "fd", "HTTPS"); d.edge("fd", "agw", "origin"); d.edge("agw", "lb"); d.edge("lb", "vm")
    d.edge("fd", "app", "Private Link origin (Premium)", "private")
    d.note("n1", "Azure CDN (classic Microsoft / Edgio / Verizon) is being retired: migrate to Front Door Standard/Premium.", 0, 3.8, w=520, dx=60)

    # ---------------------------------------------------------------- 5.3
    d = b.D("5.3", "API Management: tiers and placement", "A",
            "APIM publishes, secures and monitors APIs (OAuth/JWT, rate limits, quotas, caching, transformations, versioning, developer portal). Application Gateway handles web traffic and WAF; use both together.",
            [("Quotas and keys on APIs", "APIM"), ("APIs in several regions", "APIM Premium"), ("APIs hosted on-prem or in other clouds", "APIM self-hosted gateway"),
             ("API lifecycle vs web traffic + WAF", "APIM vs Application Gateway: use both, App Gateway in front")])
    d.box("cl", "API clients", -0.1, 1, w=110, color="gray")
    d.icon("agw", "Application_Gateways", "Application Gateway + WAF", "ALB + WAF", 1.1, 1)
    d.icon("apim", "API_Management_Services", "API Management", "API Gateway", 2.5, 1)
    d.icon("app", "App_Services", "App Service / Functions", "Lambda / Beanstalk", 4.1, 0.1)
    d.icon("aks", "Kubernetes_Services", "AKS", "EKS", 4.1, 1.5)
    d.icon("sgw", "API_Management_Services", "Self-hosted gateway (container)", "!", 4.1, 2.9)
    d.group("be", "Backends", ["app", "aks"], "green")
    d.box("onp", "On-prem / other cloud APIs", 5.5, 2.9, w=160, color="gray")
    d.edge("cl", "agw"); d.edge("agw", "apim"); d.edge("apim", "app"); d.edge("apim", "aks"); d.edge("apim", "sgw", "managed from APIM", "ctrl"); d.edge("sgw", "onp")
    d.table(0, 4.1, [dict(title="Key points", w=830)], [
        ("Consumption", ["Serverless, pay per call, no VNet, scales automatically"]),
        ("Developer", ["Testing only, no SLA"]),
        ("Basic / Standard", ["Classic production tiers"]),
        ("Basic v2 / Standard v2", ["Fast scaling, up to 10 units. Standard v2: outbound VNet integration + inbound Private Endpoint"]),
        ("Premium", ["Enterprise: multi-region active-active, availability zones, VNet injection, self-hosted gateway, SLA 99.99%"]),
        ("Premium v2", ["Up to 30 units"])], label_w=180)
    return b
