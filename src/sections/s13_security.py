from azdiag import Book

DOM = "Security and compliance"


def build():
    b = Book("13-security.drawio", "Security", DOM)

    d = b.D("13.1", "Defender for Cloud: CSPM vs CWPP", "A",
            "CSPM assesses posture and recommends fixes (Secure Score); CWPP (Defender plans) detects threats on workloads.",
            [("Posture and recommendations", "CSPM"), ("Threat protection per workload", "Defender plans")])
    d.icon("res", "Virtual_Machine", "Subscriptions, multicloud", None, 0, 0.4)
    d.icon("cspm", "Security_Center", "CSPM: Secure Score, recommendations", "Security Hub", 1.8, 0)
    d.icon("cwpp", "Security_Center", "CWPP: Defender plans", "GuardDuty / Inspector", 1.8, 1.9)
    d.edge("res", "cspm", "posture", "ctrl"); d.edge("res", "cwpp", "threats", "ctrl")

    d = b.D("13.2", "Defender plan map", "D",
            "Each Defender plan protects a workload type.",
            [("Servers", "Defender for Servers"), ("Storage malware", "Defender for Storage"), ("Containers", "Defender for Containers")])
    d.table(0, 0, [dict(title="Servers", icon="Virtual_Machine", w=150), dict(title="Storage", icon="Storage_Accounts", w=150),
                   dict(title="Databases", icon="SQL_Database", w=150), dict(title="Containers", icon="Kubernetes_Services", w=150),
                   dict(title="App Service / Key Vault", icon="Key_Vaults", w=150)],
            [("Protects", ["VM threat detection, vulnerability scanning", "Malware scan, sensitive data", "SQL, open-source, Cosmos threats", "AKS and registries", "Web apps and secrets access"])],
            label_w=90)

    d = b.D("13.3", "Microsoft Sentinel", "A",
            "Cloud-native SIEM and SOAR on Log Analytics: connectors ingest data, analytics rules create incidents, playbooks (Logic Apps) automate response.",
            [("SIEM + SOAR", "Sentinel"), ("Automated response", "playbooks")])
    d.icon("c", "Log_Analytics_Workspaces", "Data connectors", None, 0, 0.4)
    d.icon("w", "Log_Analytics_Workspaces", "Log Analytics workspace", "Security Lake", 1.6, 0.4)
    d.icon("s", "Azure_Sentinel", "Sentinel analytics + incidents", "Security Hub", 3.2, 0.4)
    d.icon("p", "Logic_Apps", "Playbooks", "EventBridge + Lambda", 4.8, 0.4)
    d.chain(["c", "w", "s", "p"], ["ingest", "detect", "respond"])

    d = b.D("13.4", "Defense in depth and compliance tools", "D",
            "Layered controls from identity to data; Defender for Cloud regulatory compliance and Policy track standards.",
            [("Regulatory compliance dashboard", "Defender for Cloud"), ("Enforce standards", "Azure Policy")])
    d.table(0, 0, [dict(title="Layer", w=200), dict(title="Controls", w=520)],
            [("Identity", ["Entra ID, MFA, Conditional Access, PIM"]), ("Network", ["NSG, Firewall, WAF, Private Link"]),
             ("Compute", ["Defender for Servers, patching, Trusted Launch"]), ("Data", ["Encryption, Key Vault, Purview labels"]),
             ("Governance", ["Policy, Blueprints/Deployment Stacks, Defender compliance"])],
            label_w=90)
    return b
