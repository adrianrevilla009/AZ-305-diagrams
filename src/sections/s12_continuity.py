from azdiag import Book

DOM = "Business continuity (15-20%)"


def build():
    b = Book("12-continuity.drawio", "Business continuity", DOM)

    d = b.D("12.1", "The four DR strategies", "D",
            "Cost falls and recovery time grows from active-active down to backup and restore. Pick by RTO/RPO versus budget.",
            [("Lowest RTO, highest cost", "active-active"), ("Cheapest, slowest", "backup and restore"), ("Core running, scale on failover", "pilot light / warm standby")])
    d.table(0, 0, [dict(title=t, icon="Recovery_Services_Vaults", w=165) for t in ["Backup & restore", "Pilot light", "Warm standby", "Active-active"]],
            [("What runs in region B", ["Only backups", "Data replicated, compute off", "Scaled-down full stack", "Full stack serving traffic"]),
             ("RTO / RPO", ["Hours / hours", "Tens of minutes", "Minutes", "★ Near zero"]),
             ("Cost", ["★ Lowest", "Low", "Medium", "Highest"])],
            label_w=110)

    d = b.D("12.2", "Azure Site Recovery", "A",
            "ASR replicates VMs continuously to a secondary region (or from on-prem) and orchestrates failover with recovery plans.",
            [("Replicate VMs to another region", "Site Recovery"), ("Order failover steps", "recovery plan"), ("Test without impact", "test failover")])
    d.icon("p", "Virtual_Machine", "Primary region VMs", "EC2", 0, 0.4)
    d.icon("v", "Recovery_Services_Vaults", "Recovery Services vault + ASR", "AWS Elastic Disaster Recovery", 1.8, 0.4)
    d.icon("s", "Virtual_Machine", "Secondary region VMs", "EC2 (DR)", 3.6, 0.4)
    d.edge("p", "v", "continuous replication", "async"); d.edge("v", "s", "failover", "ctrl")
    d.note("n1", "Recovery plans sequence groups of VMs. Test failover runs in an isolated network.", 0, 1.8, w=600, dx=0)

    d = b.D("12.3", "Azure Backup", "A",
            "Backup vaults and Recovery Services vaults protect VMs, SQL, files and blobs with policies; immutability and soft delete guard against ransomware.",
            [("Ransomware protection", "immutable vault + soft delete"), ("Cross-region restore", "GRS vault")])
    d.icon("w", "Virtual_Machine", "VMs, SQL, Files, Blobs", None, 0, 0.4)
    d.icon("pol", "Recovery_Services_Vaults", "Vault + backup policy", "AWS Backup", 1.8, 0.4)
    d.icon("im", "Recovery_Services_Vaults", "Immutable / soft-deleted copies", "Backup Vault Lock", 3.6, 0.4)
    d.edge("w", "pol", "scheduled", "data"); d.edge("pol", "im", "retain", "data")

    d = b.D("12.4", "Multi-region active-active", "A",
            "Front Door or Traffic Manager routes users to two regions; each has a full stack, and data uses multi-region writes or replication.",
            [("Global HTTP routing", "Front Door"), ("DNS routing", "Traffic Manager")])
    d.icon("fd", "Front_Doors", "Front Door", "CloudFront + Global Accelerator", 1.8, 0.2)
    d.icon("a", "App_Services", "Region A stack", "ALB + ECS", 0, 1.9)
    d.icon("b", "App_Services", "Region B stack", "ALB + ECS", 3.6, 1.9)
    d.icon("c", "Azure_Cosmos_DB", "Cosmos DB multi-region", "DynamoDB global tables", 1.8, 3.4)
    d.edge("fd", "a", "route", "data", src="l", dst="t"); d.edge("fd", "b", "route", "data", src="r", dst="t")
    d.edge("a", "c", "", "data", src="r", dst="l"); d.edge("b", "c", "", "data", src="l", dst="r")

    d = b.D("12.5", "HA building blocks cheat sheet", "D",
            "Availability grows from single VM to zones to regions; map each level to its SLA.",
            [("Zone outage", "availability zones"), ("Region outage", "paired regions / multi-region")])
    d.table(0, 0, [dict(title="Single VM", icon="Virtual_Machine", w=165), dict(title="Availability set", icon="Availability_Sets", w=165),
                   dict(title="Availability zones", icon="Virtual_Machine", w=165), dict(title="Multi-region", icon="Front_Doors", w=165)],
            [("Protects against", ["Nothing (premium disks only)", "Rack and host failure", "★ Datacenter / zone failure", "★ Region failure"]),
             ("Typical SLA", ["99.9% (premium storage)", "99.95%", "99.99%", "Composite, higher"])],
            label_w=110)

    d = b.D("12.6", "Composite SLA math", "D",
            "Serial dependencies multiply (lower SLA); parallel redundant paths improve availability: 1 - (1-A)(1-B).",
            [("Serial", "multiply SLAs"), ("Parallel", "1 - product of failure rates")])
    d.table(0, 0, [dict(title="Serial", w=250), dict(title="Parallel", w=250)],
            [("Formula", ["A x B", "1 - (1-A)(1-B)"]),
             ("Example", ["99.95% x 99.99% ≈ 99.94%", "Two 99.9% paths ≈ 99.9999%"]),
             ("Effect", ["✗ Lower than weakest link", "✓ Higher than either"])],
            label_w=90)
    return b
