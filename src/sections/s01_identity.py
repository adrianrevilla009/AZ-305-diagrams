from azdiag import Book

DOM = "Identity, governance and monitoring (25-30%)"


def build():
    b = Book("01-identity-access.drawio", "Identity and access control", DOM)

    # ---------------------------------------------------------------- 1.1
    d = b.D("1.1", "Hybrid authentication and sync: which one?", "D",
            "How on-prem AD users sign in to Entra ID (PHS, PTA, AD FS) and which agent synchronises them (Connect Sync or Cloud Sync). Defaults: PHS for sign-in, Connect Sync as the general tool.",
            [("No password hashes in the cloud", "Pass-through Authentication (PTA)"), ("Simple and resilient", "Password Hash Sync (PHS)"),
             ("Several disconnected AD forests", "Entra Cloud Sync"), ("Smart cards / legacy third-party MFA", "AD FS federation"),
             ("No password prompt on domain-joined PCs", "Seamless SSO (Kerberos) with PHS or PTA")])
    d.table(0, 0, [
        dict(title="Password Hash Sync (PHS)", icon="Entra_Connect", w=250),
        dict(title="Pass-through Authentication (PTA)", icon="Entra_Connect", w=250),
        dict(title="AD FS federation", icon="Azure_AD_Domain_Services", w=250)],
        [("How it works", ["Uploads a hash of the password hash; the sign-in is validated in the cloud", "Validates the password against on-prem AD through agents", "The identity provider stays on-prem"]),
         ("If on-prem goes down", ["✓ Users can still sign in (resilient)", "✗ Needs the on-prem agents", "✗ Needs the on-prem AD FS farm"]),
         ("Pick it when", ["★ Default recommendation. Also detects leaked credentials", "★ Hashes may not be stored in the cloud", "★ Smart cards or legacy third-party MFA only. Most complex"])],
        label_w=130)
    d.table(0, 2.6, [
        dict(title="Entra Connect Sync", icon="Entra_Connect", aws="AD Connector", w=370),
        dict(title="Entra Cloud Sync", icon="Entra_Connect_Sync", aws="-", w=370)],
        [("Agent", ["On-prem agent. Syncs users, groups and hashes", "Lightweight agent configured from the cloud; several agents give high availability"]),
         ("Strengths", ["Complex filtering, writeback, one or several forests. The general option", "Handles several disconnected AD forests (typical after a merger)"]),
         ("Limits", ["Heavier to run", "Not for complex rules"])],
        label_w=130, dy=20)

    # ---------------------------------------------------------------- 1.2
    d = b.D("1.2", "Hybrid identity architecture", "A",
            "On-prem AD syncs to Entra ID. Conditional Access decides access from signals (user, group, app, device, location, risk); Identity Protection supplies the risk. The tenant is the identity boundary.",
            [("Block, require MFA or compliant device on a condition", "Conditional Access (P1)"), ("Risky users / sign-ins", "Identity Protection (P2)"),
             ("Just-in-time admin roles", "PIM (P2)"), ("Instant token revocation", "Continuous Access Evaluation (CAE)")])
    d.icon("ad", "Azure_AD_Domain_Services", "On-prem Active Directory", None, 0, 1)
    d.icon("sync", "Entra_Connect", "Entra Connect Sync / Cloud Sync", "AD Connector", 1.4, 1)
    d.icon("id", "Azure_Active_Directory", "Microsoft Entra ID", "IAM Identity Center", 2.9, 1)
    d.icon("ca", "Conditional_Access", "Conditional Access (P1)", "-", 4.4, 1)
    d.icon("idp", "Entra_ID_Protection", "Identity Protection (P2)", "GuardDuty (partial)", 4.4, 2.4)
    d.group("ten", "Entra ID tenant = identity boundary (a subscription trusts one tenant)", ["id", "ca", "idp"], "blue")
    d.icon("apps", "Enterprise_Applications", "Apps and Azure resources", "-", 6.1, 1)
    d.chain(["ad", "sync", "id", "ca", "apps"], ["users, groups, hashes", "", "signals", "allow / MFA / block"])
    d.edge("idp", "ca", "risk score", "ctrl")
    d.table(0, 3.6, [dict(title="Free", w=250), dict(title="P1", w=250), dict(title="P2", w=300)],
            [("Licences", ["SSO and MFA, security defaults", "Conditional Access", "Identity Protection + PIM"]),
             ("Also", ["Security defaults = free basic MFA, no premium licence", "Authentication Strengths", "SSPR with writeback needs Entra Connect; CAE revokes tokens almost instantly"])],
            label_w=90)

    # ---------------------------------------------------------------- 1.3
    d = b.D("1.3", "External identities: partners and customers", "A",
            "Partners come in as guests (B2B) with their own identity. B2B direct connect avoids a guest object (Teams shared channels). Consumers use a separate external tenant (External ID) with social login and your branding.",
            [("Partner or vendor signs in with their own identity", "B2B collaboration"), ("Shared Teams channels without a guest object", "B2B direct connect"),
             ("Millions of customers with social login", "Entra External ID")])
    d.box("p1", "Partner user (Entra, Google or one-time passcode)", 0, 0.2, w=210, color="gray")
    d.icon("b2b", "External_Identities", "B2B collaboration (guest in your directory)", None, 1.7, 0.2)
    d.icon("ten", "Azure_Active_Directory", "Your Entra tenant", "-", 3.4, 0.2)
    d.box("p2", "Partner user in a trusted tenant", 0, 1.6, w=210, color="gray")
    d.icon("dc", "External_Identities", "B2B direct connect (no guest object)", "-", 1.7, 1.6)
    d.icon("teams", "Collaborative_Service", "Teams shared channels", "-", 3.4, 1.6)
    d.box("cu", "Consumers (self sign-up, Google / Facebook)", 0, 3.0, w=210, color="gray")
    d.icon("ext", "External_ID", "Entra External ID (external tenant, your branding)", "Cognito user pools", 1.7, 3.0)
    d.icon("capp", "App_Services", "Customer-facing app", "-", 3.4, 3.0)
    d.chain(["p1", "b2b", "ten"]); d.chain(["p2", "dc", "teams"], ["mutual trust, blocked by default"]); d.chain(["cu", "ext", "capp"])
    d.note("n1", "External ID replaces Azure AD B2C for new customers ⚠ verify dates.", 4.7, 3.0, w=320, dy=10)

    # ---------------------------------------------------------------- 1.4
    d = b.D("1.4", "Secretless access: managed identity, service principal, federation", "A",
            "Managed identities have no secrets for Azure resources. System-assigned lives and dies with one resource; user-assigned is its own reusable resource. Workload identity federation gives GitHub Actions, Kubernetes or other clouds access without secrets.",
            [("No credentials", "managed identity"), ("External pipeline without secrets", "workload identity federation (OIDC)"),
             ("Minimum role", "e.g. Key Vault Secrets User, not Contributor")])
    d.icon("a1", "App_Services", "App Service", "Elastic Beanstalk / App Runner", 0, 0.1)
    d.icon("m1", "Entra_Managed_Identities", "System-assigned identity (one resource, same lifecycle)", "IAM role (instance profile)", 1.6, 0.1)
    d.icon("t1", "Key_Vaults", "Key Vault", "Secrets Manager", 3.4, 0.1)
    d.icon("a2", "Virtual_Machine", "Several VMs / apps", "EC2", 0, 1.7)
    d.icon("m2", "Managed_Identities", "User-assigned identity (own resource, reusable)", "IAM role", 1.6, 1.7)
    d.icon("t2", "Storage_Accounts", "Storage Account", "S3", 3.4, 1.7)
    d.icon("gh", "Azure_DevOps", "GitHub Actions / Kubernetes / other cloud", None, 0, 3.3)
    d.icon("fed", "Entra_Managed_Identities", "Workload identity federation (OIDC, no secret)", "OIDC with IAM roles", 1.6, 3.3)
    d.icon("t3", "Resource_Groups", "Azure resources", "-", 3.4, 3.3)
    d.chain(["a1", "m1", "t1"], ["token", "RBAC"]); d.chain(["a2", "m2", "t2"], ["token", "RBAC"]); d.chain(["gh", "fed", "t3"], ["federated token", "RBAC"], "ok")
    d.icon("sp", "App_Registrations", "Service principal: secret or certificate you must rotate", "IAM user with access keys", 5.2, 1.7, tag="avoid when possible")

    # ---------------------------------------------------------------- 1.5
    d = b.D("1.5", "Legacy and private apps", "A",
            "Three services bring on-prem and legacy workloads to Entra without VPN or domain controllers.",
            [("LDAP / Kerberos / NTLM for lift-and-shift apps", "Entra Domain Services"), ("Publish internal web app without VPN or inbound ports", "Application Proxy"),
             ("ZTNA for non-web TCP/UDP apps without VPN", "Entra Private Access")])
    d.icon("ds", "Entra_Domain_Services", "Entra Domain Services", "Managed Microsoft AD", 0, 0.2)
    d.box("dsn", "Managed domain with LDAP, Kerberos and NTLM, no domain controllers to deploy. For legacy apps in lift-and-shift.", 1.6, 0.2, w=420, h=60, color="white", bold=False)
    d.icon("ap", "Enterprise_Applications", "Entra Application Proxy", "Verified Access", 0, 1.7)
    d.box("apn", "Publishes internal web apps with SSO. An outbound on-prem connector means no VPN and no inbound ports.", 1.6, 1.7, w=420, h=60, color="white", bold=False)
    d.icon("pa", "Entra_Private_Access", "Entra Private Access", "-", 0, 3.2)
    d.box("pan", "ZTNA access to private non-web apps (TCP/UDP) without a VPN.", 1.6, 3.2, w=420, h=60, color="white", bold=False)

    # ---------------------------------------------------------------- 1.6
    d = b.D("1.6", "Azure RBAC: scope, inheritance and roles", "A",
            "An assignment is principal + role + scope. Scopes inherit downward and permissions add up. Entra roles (Global Admin) are a different plane and are not inherited from Azure RBAC.",
            [("Least privilege for secrets", "Key Vault Secrets User"), ("Conditions on blob tags or attributes", "ABAC"),
             ("Manage access only", "User Access Administrator")])
    d.icon("mg", "Management_Groups", "Management group", "AWS Organizations OU", 0, 0.5)
    d.icon("sub", "Subscriptions", "Subscription", "Account", 1.4, 0.5)
    d.icon("rg", "Resource_Groups", "Resource group", "-", 2.8, 0.5)
    d.icon("res", "Virtual_Machine", "Resource", "EC2", 4.2, 0.5)
    d.chain(["mg", "sub", "rg", "res"], ["inherits down", "inherits down", "inherits down"], "ok")
    d.box("pr", "Principal: user, group, service principal, managed identity", 0, 2.1, w=230, color="gray")
    d.box("ro", "Role: Owner, Contributor, Reader, User Access Administrator", 1.7, 2.1, w=240, color="gray")
    d.box("sc", "Scope: MG, subscription, RG or resource", 3.4, 2.1, w=220, color="gray")
    d.box("as", "= Role assignment", 5.0, 2.1, w=170, color="green")
    d.chain(["pr", "ro", "sc", "as"])
    d.table(0, 3.3, [dict(title="Owner", w=190), dict(title="Contributor", w=190), dict(title="Reader", w=190), dict(title="User Access Administrator", w=230)],
            [("What it can do", ["Everything", "Everything except managing access", "View only", "Only manages access"])], label_w=110)
    d.note("n1", "Typical bad pattern: giving Contributor to something that only reads keys. Use the minimum role. ABAC = RBAC with conditions on attributes or tags (for example on blobs), which avoids creating many roles.", 0, 4.6, w=800, dx=150)
    return b
