from azdiag import Book

DOM = "Identity, governance and monitoring (25-30%)"


def build():
    b = Book("02-governance.drawio", "Governance and multi-subscription", DOM)

    # ---------------------------------------------------------------- 2.1
    d = b.D("2.1", "Landing zone and management group hierarchy", "A",
            "Tenant root group > management groups > subscriptions > resource groups > resources. Policy and RBAC inherit downward. The reference landing zone separates Platform, Landing zones, Sandbox and Decommissioned.",
            [("Isolate billing and quotas", "separate subscriptions"), ("Apply something to many subscriptions", "management group"),
             ("Prohibit regions", "Policy Deny (Allowed locations)")])
    d.icon("root", "Management_Groups", "Tenant root group", "Organizations root", 3.0, 0, side="right")
    d.icon("org", "Management_Groups", "Organisation management group", "Organizations OU", 3.0, 1.0, side="right")
    d.icon("plat", "Management_Groups", "Platform", "OU", 0.8, 2.0, side="right")
    d.icon("lz", "Management_Groups", "Landing zones", "OU", 3.2, 2.0, side="right")
    d.icon("sbx", "Management_Groups", "Sandbox", "OU", 5.0, 2.0, side="right")
    d.icon("dec", "Management_Groups", "Decommissioned", "OU", 6.3, 2.0, side="right")
    d.icon("s1", "Subscriptions", "Identity", "Account", 0.0, 3.2, side="right")
    d.icon("s2", "Subscriptions", "Management", "Account", 1.0, 3.2, side="right")
    d.icon("s3", "Subscriptions", "Connectivity", "Account", 2.0, 3.2, side="right")
    d.icon("s4", "Subscriptions", "Corp workloads", "Account", 3.2, 3.2, side="right")
    d.icon("s5", "Subscriptions", "Online workloads", "Account", 4.3, 3.2, side="right")
    d.icon("s6", "Subscriptions", "Experiments", "Account", 5.3, 3.2, side="right")
    d.tree("root", ["org"]); d.tree("org", ["plat", "lz", "sbx", "dec"])
    d.tree("plat", ["s1", "s2", "s3"]); d.tree("lz", ["s4", "s5"]); d.tree("sbx", ["s6"])
    d.note("n1", "Limits: up to 6 levels deep, 10,000 management groups per tenant. Each MG or subscription has a single parent. Microsoft recommends flat hierarchies of 3-4 levels. New subscriptions land in the tenant root group.", 0, 4.3, w=900, dx=240)

    # ---------------------------------------------------------------- 2.2
    d = b.D("2.2", "Azure Policy: effects and evaluation order", "D",
            "Policy controls what can exist and how it must be configured. RBAC controls who can do what. Start in Audit (or DoNotEnforce) before moving to Deny.",
            [("Prohibit regions", "Deny (Allowed locations)"), ("Force diagnostic settings", "DeployIfNotExists"), ("Enforce or correct configuration at deploy time", "Azure Policy, not Defender")])
    d.table(0, 0, [dict(title="What it does", w=440), dict(title="AWS analogy", w=220)],
            [("Deny", ["★ Blocks creating or changing something non-compliant", "SCP"]),
             ("Audit / AuditIfNotExists", ["Marks non-compliant but does not block", "Config rule"]),
             ("Append / Modify", ["Adds or changes properties or tags. Modify also acts on existing resources", "Tag policies (partly)"]),
             ("DeployIfNotExists", ["Deploys a related resource if missing (diagnostic settings, an agent)", "Config remediation"]),
             ("DenyAction", ["Blocks specific actions such as DELETE", "-"]),
             ("Disabled / Manual", ["Disabled turns the policy off. Manual attests controls Azure cannot evaluate", "-"])],
            label_w=170, row_label_header="Effect")
    d.box("e1", "1 Disabled", 0, 3.0, w=110, color="gray"); d.box("e2", "2 Append / Modify", 0.8, 3.0, w=140, color="blue")
    d.box("e3", "3 Deny", 1.7, 3.0, w=110, color="red"); d.box("e4", "4 Audit", 2.5, 3.0, w=110, color="yellow")
    d.box("e5", "5 AuditIfNotExists", 3.4, 3.0, w=150, color="yellow"); d.box("e6", "6 DenyAction", 4.4, 3.0, w=130, color="red")
    d.chain(["e1", "e2", "e3", "e4", "e5", "e6"])
    d.note("lbl", "Evaluation order:", 0, 3.0, w=150, bold=True, dx=-130, dy=10)
    d.note("n1", "Initiative = a set of policies (AWS: conformance pack), e.g. Microsoft cloud security benchmark, ISO 27001, PCI DSS. DeployIfNotExists and Modify need a managed identity on the assignment; existing resources are fixed with a remediation task.", 0, 3.9, w=900, dx=240)

    # ---------------------------------------------------------------- 2.3
    d = b.D("2.3", "Entra ID Governance", "A",
            "Governance of identity lifecycle and access. AWS has no native IGA product; the closest is IAM Identity Center + Access Analyzer. Licensing: PIM, access reviews and basic entitlement management came with P2; advanced features need Entra ID Governance ⚠ verify the current split.",
            [("Review guests every 90 days", "access reviews"), ("Just-in-time admin roles", "PIM"), ("Request, approve and expire access packages", "entitlement management")])
    d.icon("pim", "Entra_Privileged_Identity_Management", "Privileged Identity Management (PIM)", None, 0, 0)
    d.box("pimn", "Roles are eligible, activated with approval and MFA, and expire. Just-in-time privileged access.", 1.75, 0, w=520, h=48, color="white", bold=False)
    d.icon("ent", "Identity_Governance", "Entitlement management", None, 0, 1.1)
    d.box("entn", "Access packages with request, approval and expiry. Invites and removes B2B guests automatically.", 1.75, 1.1, w=520, h=48, color="white", bold=False)
    d.icon("rev", "Groups", "Access reviews", None, 0, 2.2)
    d.box("revn", "Periodic recertification of groups, apps, roles and guests.", 1.75, 2.2, w=520, h=48, color="white", bold=False)
    d.icon("lw", "Users", "Lifecycle Workflows", None, 0, 3.3)
    d.box("lwn", "Automated joiner, mover and leaver processes (up to 50 workflows).", 1.75, 3.3, w=520, h=48, color="white", bold=False)
    d.icon("tou", "Conditional_Access", "Terms of use", None, 0, 4.4)
    d.box("toun", "Legal acceptance before access, enforced through Conditional Access.", 1.75, 4.4, w=520, h=48, color="white", bold=False)

    # ---------------------------------------------------------------- 2.4
    d = b.D("2.4", "Multi-tenant and hybrid management: Lighthouse and Arc", "A",
            "Lighthouse gives a service provider delegated access to customer tenants without guest accounts. Arc projects servers, Kubernetes and SQL from on-prem or other clouds into Azure so Policy, RBAC, Defender and Monitor apply to them.",
            [("Delegated multi-tenant management for an MSP", "Azure Lighthouse"), ("Apply Policy / Defender to servers outside Azure", "Azure Arc")])
    d.icon("msp", "Azure_Active_Directory", "Service provider tenant", "Delegated admin", 0, 0.2)
    d.icon("lh", "Azure_Lighthouse", "Azure Lighthouse (delegation, no guest accounts)", "Cross-account roles / delegated admin", 1.6, 0.2)
    d.icon("c1", "Subscriptions", "Customer tenant A", "Account", 3.4, 0)
    d.icon("c2", "Subscriptions", "Customer tenant B", "Account", 3.4, 1.4)
    d.chain(["msp", "lh"]); d.edge("lh", "c1"); d.edge("lh", "c2")
    d.icon("srv", "Virtual_Machine", "On-prem / other-cloud servers, Kubernetes, SQL", "-", 0, 3.0)
    d.icon("arc", "Azure_Arc", "Azure Arc", "Systems Manager hybrid + EKS Anywhere", 1.6, 3.0)
    d.icon("plane", "Policy", "Azure control plane: Policy, RBAC, Defender, Monitor", "-", 3.4, 3.0)
    d.chain(["srv", "arc", "plane"], ["project", "manage"])

    # ---------------------------------------------------------------- 2.5
    d = b.D("2.5", "Boundaries: what isolates what", "C",
            "Each level of the hierarchy exists for a reason. Use this table to choose the right boundary.",
            [("Isolate billing and quotas", "separate subscriptions"), ("Apply something to many subscriptions", "management group"),
             ("Tags are not inherited by default", "Policy Modify / inherit a tag"), ("Prevent accidental deletion", "resource lock (CanNotDelete / ReadOnly)")])
    d.table(0, 0, [dict(title="Azure", w=330), dict(title="AWS", w=170), dict(title="Notes", w=360)],
            [("Tenant", ["Identity boundary. A subscription trusts one tenant", "-", "Entra ID directory"]),
             ("Management group", ["Groups subscriptions to apply Policy and RBAC in bulk", "OU (Organizations)", "6 levels, 10,000 per tenant"]),
             ("Subscription", ["Billing, quota and access boundary", "Account", "New ones land in the tenant root group"]),
             ("Resource group", ["Logical container for resources with the same lifecycle", "-", "A resource belongs to exactly one RG"]),
             ("Tags", ["Metadata for cost and ownership", "Cost allocation tags", "⚠ Not inherited by default: use a Modify / 'Inherit a tag' policy"]),
             ("Resource locks", ["CanNotDelete or ReadOnly, inherited downward", "Deletion protection", "Only Owner and User Access Administrator can remove them"]),
             ("Blueprints", ["Retired service (announced for September 2026) ⚠ verify", "Service Catalog", "Replaced by Template Specs + Deployment Stacks + Policy"])],
            label_w=150)
    return b
