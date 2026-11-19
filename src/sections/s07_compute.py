from azdiag import Book

DOM = "Infrastructure (30-35%)"


def build():
    b = Book("07-compute.drawio", "Compute", DOM)

    # ---------------------------------------------------------------- 7.1
    d = b.D("7.1", "Compute decision map", "D",
            "Pick by how much you want to manage: full OS control (VM), managed web apps (App Service), serverless containers (Container Apps), full Kubernetes (AKS), one-off container (ACI), event code (Functions), batch jobs (Batch).",
            [("Full OS control, COTS, lift-and-shift", "VM"), ("Managed web app / API", "App Service"),
             ("Containers, no K8s to manage, scale to zero", "Container Apps"), ("Operators, CRDs, full K8s control", "AKS"),
             ("A one-off container", "ACI"), ("Zero-downtime release and instant rollback", "App Service deployment slots"),
             ("Thousands of cheap batch tasks", "Batch + Spot")])
    d.table(0, 0, [
        dict(title="Virtual Machines", icon="Virtual_Machine", aws="EC2", w=150),
        dict(title="App Service", icon="App_Services", aws="Elastic Beanstalk / App Runner", w=150),
        dict(title="Container Apps", icon="Container_App_Environments", aws="App Runner / ECS Fargate", w=150),
        dict(title="AKS", icon="Kubernetes_Services", aws="EKS", w=150),
        dict(title="Container Instances", icon="Container_Instances", aws="Fargate (single task)", w=150),
        dict(title="Functions", icon="Function_Apps", aws="Lambda", w=150),
        dict(title="Batch", icon="Batch_Accounts", aws="AWS Batch", w=150)],
        [("Pick it when", ["Full OS control, COTS software, lift-and-shift", "Web apps and APIs without managing servers", "Containers without managing Kubernetes; events or HTTP; scale to zero",
                           "You need Kubernetes control: operators, CRDs", "One container or a group, no orchestration", "Event-driven code", "Parallel and HPC jobs on pools of VMs"]),
         ("You manage", ["The OS and everything above", "Just the app (plan sizing)", "Containers and scaling rules (KEDA); not K8s", "Nodes pools, upgrades, K8s objects", "Nothing but the container; manual scale", "Just the code", "Pools and jobs; the service itself has no extra cost"]),
         ("Scale / limits", ["VM Scale Sets (Flexible mode recommended)", "Up to 30 instances, 100 with ASE", "KEDA, revisions and traffic splitting, Dapr", "HPA, cluster autoscaler, KEDA; virtual nodes (ACI) for bursts",
                             "Billed per second, manual scale", "About 200 instances per function app", "Batch + Spot VMs for cheap bulk work"])],
        label_w=110)

    # ---------------------------------------------------------------- 7.2
    d = b.D("7.2", "Highly available VMs", "A",
            "VM SLA depends on placement: single instance with Premium SSD/Ultra 99.9%, Availability Set 99.95%, Availability Zones 99.99%. Scale Sets spread instances across zones behind a zone-redundant Load Balancer.",
            [("Survive a datacenter failure", "Availability Zones (99.99%)"), ("Same datacenter, rack-level protection", "Availability Set (99.95%)"),
             ("VMs close together, low latency", "Proximity placement group"), ("Licensing / compliance hardware", "Dedicated Host"),
             ("Interruptible, up to 90% cheaper", "Spot VMs")])
    d.icon("lb", "Load_Balancers", "Load Balancer Standard (zone-redundant)", "NLB", 0, 1.1)
    for i, z in enumerate(("Zone 1", "Zone 2", "Zone 3")):
        d.icon(f"vm{i}", "Virtual_Machine", f"VM instance", "EC2", 1.7, 0 + i * 1.15)
        d.group(f"z{i}", z, [f"vm{i}"], "gray", pad=(70, 36, 70, 20))
    d.group("vmss", "VM Scale Set - Flexible mode (autoscale)  (AWS: Auto Scaling Group)", ["z0", "z1", "z2"], "blue")
    d.icon("ppg", "Proximity_Placement_Groups", "Proximity placement group", "Cluster placement group", 3.7, 0)
    d.icon("host", "Hosts", "Dedicated Host", "EC2 Dedicated Hosts", 3.7, 1.15)
    d.icon("spot", "Spot_VM", "Spot VMs / Hybrid Benefit", "Spot Instances / BYOL", 3.7, 2.3)
    d.edge("lb", "vm0"); d.edge("lb", "vm1"); d.edge("lb", "vm2")
    d.table(0, 3.75, [dict(title="Single instance (Premium SSD / Ultra)", w=300), dict(title="Availability Set (2+ VMs)", w=300), dict(title="Availability Zones (2+ VMs in different zones)", w=330)],
            [("VM SLA", ["99.9%", "99.95% (fault + update domains)", "99.99%"])], label_w=110)

    # ---------------------------------------------------------------- 7.3
    d = b.D("7.3", "App Service: plans, slots and networking", "A",
            "An App Service Plan is the compute; several apps can share it. Deployment slots give blue/green releases with a swap. VNet Integration is outbound, Private Endpoint is inbound.",
            [("Zero-downtime release, quick rollback", "deployment slots (Standard tier or higher)"), ("Full isolation in your VNet", "Isolated v2 / ASE"),
             ("PaaS reaching a private DB", "VNet Integration (outbound)"), ("Block public access to the app", "Private Endpoint (inbound)")])
    d.box("cl", "Clients", -0.2, 1, w=100, color="gray")
    d.icon("pe", "Private_Endpoint", "Private Endpoint (inbound)", "VPC interface endpoint", 0.9, 1)
    d.icon("prod", "App_Services", "Web app - production slot", "Elastic Beanstalk / App Runner", 2.4, 1)
    d.icon("stg", "Web_Slots", "Staging slot (warm-up, tests)", "Blue/green environment", 3.8, 1)
    d.group("asp", "App Service Plan = the compute (shared by apps). Standard+ for autoscale and slots", ["prod", "stg"], "blue")
    d.icon("vn", "Virtual_Networks", "VNet (private resources)", "VPC", 3.8, 2.5)
    d.icon("sql", "SQL_Database", "SQL / Storage via Private Endpoint", "RDS / S3", 5.3, 2.5)
    d.edge("cl", "pe", "", "private"); d.edge("pe", "prod", "inbound", "private")
    d.edge("prod", "stg", "swap", "ok", both=True)
    d.edge("prod", "vn", "VNet Integration (outbound)", "data")
    d.edge("vn", "sql", "", "private")
    d.table(0, 3.75, [dict(title="Free / Shared", w=150), dict(title="Basic", w=150), dict(title="Standard", w=190), dict(title="Premium v3", w=150), dict(title="Isolated v2 / ASE", w=230)],
            [("Tier", ["Dev / small", "No autoscale or slots", "★ Autoscale + deployment slots", "More power, zone redundancy", "Full isolation in your VNet"]),
             ("Facts", ["", "Max 30 instances", "~5 slots ⚠ verify", "~20 slots ⚠ verify", "Max 100 instances"])], label_w=80)
    d.note("n1", "Slot settings marked 'sticky' do not move with a swap. A swap with preview warms the target slot before it takes traffic.", 0, 5.0, w=800, dx=140)

    # ---------------------------------------------------------------- 7.4
    d = b.D("7.4", "Functions hosting plans", "D",
            "Same programming model, four hosting plans. Flex Consumption is the recommended serverless choice for new work; Premium removes cold starts; Dedicated reuses a plan you already pay for.",
            [("Function that reaches the VNet", "Flex Consumption or Premium"), ("No cold start", "Premium"), ("Stateful orchestration in code", "Durable Functions (AWS Step Functions)")])
    d.table(0, 0, [
        dict(title="Consumption (classic)", icon="Function_Apps", aws="Lambda", w=210),
        dict(title="Flex Consumption (recommended)", icon="Function_Apps", aws="Lambda", w=210),
        dict(title="Premium", icon="Function_Apps", aws="Lambda provisioned concurrency", w=210),
        dict(title="Dedicated", icon="App_Service_Plans", aws="-", w=210)],
        [("Scale to zero", ["✓ Yes", "✓ Yes", "✗ Pre-warmed instances always on", "✗ Uses your App Service Plan"]),
         ("Cold start", ["⚠ Yes", "★ Reduced (optional always-ready instances)", "✓ None", "None if Always On"]),
         ("Timeout", ["5 min default, 10 min max", "★ Unlimited", "Long", "Long"]),
         ("VNet access", ["✗ No", "✓ Yes", "✓ Yes", "✓ Yes"]),
         ("Billing", ["Per execution", "Per execution, with optional always-ready", "Per instance", "The plan you already pay"])],
        label_w=110)
    d.icon("df", "Function_Apps", "Durable Functions", "Step Functions", 0.2, 4.4)
    d.note("n1", "Durable Functions: stateful orchestrations written in code (retries, fan-out/fan-in). About 200 instances max per function app.", 1.0, 4.4, w=520, dx=230, dy=10)

    # ---------------------------------------------------------------- 7.5
    d = b.D("7.5", "AKS reference architecture", "A",
            "Node pools spread across zones, secrets via Workload Identity and Key Vault, images from ACR over Private Link, telemetry to Log Analytics. Scale with HPA, cluster autoscaler and KEDA; use virtual nodes (ACI) for bursts.",
            [("Pods access Azure without secrets", "Workload Identity"), ("K8s control, operators, CRDs", "AKS"), ("Without managing Kubernetes", "Container Apps"),
             ("HA for node pools", "spread across availability zones"), ("L7 ingress for AKS", "AGIC / Application Gateway for Containers")])
    d.box("usr", "Users", -0.1, 1.1, w=90, color="gray")
    d.icon("agw", "Application_Gateway_Containers", "App Gateway (AGIC / for Containers)", "ALB + LB Controller", 0.9, 1.1)
    d.box("sys", "System node pool", 2.5, 0.0, w=190, color="blue")
    d.box("usrp", "User node pools spread over zones 1-3", 2.5, 1.1, w=190, color="blue")
    d.box("spotp", "Spot node pool (interruptible)", 2.5, 2.2, w=190, color="gray")
    d.icon("vn", "Container_Instances", "Virtual nodes (ACI) for bursts", "Fargate burst", 3.8, 2.2)
    d.group("aks", "AKS cluster  (AWS: EKS)  - Azure CNI or kubenet", ["sys", "usrp", "spotp", "vn"], "purple")
    d.icon("acr", "Container_Registries", "Container Registry (Premium: geo-replication, Private Link)", "ECR", 5.4, 0)
    d.icon("kv", "Key_Vaults", "Key Vault (CSI driver)", "Secrets Manager", 5.4, 1.1)
    d.icon("mi", "Entra_Managed_Identities", "Workload Identity (Entra)", "IRSA", 5.4, 2.2)
    d.icon("law", "Log_Analytics_Workspaces", "Container Insights + Log Analytics", "CloudWatch Container Insights", 6.7, 0.5)
    d.icon("dfc", "Azure_Defender", "Defender for Containers", "GuardDuty EKS + ECR scanning", 6.7, 1.7)
    d.group("ops", "Observe and protect", ["law", "dfc"], "gray")
    d.edge("usr", "agw"); d.edge("agw", "usrp", "ingress")
    d.edge("acr", "usrp", "pull image", "ctrl"); d.edge("usrp", "kv", "secrets", "ctrl"); d.edge("mi", "kv", "no secrets", "ok")
    d.note("n1", "Control plane is free in the Free tier; the Standard tier adds an SLA. Azure Policy for Kubernetes and Entra authentication harden the cluster. Autoscaling: HPA, cluster autoscaler, KEDA.", 0, 3.5, w=900, dx=240)

    # ---------------------------------------------------------------- 7.6
    d = b.D("7.6", "Container Apps: serverless containers", "A",
            "Container Apps runs containers without exposing Kubernetes. KEDA scales on HTTP or events (down to zero), revisions allow canary traffic splitting, Dapr gives service-to-service building blocks.",
            [("Containers, scale to zero, no K8s", "Container Apps"), ("Percentage of traffic to a new version", "revisions + traffic splitting"), ("Event-driven scaling", "KEDA")])
    d.icon("src", "Service_Bus", "Event sources: HTTP, Service Bus, Event Hubs", "SQS / Kinesis", 0, 1)
    d.icon("keda", "Container_App_Environments", "KEDA scaler (0 to N)", "-", 1.4, 1, tag="scales to zero")
    d.icon("r1", "Worker_Container_App", "Revision 1 (80% traffic)", "Fargate service", 2.9, 0.2)
    d.icon("r2", "Worker_Container_App", "Revision 2 (20% canary)", "Fargate service", 2.9, 1.8)
    d.icon("dapr", "Container_Instances", "Dapr sidecar", "App Mesh (approx.)", 4.4, 1)
    d.group("env", "Container Apps environment  (AWS: App Runner / ECS Fargate)", ["keda", "r1", "r2", "dapr"], "purple")
    d.icon("acr", "Container_Registries", "Container Registry", "ECR", 6.1, 1)
    d.edge("src", "keda", "events"); d.edge("keda", "r1"); d.edge("keda", "r2"); d.edge("r1", "dapr", "", "ctrl"); d.edge("r2", "dapr", "", "ctrl"); d.edge("acr", "r1", "pull image", "ctrl")

    # ---------------------------------------------------------------- 7.7
    d = b.D("7.7", "Batch, HPC and specialised compute", "A",
            "Azure Batch runs parallel work on pools of VMs (Spot to save money). The service itself has no extra cost. CycleCloud covers classic HPC clusters; Service Fabric and ARO are niche.",
            [("Thousands of cheap batch tasks", "Batch + Spot"), ("Classic HPC clusters (Slurm, PBS)", "CycleCloud"), ("Managed OpenShift", "Azure Red Hat OpenShift (AWS ROSA)")])
    d.icon("in", "Storage_Accounts", "Input data (Blob)", "S3", 0, 1)
    d.icon("batch", "Batch_Accounts", "Batch account: jobs + tasks", "AWS Batch", 1.5, 1)
    d.icon("pool", "VM_Scale_Sets", "Pool: dedicated + Spot VMs", "Spot Fleet", 3.0, 1)
    d.icon("out", "Storage_Accounts", "Results (Blob)", "S3", 4.5, 1)
    d.chain(["in", "batch", "pool", "out"])
    d.icon("cc", "Azure_HPC_Workbench", "CycleCloud (classic HPC clusters)", "ParallelCluster (approx.)", 1.5, 2.6)
    d.icon("sf", "Service_Fabric_Clusters", "Service Fabric (stateful microservices; de facto retiring)", "-", 3.0, 2.6)
    d.icon("aro", "Azure_Red_Hat_OpenShift", "Azure Red Hat OpenShift", "ROSA", 4.5, 2.6)

    # ---------------------------------------------------------------- 7.8
    d = b.D("7.8", "Azure Virtual Desktop", "A",
            "Multi-session Windows desktops on host pools. User profiles roam with FSLogix on Azure Files or NetApp Files; Entra ID and Conditional Access control sign-in; autoscale starts and stops hosts.",
            [("Windows multi-session desktops", "Azure Virtual Desktop"), ("User profiles for pooled hosts", "FSLogix on Azure Files / NetApp Files")])
    d.box("usr", "Remote users", -0.1, 1, w=110, color="gray")
    d.icon("ca", "Conditional_Access", "Entra ID + Conditional Access", "IAM Identity Center", 1.1, 1)
    d.icon("avd", "Windows_Virtual_Desktop", "AVD control plane (host pools, app groups)", "WorkSpaces / AppStream", 2.5, 1)
    d.icon("hp", "Host_Pools", "Session hosts (multi-session, autoscale)", "WorkSpaces pool", 4.0, 1)
    d.icon("fs", "Storage_Azure_Files", "FSLogix profiles on Azure Files / NetApp Files", "FSx for Windows / EFS", 5.5, 1)
    d.chain(["usr", "ca", "avd", "hp", "fs"], ["sign in", "", "", "profile"])
    return b
