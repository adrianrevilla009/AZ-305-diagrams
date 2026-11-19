from azdiag import Book

DOM = "Data storage (20-25%)"


def build():
    b = Book("08-databases.drawio", "Databases", DOM)

    # ---------------------------------------------------------------- 8.1
    d = b.D("8.1", "Azure SQL options: which one?", "D",
            "Choose by compatibility versus management effort: SQL Database (PaaS, single or pool), Managed Instance (near-100% SQL Server compatibility), SQL Server on a VM (full OS control).",
            [("Near-100% SQL Server compatibility, lift and shift", "SQL Managed Instance"), ("Full control, unsupported features", "SQL Server on VM"), ("Many databases with variable load", "Elastic pool")])
    d.table(0, 0, [
        dict(title="SQL Database", icon="SQL_Database", aws="RDS for SQL Server", w=190),
        dict(title="SQL Managed Instance", icon="SQL_Managed_Instance", aws="RDS for SQL Server", w=190),
        dict(title="SQL Server on VM", icon="Virtual_Machine", aws="EC2 + SQL Server", w=190)],
        [("Model", ["PaaS, single DB or elastic pool", "PaaS, instance scoped, in your VNet", "IaaS, you manage the OS and engine"]),
         ("Compatibility", ["Most features, no instance-level ones", "★ Near 100%: SQL Agent, cross-DB queries, CLR", "★ 100%, any version"]),
         ("Pick it when", ["New cloud apps, SaaS multi-tenant (pool)", "★ Lift and shift of SQL Server with minimal change", "Unsupported features, OS access, or licence control"])],
        label_w=110)

    # ---------------------------------------------------------------- 8.2
    d = b.D("8.2", "SQL Database purchase and service tiers", "D",
            "Two purchasing models (vCore and DTU) and three main tiers; Hyperscale scales storage up to 100 TB, Serverless pauses when idle.",
            [("Unpredictable, idle periods", "Serverless"), ("Very large DB, fast scale", "Hyperscale"), ("Low-latency, in-memory", "Business Critical")])
    d.table(0, 0, [
        dict(title="General Purpose", icon="SQL_Database", w=170), dict(title="Business Critical", icon="SQL_Database", w=170),
        dict(title="Hyperscale", icon="SQL_Database", aws="Aurora (similar idea)", w=170), dict(title="Serverless", icon="SQL_Database", w=170)],
        [("Architecture", ["Remote storage", "Local SSD, Always On replicas (readable)", "Distributed page servers, up to 100 TB", "General Purpose compute that auto-scales and auto-pauses"]),
         ("Pick it when", ["Most workloads", "★ Lowest latency and highest IOPS", "★ Very large or fast-growing DBs", "★ Intermittent use, pay per second"])],
        label_w=110)
    d.note("n1", "Purchasing: vCore (flexible, reserved capacity, Hybrid Benefit) or DTU (bundled). Hybrid Benefit reuses existing SQL licences.", 0, 2.3, w=700, dx=130)

    # ---------------------------------------------------------------- 8.3
    d = b.D("8.3", "SQL HA and DR", "A",
            "Zone redundancy gives HA within a region; active geo-replication or failover groups give DR across regions with a readable secondary.",
            [("Automatic regional failover with one endpoint", "failover group"), ("Zone outage", "zone-redundant"), ("Restore after error", "PITR / LTR")])
    d.icon("app", "App_Services", "Application", None, 0, 0)
    d.icon("lis", "SQL_Database", "Failover group listener endpoint", "Aurora global endpoint", 1.5, 0)
    d.icon("p", "SQL_Database", "Primary region (zone-redundant)", "RDS Multi-AZ", 3.2, 0)
    d.icon("s", "SQL_Database", "Secondary region (readable)", "Cross-region read replica", 5.0, 0)
    d.edge("app", "lis", "connect", "data"); d.edge("lis", "p", "primary", "data"); d.edge("p", "s", "async replication", "async")
    d.group("gp", "Region A", ["p"], color="blue"); d.group("gs", "Region B", ["s"], color="green")
    d.note("n1", "Backups: automatic PITR (up to 35 days) and long-term retention (up to 10 years) ⚠ verify.", 0, 1.5, w=420, dx=40)

    # ---------------------------------------------------------------- 8.4
    d = b.D("8.4", "Cosmos DB: global distribution", "A",
            "Multi-region writes give active-active with low latency worldwide; conflict resolution defaults to last-writer-wins. Choose the API by the existing data model.",
            [("Global low latency writes", "multi-region writes"), ("Existing MongoDB", "API for MongoDB"), ("Graph", "Gremlin API")])
    d.icon("w", "Azure_Cosmos_DB", "Region 1 (read/write)", "DynamoDB global tables", 0, 0.4)
    d.icon("e", "Azure_Cosmos_DB", "Region 2 (read/write)", None, 1.6, 0.4)
    d.icon("a", "Azure_Cosmos_DB", "Region 3 (read/write)", None, 3.2, 0.4)
    d.edge("w", "e", "replication", "async", both=True); d.edge("e", "a", "replication", "async", both=True)
    d.note("n1", "APIs: NoSQL, MongoDB, Cassandra, Gremlin, Table, PostgreSQL. Throughput: provisioned, autoscale or serverless. Partition key choice decides scale and cost.", 0, 1.7, w=780, dx=0)

    # ---------------------------------------------------------------- 8.5
    d = b.D("8.5", "Cosmos DB consistency ladder", "D",
            "Five levels trade consistency for latency and availability. Session is the default and fits most apps.",
            [("Default, most apps", "Session"), ("Strongest, linearizable", "Strong"), ("Lowest latency, no ordering", "Eventual")])
    d.table(0, 0, [dict(title=t, icon="Azure_Cosmos_DB", w=150) for t in ["Strong", "Bounded staleness", "Session", "Consistent prefix", "Eventual"]],
            [("Guarantee", ["Linearizable reads", "Reads lag by a bound (time or versions)", "★ Read your own writes in a session (default)", "Ordered, never out of order", "No ordering guarantee"]),
             ("Latency / cost", ["Highest latency", "High", "Balanced", "Low", "★ Lowest latency and cost"]),
             ("Note", ["✗ Not with multi-region writes", "Use for ordered global reads", "", "", ""])],
            label_w=110)

    # ---------------------------------------------------------------- 8.6
    d = b.D("8.6", "PostgreSQL and MySQL Flexible Server", "A",
            "Flexible Server runs the community engines with zone-redundant HA, read replicas and stop/start. Use Private access (VNet injection) or Private Endpoint.",
            [("Open-source relational, PaaS", "Flexible Server"), ("Scale reads", "read replicas"), ("HA in zones", "zone-redundant HA")])
    d.icon("app", "App_Services", "App", None, 0, 0.4)
    d.icon("pri", "Azure_Database_PostgreSQL_Server", "Primary (zone 1)", "RDS / Aurora PostgreSQL", 1.6, 0)
    d.icon("stb", "Azure_Database_PostgreSQL_Server", "Standby (zone 2)", "Multi-AZ standby", 1.6, 1.9)
    d.icon("rr", "Azure_Database_PostgreSQL_Server", "Read replica", "Read replica", 3.2, 0.4)
    d.edge("app", "pri", "writes", "data"); d.edge("pri", "rr", "async", "async")
    d.note("n1", "Zone-redundant HA keeps a synchronous standby in another zone, with automatic failover.", 0, 3.2, w=520, dx=80)

    # ---------------------------------------------------------------- 8.7
    d = b.D("8.7", "Azure Managed Redis", "A",
            "In-memory cache for session state, leaderboards and hot data; also a vector store. Cache-aside is the common pattern.",
            [("Reduce database load", "cache-aside"), ("Session state", "Redis")])
    d.icon("app", "App_Services", "App", None, 0, 0.4)
    d.icon("r", "Cache_Redis", "Azure Managed Redis", "ElastiCache / MemoryDB", 1.6, 0.4)
    d.icon("db", "SQL_Database", "Database", "RDS", 3.2, 0.4)
    d.edge("app", "r", "1. read", "data"); d.edge("r", "db", "2. miss: load", "data")
    d.note("n1", "Cache-aside: check cache, on miss read the DB and populate with a TTL. Supports geo-replication and persistence.", 0, 1.7, w=640, dx=40)
    return b
