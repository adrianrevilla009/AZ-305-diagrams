from azdiag import Book

DOM = "Infrastructure (30-35%)"


def build():
    b = Book("09-messaging-integration.drawio", "Messaging, streaming and integration", DOM)

    # ---------------------------------------------------------------- 9.1
    d = b.D("9.1", "Message vs event: which service?", "D",
            "A message is something the sender expects someone to process (an order, a payment): Service Bus or Storage Queue. An event is a notification that something happened: Event Grid for discrete events, Event Hubs for continuous streams of telemetry.",
            [("Strict order, transactions, duplicate detection", "Service Bus with sessions"), ("Millions of events/s with replay", "Event Hubs"),
             ("React to an Azure event", "Event Grid"), ("Migrate Kafka without code changes", "Event Hubs (Kafka endpoint)"),
             ("Telemetry without commands", "Event Hubs"), ("Simple cheap queue (>80 GB)", "Storage Queue")])
    d.table(0, 0, [
        dict(title="Service Bus", icon="Service_Bus", aws="SQS FIFO + SNS / Amazon MQ", w=200),
        dict(title="Event Grid", icon="Event_Grid_Topics", aws="EventBridge / SNS", w=200),
        dict(title="Event Hubs", icon="Event_Hubs", aws="Kinesis Data Streams / MSK", w=200),
        dict(title="Storage Queue", icon="Storage_Queue", aws="SQS Standard", w=200)],
        [("Is it a...", ["Message (enterprise broker: queues, topics)", "Event (discrete, push routing and fan-out)", "Event stream (partitioned log)", "Message (simple, cheap)"]),
         ("Ordering", ["★ FIFO per session", "✗ None", "★ Per partition (partition key)", "✗ None"]),
         ("Transactions + duplicate detection", ["✓ Only Service Bus", "✗", "✗", "✗"]),
         ("Dead-letter", ["✓ Yes (automatic)", "✓ Yes (to Storage, retries up to 24 h)", "✗ No", "✗ No"]),
         ("Replay", ["✗ No", "✗ No", "✓ Yes, within the retention", "✗ No"]),
         ("Size / notes", ["Premium messages up to 100 MB (256 KB below)", "Destinations: Functions, Logic Apps, Service Bus, Event Hubs, Queue, webhooks", "Capture to Blob/ADLS in Avro. Kafka, AMQP 1.0, HTTPS", "Queues over 80 GB, no DLQ, no sessions"])],
        label_w=140)

    # ---------------------------------------------------------------- 9.2
    d = b.D("9.2", "Service Bus: queues, topics and tiers", "A",
            "Enterprise broker. Topics fan out to subscriptions with filters (like SNS filter policies to SQS). Sessions give FIFO per key; failed messages move to the dead-letter queue after the max delivery count (10 by default).",
            [("Strict order, transactions, duplicates", "Service Bus with sessions"), ("Messages up to 100 MB, VNet, geo-DR", "Premium tier"),
             ("Process once, no loss", "peek-lock (at-least-once, default)"), ("Messages replay", "not possible in Service Bus (use Event Hubs)")])
    d.icon("prod", "Function_Apps", "Producers", "Lambda / apps", 0, 1)
    d.icon("topic", "Service_Bus", "Topic", "SNS topic", 1.5, 1)
    d.icon("sub1", "Service_Bus", "Subscription A (filter)", "SQS + filter policy", 3.0, 0.2)
    d.icon("sub2", "Service_Bus", "Subscription B (filter)", "SQS + filter policy", 3.0, 1.8)
    d.icon("c1", "Function_Apps", "Consumer 1", "Lambda", 4.5, 0.2)
    d.icon("c2", "Function_Apps", "Consumer 2", "Lambda", 4.5, 1.8)
    d.icon("dlq", "Service_Bus", "Dead-letter queue", "SQS DLQ", 4.5, 1.0, tag="after 10 deliveries")
    d.chain(["prod", "topic"]); d.edge("topic", "sub1", "filter"); d.edge("topic", "sub2", "filter")
    d.edge("sub1", "c1", "peek-lock"); d.edge("sub2", "c2", "peek-lock"); d.edge("sub2", "dlq", "expired / max delivery", "bad")
    d.table(0, 3.3, [dict(title="Basic", w=240), dict(title="Standard", w=240), dict(title="Premium", w=360)],
            [("Tier", ["Queues only", "Topics and transactions", "Dedicated resources, messages up to 100 MB (vs 256 KB), VNet / Private Link, geo-DR, zones"]),
             ("Notes", ["", "Sessions = FIFO per session key, one consumer per session", "Geo-DR replicates only metadata, not the messages ⚠ see 12.5"])],
            label_w=90)

    # ---------------------------------------------------------------- 9.3
    d = b.D("9.3", "Event Hubs: partitions, consumer groups, Capture", "A",
            "A partitioned log for millions of events per second. Order is guaranteed inside a partition; parallelism is capped by the partition count. Consumer groups read independently and can replay within the retention.",
            [("Millions of events/s with replay", "Event Hubs"), ("Migrate Kafka without code changes", "Event Hubs Kafka endpoint"), ("Archive the stream automatically", "Capture to Blob / ADLS (Avro)")])
    d.row(1, [("prod", "IoT_Hub", "Producers (apps, devices)", "Kinesis producers")], c0=0)
    d.box("p0", "Partition 0", 1.7, 0.0, w=140, color="blue"); d.box("p1", "Partition 1", 1.7, 0.9, w=140, color="blue")
    d.box("p2", "Partition 2", 1.7, 1.8, w=140, color="blue"); d.box("p3", "Partition 3", 1.7, 2.7, w=140, color="blue")
    d.group("eh", "Event Hubs namespace  (AWS: Kinesis stream / MSK)", ["p0", "p1", "p2", "p3"], "blue")
    d.icon("asa", "Stream_Analytics_Jobs", "Stream Analytics (consumer group 1)", "Managed Flink", 3.6, 0.3)
    d.icon("fn", "Function_Apps", "Functions (consumer group 2)", "Lambda", 3.6, 1.7)
    d.icon("cap", "Storage_Accounts", "Capture to Blob / ADLS (Avro)", "Firehose to S3", 5.2, 1.0)
    d.edge("prod", "p1", "partition key = order per key"); d.edge("p0", "asa"); d.edge("p3", "fn"); d.edge("p2", "cap", "Capture", "async")
    d.table(0, 4.1, [dict(title="Standard", w=250), dict(title="Premium", w=250), dict(title="Dedicated", w=250)],
            [("Capacity", ["Throughput Units: each 1 MB/s in, 2 MB/s out. Retention up to 7 days", "Processing Units, isolation, retention up to 90 days", "Clusters with Capacity Units"]),
             ("Extras", ["Auto-Inflate raises TUs automatically", "Schema Registry, geo-replication for DR, SLA up to 99.99%", "Kafka endpoint + AMQP 1.0 + HTTPS (all tiers); no dead-letter"])],
            label_w=90)

    # ---------------------------------------------------------------- 9.4
    d = b.D("9.4", "Event-driven and telemetry pipelines", "A",
            "Two classic patterns. Discrete events: a blob creation triggers a function that queues work. Continuous telemetry: Event Hubs feeds Stream Analytics that writes to a database or the lake.",
            [("React to an Azure event", "Event Grid"), ("SQL on streams in real time", "Stream Analytics"), ("Work queue with DLQ", "Service Bus"), ("Telemetry without commands", "Event Hubs")])
    d.row(0.2, [("blob", "Blob_Block", "Blob created", "S3 event"), ("eg", "Event_Grid_Topics", "Event Grid (system topic)", "EventBridge"),
                ("fn", "Function_Apps", "Function", "Lambda"), ("sb", "Service_Bus", "Service Bus queue (with DLQ)", "SQS + DLQ"), ("wk", "Logic_Apps", "Worker / Logic App", "Step Functions")], c0=0, step=1.3)
    d.chain(["blob", "eg", "fn", "sb", "wk"], ["event", "trigger", "enqueue", "dequeue"])
    d.row(2.2, [("dev", "IoT_Hub", "Devices / apps", "IoT Core"), ("eh", "Event_Hubs", "Event Hubs", "Kinesis"), ("asa", "Stream_Analytics_Jobs", "Stream Analytics (SQL)", "Managed Flink"),
                ("cos", "Azure_Cosmos_DB", "Cosmos DB (hot)", "DynamoDB")], c0=0, step=1.3)
    d.chain(["dev", "eh", "asa", "cos"], ["telemetry", "", "hot path"])
    d.icon("lake", "Data_Lake_Store_Gen1", "ADLS Gen2 (cold path)", "S3 + Lake Formation", 3.9, 3.5)
    d.edge("asa", "lake", "cold path", "async")

    # ---------------------------------------------------------------- 9.5
    d = b.D("9.5", "IoT: IoT Hub, DPS, IoT Central", "A",
            "IoT Hub is bidirectional (device-to-cloud and cloud-to-device) with an identity and a device twin per device. Its endpoint is Event Hubs-compatible. DPS provisions devices without touching them; IoT Central is the ready-made SaaS.",
            [("Devices that receive commands", "IoT Hub"), ("Telemetry without commands", "Event Hubs"), ("Zero-touch device onboarding", "Device Provisioning Service"), ("Ready-made IoT SaaS", "IoT Central")])
    d.icon("dev", "IoT_Edge", "Devices (IoT Edge)", "Greengrass (approx.)", 0, 1, tag="+ added")
    d.icon("dps", "Device_Provisioning_Services", "Device Provisioning Service", "IoT fleet provisioning", 1.5, 0)
    d.icon("hub", "IoT_Hub", "IoT Hub (D2C + C2D, twin)", "IoT Core", 1.5, 1.5)
    d.icon("asa", "Stream_Analytics_Jobs", "Stream Analytics", "Managed Flink", 3.2, 1.5)
    d.icon("db", "Azure_Cosmos_DB", "Cosmos DB / Data Explorer / ADLS", "DynamoDB / Timestream", 4.8, 1.5)
    d.icon("central", "IoT_Central_Applications", "IoT Central (SaaS)", "IoT SiteWise (partial)", 3.2, 3.0)
    d.icon("twin", "Digital_Twins", "Digital Twins", "IoT TwinMaker", 4.8, 3.0, tag="+ added")
    d.edge("dev", "dps", "zero-touch provisioning", "ctrl"); d.edge("dev", "hub", "telemetry", "data", both=True); d.edge("hub", "asa", "Event Hubs-compatible endpoint"); d.edge("asa", "db")
    d.edge("hub", "central", "SaaS on top", "ctrl")

    # ---------------------------------------------------------------- 9.6
    d = b.D("9.6", "Real-time web, push and low-code", "A",
            "SignalR Service / Web PubSub keep WebSockets open at scale; Notification Hubs sends mobile push; Power Automate gives users low-code automation.",
            [("WebSockets at scale", "SignalR / Web PubSub"), ("Mobile push notifications", "Notification Hubs"), ("Low-code for end users", "Power Automate")])
    d.icon("app", "Function_Apps", "Backend (Functions / App Service)", "Lambda", 0, 1)
    d.icon("sig", "SignalR", "SignalR Service / Web PubSub", "API Gateway WebSocket / AppSync", 1.6, 0.2)
    d.icon("br", "Browser", "Browsers (WebSockets)", "-", 3.2, 0.2)
    d.icon("nh", "Notification_Hubs", "Notification Hubs", "SNS Mobile Push", 1.6, 1.9)
    d.icon("mob", "Mobile", "Mobile apps (APNs / FCM)", "-", 3.2, 1.9)
    d.icon("pa", "PowerAutomate", "Power Automate (low-code)", "-", 1.6, 3.4)
    d.icon("acs", "Azure_Communication_Services", "Communication Services", "Pinpoint / Chime SDK", 3.2, 3.4, tag="+ added")
    d.edge("app", "sig"); d.edge("sig", "br", "", "data"); d.edge("app", "nh"); d.edge("nh", "mob", "push"); d.edge("app", "pa", "", "ctrl")

    # ---------------------------------------------------------------- 9.7
    d = b.D("9.7", "Orchestration: which tool?", "D",
            "Several services glue things together. Match the tool to who builds it (end user, integrator, developer, data engineer).",
            [("SaaS with minimal code", "Logic Apps"), ("Stateful orchestration in code with retries and fan-out", "Durable Functions"),
             ("ETL/ELT across on-prem and cloud", "Data Factory"), ("APIs as a front door", "API Management")])
    d.table(0, 0, [
        dict(title="Logic Apps", icon="Logic_Apps", aws="Step Functions + AppFlow", w=185),
        dict(title="Durable Functions", icon="Function_Apps", aws="Step Functions", w=185),
        dict(title="Data Factory", icon="Data_Factory", aws="Glue ETL + Step Functions / DataSync", w=185),
        dict(title="Power Automate", icon="PowerAutomate", aws="-", w=185),
        dict(title="API Management", icon="API_Management_Services", aws="API Gateway", w=185)],
        [("What it is", ["Low-code workflows with 400+ connectors", "Stateful orchestrations written in code", "ETL/ELT data movement with 100+ connectors", "Low-code automation for end users", "Façade that publishes, secures and monitors APIs"]),
         ("Pick it when", ["SaaS integration with minimal code", "Retries, fan-out/fan-in, long-running logic in code", "Pipelines between on-prem and cloud sources", "Citizens / business users automate their own tasks", "Quotas, keys, OAuth, versioning on APIs"])],
        label_w=110)
    return b
