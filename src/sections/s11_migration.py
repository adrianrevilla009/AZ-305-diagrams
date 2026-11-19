from azdiag import Book

DOM = "Infrastructure (30-35%)"


def build():
    b = Book("11-migration.drawio", "Migration", DOM)

    # ---------------------------------------------------------------- 11.1
    d = b.D("11.1", "Cloud Adoption Framework and the migration Rs", "C",
            "CAF is a methodology, not a service. Build the landing zone before moving workloads, then choose a migration strategy per workload.",
            [("Move fast without touching code", "Rehost"), ("PaaS with minimal changes", "Refactor"), ("Several hundred VMs, low downtime", "Azure Migrate Server Migration"),
             ("Keep vSphere as it is", "Azure VMware Solution")])
    for i, (k, t, c) in enumerate([("s", "Strategy", "gray"), ("p", "Plan", "gray"), ("r", "Ready (landing zone)", "blue"), ("a", "Adopt (migrate or innovate)", "green"), ("g", "Govern", "orange"), ("m", "Manage", "orange")]):
        d.box(k, t, i * 0.95, 0.2, w=170, color=c)
    d.chain(list("sprag") + ["m"])
    d.box("a1", "Assess", 0.5, 1.0, w=140, color="white"); d.box("a2", "Migrate", 1.7, 1.0, w=140, color="white")
    d.box("a3", "Optimize", 2.9, 1.0, w=140, color="white"); d.box("a4", "Secure and manage", 4.1, 1.0, w=170, color="white")
    d.chain(["a1", "a2", "a3", "a4"])
    d.note("jn", "Migration journey:", 0, 1.0, w=150, bold=True, dx=-90, dy=10)
    d.table(0, 1.8, [dict(title="Rehost", w=160), dict(title="Refactor", w=160), dict(title="Rearchitect", w=160), dict(title="Rebuild", w=160), dict(title="Replace", w=160), dict(title="Retire", w=160)],
            [("What it means", ["Move as-is to VMs. Low effort", "Minimal changes to use PaaS", "Redesign to be cloud-native", "Rewrite from scratch", "Swap for a SaaS product", "Switch it off"]),
             ("Example", ["VMs to Azure VMs", ".NET app to App Service; SQL Server to SQL MI", "Monolith to AKS", "New code base", "Move mail to SaaS", "Decommission"])],
            label_w=110)
    d.note("n1", "Before moving workloads, build the landing zone: subscriptions, management groups, network, identity and policies (AWS: Control Tower).", 0, 3.4, w=700, dx=190)

    # ---------------------------------------------------------------- 11.2
    d = b.D("11.2", "Azure Migrate: server migration", "A",
            "Azure Migrate discovers servers (VMware, Hyper-V, physical, other clouds), sizes them from real performance and replicates them continuously for a short cutover. AVS keeps vSphere unchanged; Resource Mover relocates between Azure regions.",
            [("Hundreds of VMware VMs, low downtime", "Azure Migrate Server Migration"), ("Keep vSphere unchanged", "Azure VMware Solution"),
             ("Move resources between regions", "Resource Mover"), (".NET / PHP websites to PaaS", "App Service Migration Assistant")])
    d.box("vm", "VMware", 0, 0, w=110, color="gray"); d.box("hv", "Hyper-V", 0, 0.9, w=110, color="gray")
    d.box("ph", "Physical servers", 0, 1.8, w=110, color="gray"); d.box("oc", "Other clouds", 0, 2.7, w=110, color="gray")
    d.group("src", "Source", ["vm", "hv", "ph", "oc"], "gray")
    d.icon("am", "Azure_Migrate", "Azure Migrate: discovery + assessment", "Migration Hub + Application Discovery", 1.6, 1.0)
    d.icon("sm", "Azure_Migrate", "Server Migration: continuous replication", "Application Migration Service (MGN)", 3.1, 1.0)
    d.icon("az", "Virtual_Machine", "Azure VMs (low-downtime cutover)", "EC2", 4.7, 1.0)
    d.chain(["am", "sm", "az"], ["right-size from real performance", "replicate"])
    d.icon("avs", "AVS", "Azure VMware Solution", "VMware Cloud on AWS", 3.1, 2.6)
    d.icon("rm", "Resource_Mover", "Resource Mover (region to region)", "-", 4.7, 2.6)
    d.icon("asma", "App_Services", "App Service Migration Assistant", "-", 1.6, 2.6)
    d.note("n1", "Assessment is a point-in-time snapshot (recalculate). Dependency analysis groups servers into apps, agentless or with an agent. Business case compares on-prem cost with Azure. The containerization tool is for containers and Java (AWS App2Container).", 0, 3.7, w=760, dx=150)
    d.edge("vm", "am", "", "ctrl")

    # ---------------------------------------------------------------- 11.3
    d = b.D("11.3", "Database migration paths", "A",
            "Assess compatibility first (DMA), then migrate with DMS online (continuous replication, short cutover) or offline (full stop). Heterogeneous moves need a schema conversion step.",
            [("SQL Server with SQL Agent / linked servers to PaaS", "SQL MI with DMS online or Log Replay Service"), ("Low-downtime SQL Server to MI", "DMS online, LRS, native restore or MI link"),
             ("Oracle to PostgreSQL", "SSMA or ora2pg for the schema (AWS SCT)")])
    d.icon("src", "SQL_Server", "Source: SQL Server on-prem", "RDS source", 0, 1)
    d.icon("dma", "Azure_Database_Migration_Services", "Data Migration Assistant (assessment)", "Schema Conversion Tool", 1.5, 1)
    d.icon("dms", "Azure_Database_Migration_Services", "Database Migration Service: online or offline", "AWS DMS", 3.0, 1)
    d.icon("sqldb", "SQL_Database", "SQL Database", "RDS for SQL Server", 4.7, 0)
    d.icon("mi", "SQL_Managed_Instance", "SQL Managed Instance", "RDS Custom for SQL Server", 4.7, 1)
    d.icon("vm", "Azure_SQL_VM", "SQL Server on VM", "SQL Server on EC2", 4.7, 2)
    d.chain(["src", "dma", "dms"]); d.edge("dms", "sqldb"); d.edge("dms", "mi"); d.edge("dms", "vm")
    d.icon("ora", "Oracle_Database", "Oracle / heterogeneous source", "RDS for Oracle", 0, 3.2)
    d.icon("ssma", "Azure_Database_Migration_Services", "SSMA / ora2pg (schema conversion)", "SCT", 1.5, 3.2)
    d.icon("pg", "Azure_Database_PostgreSQL_Server", "PostgreSQL / MySQL Flexible Server", "RDS / Aurora", 4.7, 3.2)
    d.chain(["ora", "ssma"]); d.edge("ssma", "pg", "then DMS")
    d.note("n1", "SQL Server to SQL MI with low downtime: DMS online, Log Replay Service (LRS), native restore, or MI link (distributed Always On).", 3.0, 2.2, w=380, dx=-60, dy=60)

    # ---------------------------------------------------------------- 11.4
    d = b.D("11.4", "Data transfer: online or offline?", "D",
            "Decide with arithmetic: size divided by bandwidth. 200 TB over 1 Gbps takes about 26 days. If that does not fit the window, go offline with Data Box.",
            [("A few TB, good bandwidth", "AzCopy or Storage Mover"), ("400 TB and a slow network", "several Data Box or Data Box Heavy"),
             ("Export from Azure to disk", "Data Box (Disk and Heavy do not support export)")])
    d.table(0, 0, [
        dict(title="AzCopy", icon="Storage_Explorer", aws="s3 sync", w=140),
        dict(title="Storage Mover", icon="Azure_Storage_Mover", aws="DataSync", w=140),
        dict(title="Data Box Disk", icon="Data_Box", aws="Snowcone", w=140),
        dict(title="Data Box", icon="Data_Box", aws="Snowball Edge", w=140),
        dict(title="Data Box Heavy", icon="Data_Box", aws="Snowmobile / several Snowballs", w=140),
        dict(title="Data Box Gateway", icon="Data_Box_Edge", aws="Storage Gateway", w=140),
        dict(title="Import / Export", icon="Import_Export_Jobs", aws="-", w=140)],
        [("Mode", ["Online (CLI over the network)", "Online (orchestrated NFS/SMB shares to Blob/Files)", "★ Offline", "★ Offline", "★ Offline", "Online (virtual appliance uploads over the network)", "Offline: you ship your own disks"]),
         ("Capacity / interface", ["Copy to Blob or Files", "Shares to Blob / Files", "About 35 TB usable (up to 5 x 8 TB), USB", "About 80 TB usable (100 TB raw), SMB/NFS, AES-256", "About 800 TB usable (1 PB raw)", "Virtual appliance", "Use if no Data Box is available in your region"]),
         ("Export from Azure?", ["n/a", "n/a", "✗ No", "✓ Yes", "✗ No", "n/a", "✓ Yes"])],
        label_w=120)
    d.note("n1", "Rule of thumb: time = size / bandwidth. 200 TB over 1 Gbps is about 26 days. If it does not fit the migration window, go offline.", 0, 3.5, w=640, dx=180)
    return b
