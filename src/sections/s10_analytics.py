from azdiag import Book

DOM = "Data analytics (20-25%)"


def build():
    b = Book("10-analytics.drawio", "Analytics and data platform", DOM)

    # ---------------------------------------------------------------- 10.1
    d = b.D("10.1", "Analytics engines: which one?", "D",
            "Fabric is the unified SaaS platform; Synapse, Databricks, Data Explorer and HDInsight remain for specific needs.",
            [("Unified SaaS analytics", "Fabric"), ("Spark-first, ML, open lakehouse", "Databricks"), ("Logs and time-series, KQL", "Data Explorer"), ("Open-source Hadoop/Kafka", "HDInsight")])
    d.table(0, 0, [
        dict(title="Microsoft Fabric", icon="Azure_Synapse_Analytics", aws="-", w=165),
        dict(title="Synapse Analytics", icon="Azure_Synapse_Analytics", aws="Redshift + Athena", w=165),
        dict(title="Databricks", icon="Azure_Databricks", aws="EMR / Databricks", w=165),
        dict(title="Data Explorer", icon="Azure_Data_Explorer_Clusters", w=165),
        dict(title="HDInsight", icon="HD_Insight_Clusters", aws="EMR", w=165)],
        [("Strength", ["★ All-in-one SaaS on OneLake", "SQL warehouse + Spark, existing estates", "★ Spark, ML, Delta lakehouse", "★ Logs, telemetry, time-series with KQL", "Managed Hadoop, Spark, Kafka, HBase"]),
         ("Pick it when", ["New platform, one capacity, Power BI", "Existing Synapse investments", "Data science and large Spark", "Interactive log analytics", "Lift-and-shift open-source big data"])],
        label_w=100)

    # ---------------------------------------------------------------- 10.2
    d = b.D("10.2", "Medallion data platform", "A",
            "Ingest raw data into Bronze, clean to Silver, model to Gold, then serve to BI and ML. Governance spans all layers.",
            [("Raw, immutable landing", "Bronze"), ("Curated for reports", "Gold")])
    d.icon("src", "Data_Factory", "Sources + ingestion", "Glue / DMS", 0, 0.3)
    d.icon("br", "Data_Lake_Store_Gen1", "Bronze (raw)", "S3 raw zone", 1.5, 0.3)
    d.icon("si", "Data_Lake_Store_Gen1", "Silver (cleaned)", "S3 curated", 3.0, 0.3)
    d.icon("go", "Data_Lake_Store_Gen1", "Gold (modeled)", "S3 gold + Redshift", 4.5, 0.3)
    d.icon("bi", "Power_BI_Embedded", "Power BI", "QuickSight", 6.0, 0.3)
    d.chain(["src", "br", "si", "go", "bi"], ["ingest", "clean", "model", "serve"])
    d.icon("pv", "Azure_Purview_Accounts", "Microsoft Purview governance", "Glue Data Catalog / Lake Formation", 3.0, 2.0)
    d.edge("pv", "si", "catalog + lineage", "ctrl", src="t", dst="b")
    d.note("n1", "Delta/Parquet formats, ADLS Gen2 as storage, Spark or SQL for transforms.", 0, 2.1, w=420, dx=0)

    # ---------------------------------------------------------------- 10.3
    d = b.D("10.3", "Data Factory integration runtimes", "D",
            "Pick the runtime by where the data lives: Azure IR for cloud, self-hosted IR for on-prem or private networks, Azure-SSIS IR for SSIS packages.",
            [("On-premises source", "self-hosted IR"), ("Run SSIS packages", "Azure-SSIS IR"), ("Private PaaS sources", "managed VNet IR")])
    d.table(0, 0, [
        dict(title="Azure IR", icon="Data_Factory", w=170), dict(title="Self-hosted IR", icon="Data_Factory", w=170),
        dict(title="Azure-SSIS IR", icon="Data_Factory", w=170), dict(title="Managed VNet IR", icon="Data_Factory", w=170)],
        [("Where it runs", ["Azure-managed, public", "Your VM on-prem or in a VNet", "Azure-managed cluster for SSIS", "Azure-managed inside a managed VNet"]),
         ("Pick it when", ["Cloud-to-cloud copies", "★ On-prem or private network sources", "★ Lifting SSIS packages", "★ Private Endpoints, exfiltration protection"])],
        label_w=110)

    # ---------------------------------------------------------------- 10.4
    d = b.D("10.4", "Streaming: hot, warm and cold paths", "A",
            "Events arrive through Event Hubs; a hot path analyses in real time while a cold path lands data in the lake for batch.",
            [("Real-time SQL on streams", "Stream Analytics"), ("Replay / long retention", "Capture to lake"), ("Telemetry store", "Data Explorer")])
    d.icon("eh", "Event_Hubs", "Event Hubs", "Kinesis Data Streams", 0, 1.0)
    d.icon("sa", "Stream_Analytics_Jobs", "Stream Analytics (hot)", "Managed Flink", 1.8, 0)
    d.icon("adx", "Azure_Data_Explorer_Clusters", "Data Explorer (warm)", "Timestream / OpenSearch", 3.6, 0)
    d.icon("lk", "Data_Lake_Store_Gen1", "ADLS Gen2 (cold)", "S3", 1.8, 2.0)
    d.icon("sy", "Azure_Synapse_Analytics", "Synapse / Fabric (batch)", "Athena / Redshift", 3.6, 2.0)
    d.edge("eh", "sa", "hot", "data"); d.edge("sa", "adx", "results", "data"); d.edge("eh", "lk", "Capture", "async"); d.edge("lk", "sy", "batch", "data")

    # ---------------------------------------------------------------- 10.5
    d = b.D("10.5", "Microsoft Purview", "A",
            "Purview scans sources, builds a data map and catalog, tracks lineage and applies sensitivity labels and policies across the estate.",
            [("Catalog, lineage, classification", "Purview"), ("Sensitivity labels", "Purview Information Protection")])
    d.icon("s1", "Data_Lake_Store_Gen1", "Sources: lakes, SQL, Fabric, on-prem, other clouds", "Glue Data Catalog", 0, 0.4)
    d.icon("pv", "Azure_Purview_Accounts", "Purview: scan + classify", "Lake Formation / Macie", 1.8, 0.4)
    d.icon("map", "Azure_Purview_Accounts", "Data map + catalog + lineage", "Glue Data Catalog", 3.6, 0.4)
    d.edge("s1", "pv", "scan", "ctrl"); d.edge("pv", "map", "publish", "data")
    d.note("n1", "Governance domains, data products, access policies and sensitivity labels. Pairs with Defender for Cloud for security posture.", 0, 1.8, w=700, dx=0)

    # ---------------------------------------------------------------- 10.6
    d = b.D("10.6", "Fabric concepts", "A",
            "One capacity powers every Fabric workload on OneLake; shortcuts reference external data without copying, and Direct Lake reads lake files from Power BI.",
            [("Reference data without copy", "shortcut"), ("Power BI over lake files", "Direct Lake"), ("Pay once for all workloads", "capacity")])
    d.icon("cap", "Azure_Synapse_Analytics", "Fabric capacity", None, 0, 0.4)
    d.icon("ol", "Data_Lake_Store_Gen1", "OneLake", "S3 (unified)", 1.8, 0.4)
    d.icon("sc", "Storage_Accounts", "Shortcuts: ADLS, S3, others", "S3", 3.6, 0)
    d.icon("pb", "Power_BI_Embedded", "Power BI (Direct Lake)", "QuickSight", 3.6, 1.9)
    d.edge("cap", "ol", "powers", "ctrl"); d.edge("sc", "ol", "no copy", "data"); d.edge("ol", "pb", "Direct Lake", "data")
    d.note("n1", "Workloads: Data Factory, Data Engineering, Warehouse, Real-Time Intelligence, Data Science, Power BI, Databases.", 0, 3.2, w=700, dx=0)
    return b
