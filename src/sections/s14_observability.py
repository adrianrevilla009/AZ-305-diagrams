from azdiag import Book

DOM = "Identity, governance and monitoring (25-30%)"


def build():
    b = Book("14-observability-ops.drawio", "Observability and operations", DOM)

    # ---------------------------------------------------------------- 14.1
    d = b.D("14.1", "Azure Monitor data flow", "A",
            "Platform metrics and the Activity Log are automatic. Resource logs need diagnostic settings; guest OS logs need Azure Monitor Agent + a DCR; apps need Application Insights. Choose the destination by purpose.",
            [("Monitor, alert and dashboard", "Azure Monitor"), ("KQL over logs from several resources", "Log Analytics"),
             ("Resource logs to Splunk", "diagnostic setting to Event Hubs"), ("Archive logs cheaply", "Storage or total retention"), ("Guest OS logs", "AMA + DCR")])
    srcs = [("s1", "Platform metrics + Activity Log (automatic)"), ("s2", "Resource logs (need diagnostic settings)"), ("s3", "Guest OS logs (AMA + DCR)"),
            ("s4", "Application (Application Insights)"), ("s5", "Entra ID sign-in + audit (tenant diagnostic settings)"), ("s6", "AKS (Container Insights + Managed Prometheus)")]
    for i, (k, t) in enumerate(srcs):
        d.box(k, t, 0, i * 0.52, w=300, h=44, color="gray", bold=False)
    d.group("src", "Sources", [k for k, _ in srcs], "gray")
    d.icon("ds", "Diagnostics_Settings", "Diagnostic settings (up to 5 per resource)", "-", 2.0, 0.6)
    d.icon("dcr", "Data_Collection_Rules", "Azure Monitor Agent + DCR (filter / transform with KQL)", "CloudWatch Agent", 2.0, 1.9)
    d.icon("law", "Log_Analytics_Workspaces", "Log Analytics (KQL, alerts, Sentinel)", "CloudWatch Logs + Logs Insights", 4.0, 0)
    d.icon("sa", "Storage_Accounts", "Storage Account (cheap archive, audit)", "S3", 4.0, 1.1)
    d.icon("eh", "Event_Hubs", "Event Hubs (stream to Splunk / QRadar)", "Kinesis", 4.0, 2.2)
    d.icon("pt", "Marketplace", "Partner solution (Datadog, Elastic)", "-", 4.0, 3.3)
    d.edge("s2", "ds"); d.edge("s5", "ds"); d.edge("s3", "dcr"); d.edge("s4", "dcr")
    for t in ("law", "sa", "eh", "pt"):
        d.edge("ds", t)
    d.edge("dcr", "law")
    d.note("n1", "AMA replaces the old MMA / Log Analytics agent (retired ⚠ verify dates). The retention policy inside a diagnostic setting is deprecated: use Storage lifecycle management.", 0, 4.4, w=820, dx=150)

    # ---------------------------------------------------------------- 14.2
    d = b.D("14.2", "Alerts and action groups", "A",
            "Pick the alert type by speed and logic, then route it to an action group. One action group can be reused by many rules.",
            [("Fast alert", "metric alert"), ("Complex logic", "log search alert"), ("VM deleted or RBAC change", "activity log alert"),
             ("Autoscale VMSS / App Service on a metric", "Autoscale (AWS: Auto Scaling policies)")])
    d.box("m", "Metric alert: near-real-time, cheap, dynamic thresholds", 0, 0, w=300, color="blue", bold=False)
    d.box("l", "Log search alert: KQL query, flexible but slower and costlier", 0, 1.0, w=300, color="blue", bold=False)
    d.box("a", "Activity log alert: delete a VM, RBAC changes, Service Health", 0, 2.0, w=300, color="blue", bold=False)
    d.box("p", "Prometheus alert (AKS) / Smart detection (App Insights, ML)", 0, 3.0, w=300, color="blue", bold=False)
    d.icon("ag", "Alerts", "Action group (reusable)", "SNS + EventBridge", 1.8, 1.5)
    d.icon("f", "Function_Apps", "Function", "Lambda", 3.5, 0.0)
    d.icon("la", "Logic_Apps", "Logic App", "Step Functions", 3.5, 1.1)
    d.icon("rb", "Automation_Accounts", "Automation runbook", "SSM Automation", 3.5, 2.2)
    d.icon("eh", "Event_Hubs", "Event Hubs / ITSM", "-", 3.5, 3.3)
    d.box("notif", "Email, SMS, push, voice, webhook", 5.1, 1.1, w=190, color="gray")
    for k in ("m", "l", "a", "p"):
        d.edge(k, "ag")
    for t in ("f", "la", "rb", "eh", "notif"):
        d.edge("ag", t)

    # ---------------------------------------------------------------- 14.3
    d = b.D("14.3", "Log Analytics workspace design", "A",
            "One central workspace by default (simplest and cheapest). Split by region for data sovereignty, by team or environment for admin or billing separation, and keep a dedicated one for Sentinel.",
            [("KQL over logs of several resources", "Log Analytics"), ("Archive logs cheaply", "Storage, or total retention (up to 12 years)"),
             ("Each team sees only its resources' logs", "resource-context RBAC")])
    d.table(0, 0, [dict(title="Analytics", w=270), dict(title="Basic", w=270), dict(title="Auxiliary", w=270)],
            [("Use for", ["Critical logs, alerts and full queries", "High-volume, rarely queried logs", "Low-value, audit and cheap long retention"]),
             ("Interactive retention", ["30 days (90 days for Sentinel and App Insights), up to 2 years", "Fixed 30 days of query", "Minimal ingestion"]),
             ("Alerts", ["✓ Yes", "⚠ Limited ⚠ verify", "✗ No"]),
             ("Total retention (with archive)", ["Up to 12 years in all three plans", "Up to 12 years", "Up to 12 years"])],
            label_w=170)
    d.table(0, 3.0, [dict(title="Placement and access", w=810)],
            [("Workspace layout", ["Central by default; per region/country for sovereignty; per team/env for admin or billing separation; dedicated workspace for Sentinel (different retention and cost)"]),
             ("Access", ["Resource-context RBAC: each team sees only the logs of its resources. Or table-level RBAC"]),
             ("Operations", ["Search jobs and restore recover archived data on demand. Data export rules export tables continuously to Storage or Event Hubs"]),
             ("Cost", ["Commitment tiers give a discount from 100 GB/day. ⚠ Daily cap stops ingestion when reached, and data is lost, including security data"])],
            label_w=170)

    # ---------------------------------------------------------------- 14.4
    d = b.D("14.4", "Application, container and VM insights", "A",
            "Application Insights is APM (traces, dependencies, exceptions) and is workspace-based: its data lives in Log Analytics. Container Insights and VM Insights cover AKS and VMs through Azure Monitor Agent.",
            [("App performance, dependencies, exceptions", "Application Insights"), ("Logs of the OS", "AMA + DCR")])
    d.icon("app", "App_Services", "Apps (SDK or auto-instrumentation, OpenTelemetry)", "-", 0, 0.4)
    d.icon("ai", "Application_Insights", "Application Insights (workspace-based)", "X-Ray + CloudWatch Application Signals", 1.7, 0.4)
    d.icon("aks", "Kubernetes_Services", "AKS: Container Insights + Managed Prometheus / Grafana", "Container Insights / Managed Prometheus", 0, 2.1)
    d.icon("vm", "Virtual_Machine", "VM Insights (AMA)", "CloudWatch Agent + Application Insights", 1.7, 3.3)
    d.icon("law", "Log_Analytics_Workspaces", "Log Analytics workspace", "CloudWatch Logs", 3.7, 1.8)
    d.edge("ai", "law"); d.edge("aks", "law"); d.edge("vm", "law"); d.edge("app", "ai", "telemetry")
    d.note("n1", "Features: Application Map (dependencies), Live Metrics, distributed tracing, availability tests (public URL from several regions), Smart Detection, Profiler, Snapshot Debugger, sampling to reduce cost. Classic mode is retired.", 4.8, 0.2, w=420, dy=5)

    # ---------------------------------------------------------------- 14.5
    d = b.D("14.5", "Diagnostics: who did what, what's broken, where is it", "D",
            "Four tools answer four different questions.",
            [("Audit who created or deleted", "Activity Log"), ("Connectivity between endpoints", "Connection Monitor"),
             ("Azure incident affecting my resources", "Service Health"), ("Inventory across subscriptions", "Resource Graph")])
    d.table(0, 0, [
        dict(title="Network Watcher", icon="Network_Watcher", aws="VPC Flow Logs + Reachability Analyzer + Traffic Mirroring", w=210),
        dict(title="Activity Log", icon="Activity_Log", aws="CloudTrail", w=210),
        dict(title="Service Health / Resource Health", icon="Service_Health", aws="AWS Health Dashboard", w=210),
        dict(title="Resource Graph", icon="Resource_Graph_Explorer", aws="Config aggregator / Resource Explorer", w=210)],
        [("Answers", ["Why is my VM not receiving traffic? Is endpoint A reaching B?", "Who created or deleted a resource (control plane)?", "Is Azure having an incident that affects me?", "What exists across all my subscriptions?"]),
         ("Features", ["Connection Monitor, NSG / VNet flow logs + Traffic Analytics, IP flow verify, next hop, packet capture", "Automatic, 90 days retention; use a diagnostic setting for longer", "Service Health: incidents and maintenance on your subscription. Resource Health: one resource. Azure Status: global",
                       "KQL at scale over resource inventory. Change Analysis shows who changed what"]),
         ("Note", ["NSG flow logs are moving to VNet flow logs ⚠ verify retirement", "", "Alerts available", ""])],
        label_w=90)

    # ---------------------------------------------------------------- 14.6
    d = b.D("14.6", "Operations automation", "D",
            "Automate runbooks, patching and recommendations. Arc brings AMA and Update Manager to servers outside Azure.",
            [("Patch VMs", "Update Manager"), ("Inventory across subscriptions", "Resource Graph"), ("Best-practice recommendations", "Advisor")])
    d.table(0, 0, [
        dict(title="Azure Automation", icon="Automation_Accounts", aws="Systems Manager Automation", w=210),
        dict(title="Update Manager", icon="Update_Center", aws="Systems Manager Patch Manager", w=210),
        dict(title="Azure Arc", icon="Azure_Arc", aws="SSM hybrid activations / EKS Anywhere", w=210),
        dict(title="Advisor", icon="Advisor", aws="Trusted Advisor", w=210)],
        [("What it does", ["Runbooks and operations automation. Includes Change Tracking", "Central patching of Azure VMs and on-prem servers (with Arc)", "Manages on-prem or multicloud servers, Kubernetes and DBs with the Azure plane",
                           "Recommendations on cost, reliability, security, performance and operational excellence"])],
        label_w=90)
    return b
