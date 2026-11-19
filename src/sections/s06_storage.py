from azdiag import Book

DOM = "Data storage (20-25%)"


def build():
    b = Book("06-storage.drawio", "Storage", DOM)

    # ---------------------------------------------------------------- 6.1
    d = b.D("6.1", "Redundancy ladder: LRS to RA-GZRS", "D",
            "Redundancy is chosen per storage account. From least to most resilient: LRS < ZRS < GRS < GZRS < RA-GZRS. Replication to the secondary region is asynchronous (RPO > 0) and the secondary is writable only after a failover.",
            [("Survive a zone outage", "ZRS"), ("Survive a region outage and keep reading", "RA-GZRS"), ("Minimum cost, recreatable data", "LRS")])
    d.table(0, 0, [
        dict(title="LRS", icon="Storage_Accounts", aws="S3 One Zone-IA", w=170),
        dict(title="ZRS", icon="Storage_Accounts", aws="S3 Standard (multi-AZ)", w=170),
        dict(title="GRS", icon="Storage_Accounts", aws="S3 CRR", w=170),
        dict(title="GZRS", icon="Storage_Accounts", w=170),
        dict(title="RA-GRS / RA-GZRS", icon="Storage_Accounts", w=170)],
        [("Where the copies are", ["3 copies in one datacenter", "3 copies in 3 zones, synchronous writes", "LRS + async copy to another region", "ZRS in the primary + LRS in the secondary", "Same, but the secondary is readable without a failover"]),
         ("Durability", ["11 nines", "12 nines", "16 nines", "16 nines", "16 nines"]),
         ("Protects against", ["Disk or rack failure", "★ Zone outage", "★ Region outage", "★ Zone + region outage", "★ Zone + region, and reads from the secondary"]),
         ("Watch out", ["Cheapest. Datacenter loss loses data", "No region protection", "Secondary writable only after failover", "Archive tier not supported (ZRS, GZRS, RA-GZRS)", "Archive tier not supported with RA-GZRS"])],
        label_w=120)
    d.note("n1", "Changing the redundancy is an asynchronous process with no time SLA and no downtime.", 0, 3.6, w=700, dx=190)

    # ---------------------------------------------------------------- 6.2
    d = b.D("6.2", "Blob tiers, lifecycle and data protection", "A",
            "Pick the access tier by how often you read the data; lifecycle rules move data automatically. Protect against deletion and tampering with soft delete, versioning, point-in-time restore and WORM.",
            [("Not modifiable or deletable", "immutable (WORM) storage"), ("Cold data", "lifecycle to Cool or Archive"), ("Retention by litigation", "legal hold")])
    d.box("hot", "Hot (AWS S3 Standard): online, costly storage, cheap access", 0, 0.1, w=190, h=72, color="red", bold=False)
    d.box("cool", "Cool (S3 Standard-IA): online, 30-day minimum retention", 1.35, 0.1, w=190, h=72, color="orange", bold=False)
    d.box("cold", "Cold (S3 Glacier Instant Retrieval): online, 90-day minimum", 2.7, 0.1, w=190, h=72, color="blue", bold=False)
    d.box("arch", "Archive (S3 Glacier Flexible / Deep Archive): offline, rehydrate up to ~15 h, 180-day minimum, blob level only", 4.15, 0.1, w=250, h=86, color="purple", bold=False)
    d.chain(["hot", "cool", "cold", "arch"], ["", "", ""])
    d.note("n1", "Moving a blob before its minimum retention costs an early-deletion charge. Lifecycle management (S3 Lifecycle) uses age, last access, prefix or tags. Smart tier (Intelligent-Tiering) moves only between Hot, Cool and Cold ⚠ verify availability.", 0, 1.0, w=900, dx=250)
    d.table(0, 1.7, [dict(title="What it does", w=520), dict(title="AWS", w=240)],
            [("Soft delete", ["Recovers deleted blobs and containers", "-"]),
             ("Versioning", ["Keeps previous versions", "S3 Versioning"]),
             ("Point-in-time restore", ["Restore containers to a moment. Needs versioning + change feed + soft delete", "-"]),
             ("Immutable storage (WORM)", ["★ Time-based retention and legal hold, at container or version level. What SEC 17a-4 asks for", "S3 Object Lock"]),
             ("Object replication", ["Async copy between accounts or regions", "S3 CRR / SRR"]),
             ("Azure Backup for blobs", ["Operational backup of blobs", "AWS Backup for S3"])],
            label_w=170)

    # ---------------------------------------------------------------- 6.3
    d = b.D("6.3", "Securing access to a storage account", "A",
            "Layer identity, network and encryption. Prefer Entra ID (RBAC and user-delegation SAS) over account keys, close the public endpoint, and require secure transfer.",
            [("Restrict Storage to a subnet at no cost", "Service Endpoint"), ("No public endpoint", "Private Endpoint"), ("Customer revokes the keys", "CMK")])
    d.icon("cl", "Virtual_Machine", "Clients / apps", None, 0, 1)
    d.icon("id", "Azure_Active_Directory", "Entra ID: RBAC + user-delegation SAS", "IAM + presigned URLs", 1.5, 1)
    d.icon("net", "Private_Endpoint", "Private Endpoint + storage firewall", "VPC endpoint", 3.0, 1)
    d.icon("sa", "Storage_Accounts", "Storage Account", "S3", 4.5, 1)
    d.icon("kv", "Key_Vaults", "Key Vault: customer-managed key", "KMS", 4.5, 2.6)
    d.chain(["cl", "id", "net", "sa"], ["token", "private IP"]); d.edge("kv", "sa", "CMK", "ctrl", src="t", dst="b")
    d.note("n1", "Disable anonymous access and shared-key access (AWS: Block Public Access). Require secure transfer. Infrastructure (double) encryption is available for regulatory needs.", 0, 2.4, w=480, dx=100)

    # ---------------------------------------------------------------- 6.4
    d = b.D("6.4", "File and block services: which one?", "D",
            "Match the protocol and performance profile: managed SMB/NFS shares, hybrid caching on a Windows Server, enterprise NAS, SAN, or VM disks.",
            [("Managed SMB", "Azure Files"), ("Very high-performance NAS / SAP HANA / NetApp", "Azure NetApp Files"), ("Local cache of cloud shares on-site", "Azure File Sync"),
             ("Migrate an on-prem SAN", "Elastic SAN")])
    d.table(0, 0, [
        dict(title="Azure Files", icon="Storage_Azure_Files", aws="EFS / FSx for Windows", w=165),
        dict(title="Azure File Sync", icon="Storage_Sync_Services", aws="Storage Gateway (File)", w=165),
        dict(title="Azure NetApp Files", icon="Azure_NetApp_Files", aws="FSx for NetApp ONTAP", w=165),
        dict(title="Elastic SAN", icon="Elastic_SAN", w=165),
        dict(title="Managed Disks", icon="Disks", aws="EBS", w=165)],
        [("What it is", ["Managed SMB or NFS file shares", "Local cache of Azure Files on an on-site Windows Server, with tiering to the cloud", "Enterprise NAS (NFS/SMB), sub-millisecond latency", "Cloud SAN over iSCSI with pooled performance", "Block disks for VMs"]),
         ("Pick it when", ["★ Managed SMB", "Hybrid file servers", "★ SAP HANA, Oracle, HPC, VDI, or migrating from on-prem NetApp", "Migrating an on-prem SAN", "VM OS and data disks"])],
        label_w=100)

    # ---------------------------------------------------------------- 6.5
    d = b.D("6.5", "Managed disks: performance ladder", "D",
            "IOPS and throughput grow up the ladder. Premium SSD v2 lets you set IOPS and throughput separately from capacity; Ultra is for sub-millisecond workloads.",
            [("High IOPS and sub-ms latency", "Ultra Disk"), ("Cluster shared disk (WSFC, SQL FCI)", "shared disks"), ("HA across zones", "ZRS disks")])
    d.table(0, 0, [
        dict(title="Standard HDD", icon="Disks", w=170), dict(title="Standard SSD", icon="Disks", w=170), dict(title="Premium SSD", icon="Disks", w=170),
        dict(title="Premium SSD v2", icon="Disks", w=170), dict(title="Ultra Disk", icon="Disks", aws="io2 Block Express", w=170)],
        [("Performance", ["About 500 IOPS, 60 MB/s", "⚠ Web and dev/test (verify limits)", "20,000 IOPS, 900 MB/s", "★ Up to 80,000 IOPS. IOPS and throughput set separately from capacity", "★ 160,000 IOPS, 4,000 MB/s, sub-ms latency, up to 64 TB"]),
         ("Use it for", ["Dev/test and backup", "Web servers, dev/test", "Production and SQL. ZRS version available", "High performance without Ultra cost", "Most demanding databases"]),
         ("Limits", ["", "", "", "✗ Cannot be an OS disk", ""])],
        label_w=110)

    # ---------------------------------------------------------------- 6.6
    d = b.D("6.6", "Data Lake Storage Gen2 and the other storage services", "A",
            "ADLS Gen2 is a storage account with the hierarchical namespace turned on, giving POSIX ACLs for Spark, Synapse, Fabric and Databricks. The same account type also hosts Blob, Files, Queue and Table.",
            [("Data lake with POSIX ACLs", "ADLS Gen2"), ("Simple cheap queue", "Storage Queue (SQS basic)"), ("Simple NoSQL key-value", "Table Storage (DynamoDB basic)")])
    d.icon("src", "Data_Factory", "Ingest (Data Factory)", "Glue ETL", 0, 0.2)
    d.icon("lake", "Data_Lake_Store_Gen1", "ADLS Gen2: hierarchical namespace + POSIX ACLs", "S3 + Lake Formation", 1.6, 0.2)
    d.icon("eng", "Azure_Databricks", "Synapse / Fabric / Databricks", "EMR / Athena / Redshift", 3.3, 0.2)
    d.chain(["src", "lake", "eng"])
    d.icon("q", "Storage_Queue", "Queue Storage", "SQS (basic)", 1.6, 1.9)
    d.icon("t", "Table", "Table Storage", "DynamoDB (basic)", 3.3, 1.9)
    d.icon("f", "Storage_Azure_Files", "Azure Files", "EFS / FSx for Windows", 0, 1.9)
    d.note("n1", "Lake security: POSIX ACLs + RBAC, Private Endpoint, CMK. Managed VNet in Data Factory and Synapse with data-exfiltration protection.", 0, 3.2, w=700, dx=160)
    return b
