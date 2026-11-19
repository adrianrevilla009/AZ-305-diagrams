# Azure AZ-305 diagrams (with AWS equivalents)

96 draw.io diagrams in 18 files, one tab per diagram. Tab 0 of each file is a legend. Built to map Azure services to AWS for someone coming from SAP-C02.

## Use
Open any `diagrams/*.drawio` in https://app.diagrams.net (or the desktop app). Icons are draw.io's built-in Azure set (`img/lib/azure2/...`), resolved by draw.io itself; no Microsoft artwork is bundled here.

Kinds: **A** architecture, **D** decision table, **C** concept. `⚠ verify` marks facts the study notes flagged as uncertain; `+ added` marks services not in the notes. Check limits and prices against Microsoft Learn before the exam.

## Rebuild
```
python3 -I build.py            # all files, also writes diagrams/_index.json
python3 -I build.py s04 s08    # selected sections
python3 -I tools/render.py WEBAPP_DIR FILE.drawio OUT_DIR [page...]   # PNG preview via the draw.io viewer
```
Sections live in `src/sections/`, the generator DSL in `src/azdiag/`.

## Index
| File | ID | Diagram | Kind |
|---|---|---|---|
| `01-identity-access.drawio` | 1.1 | Hybrid authentication and sync: which one? | Decision |
| `01-identity-access.drawio` | 1.2 | Hybrid identity architecture | Architecture |
| `01-identity-access.drawio` | 1.3 | External identities: partners and customers | Architecture |
| `01-identity-access.drawio` | 1.4 | Secretless access: managed identity, service principal, federation | Architecture |
| `01-identity-access.drawio` | 1.5 | Legacy and private apps | Architecture |
| `01-identity-access.drawio` | 1.6 | Azure RBAC: scope, inheritance and roles | Architecture |
| `02-governance.drawio` | 2.1 | Landing zone and management group hierarchy | Architecture |
| `02-governance.drawio` | 2.2 | Azure Policy: effects and evaluation order | Decision |
| `02-governance.drawio` | 2.3 | Entra ID Governance | Architecture |
| `02-governance.drawio` | 2.4 | Multi-tenant and hybrid management: Lighthouse and Arc | Architecture |
| `02-governance.drawio` | 2.5 | Boundaries: what isolates what | Concept |
| `03-encryption-keys.drawio` | 3.1 | Key Vault design | Architecture |
| `03-encryption-keys.drawio` | 3.2 | Which key store? Key Vault, Managed HSM, Cloud HSM... | Decision |
| `03-encryption-keys.drawio` | 3.3 | Encryption map: at rest, in transit, in use | Concept |
| `04-networking.drawio` | 4.1 | Hub-and-spoke network | Architecture |
| `04-networking.drawio` | 4.2 | Virtual WAN | Architecture |
| `04-networking.drawio` | 4.3 | Hub-spoke vs Virtual WAN | Decision |
| `04-networking.drawio` | 4.4 | Hybrid connectivity: VPN and ExpressRoute | Architecture |
| `04-networking.drawio` | 4.5 | Private access to PaaS: Private Endpoint vs Service Endpoint | Architecture |
| `04-networking.drawio` | 4.6 | Network security stack | Architecture |
| `04-networking.drawio` | 4.7 | Hybrid DNS and name resolution | Architecture |
| `04-networking.drawio` | 4.8 | Azure Virtual Network Manager and Route Server (added) | Architecture |
| `05-lb-cdn-apis.drawio` | 5.1 | Load-balancing decision map | Decision |
| `05-lb-cdn-apis.drawio` | 5.2 | Layered web front end | Architecture |
| `05-lb-cdn-apis.drawio` | 5.3 | API Management: tiers and placement | Architecture |
| `06-storage.drawio` | 6.1 | Redundancy ladder: LRS to RA-GZRS | Decision |
| `06-storage.drawio` | 6.2 | Blob tiers, lifecycle and data protection | Architecture |
| `06-storage.drawio` | 6.3 | Securing access to a storage account | Architecture |
| `06-storage.drawio` | 6.4 | File and block services: which one? | Decision |
| `06-storage.drawio` | 6.5 | Managed disks: performance ladder | Decision |
| `06-storage.drawio` | 6.6 | Data Lake Storage Gen2 and the other storage services | Architecture |
| `07-compute.drawio` | 7.1 | Compute decision map | Decision |
| `07-compute.drawio` | 7.2 | Highly available VMs | Architecture |
| `07-compute.drawio` | 7.3 | App Service: plans, slots and networking | Architecture |
| `07-compute.drawio` | 7.4 | Functions hosting plans | Decision |
| `07-compute.drawio` | 7.5 | AKS reference architecture | Architecture |
| `07-compute.drawio` | 7.6 | Container Apps: serverless containers | Architecture |
| `07-compute.drawio` | 7.7 | Batch, HPC and specialised compute | Architecture |
| `07-compute.drawio` | 7.8 | Azure Virtual Desktop | Architecture |
| `08-databases.drawio` | 8.1 | Azure SQL options: which one? | Decision |
| `08-databases.drawio` | 8.2 | SQL Database purchase and service tiers | Decision |
| `08-databases.drawio` | 8.3 | SQL HA and DR | Architecture |
| `08-databases.drawio` | 8.4 | Cosmos DB: global distribution | Architecture |
| `08-databases.drawio` | 8.5 | Cosmos DB consistency ladder | Decision |
| `08-databases.drawio` | 8.6 | PostgreSQL and MySQL Flexible Server | Architecture |
| `08-databases.drawio` | 8.7 | Azure Managed Redis | Architecture |
| `09-messaging-integration.drawio` | 9.1 | Message vs event: which service? | Decision |
| `09-messaging-integration.drawio` | 9.2 | Service Bus: queues, topics and tiers | Architecture |
| `09-messaging-integration.drawio` | 9.3 | Event Hubs: partitions, consumer groups, Capture | Architecture |
| `09-messaging-integration.drawio` | 9.4 | Event-driven and telemetry pipelines | Architecture |
| `09-messaging-integration.drawio` | 9.5 | IoT: IoT Hub, DPS, IoT Central | Architecture |
| `09-messaging-integration.drawio` | 9.6 | Real-time web, push and low-code | Architecture |
| `09-messaging-integration.drawio` | 9.7 | Orchestration: which tool? | Decision |
| `10-analytics.drawio` | 10.1 | Analytics engines: which one? | Decision |
| `10-analytics.drawio` | 10.2 | Medallion data platform | Architecture |
| `10-analytics.drawio` | 10.3 | Data Factory integration runtimes | Decision |
| `10-analytics.drawio` | 10.4 | Streaming: hot, warm and cold paths | Architecture |
| `10-analytics.drawio` | 10.5 | Microsoft Purview | Architecture |
| `10-analytics.drawio` | 10.6 | Fabric concepts | Architecture |
| `11-migration.drawio` | 11.1 | Cloud Adoption Framework and the migration Rs | Concept |
| `11-migration.drawio` | 11.2 | Azure Migrate: server migration | Architecture |
| `11-migration.drawio` | 11.3 | Database migration paths | Architecture |
| `11-migration.drawio` | 11.4 | Data transfer: online or offline? | Decision |
| `12-continuity.drawio` | 12.1 | The four DR strategies | Decision |
| `12-continuity.drawio` | 12.2 | Azure Site Recovery | Architecture |
| `12-continuity.drawio` | 12.3 | Azure Backup | Architecture |
| `12-continuity.drawio` | 12.4 | Multi-region active-active | Architecture |
| `12-continuity.drawio` | 12.5 | HA building blocks cheat sheet | Decision |
| `12-continuity.drawio` | 12.6 | Composite SLA math | Decision |
| `13-security.drawio` | 13.1 | Defender for Cloud: CSPM vs CWPP | Architecture |
| `13-security.drawio` | 13.2 | Defender plan map | Decision |
| `13-security.drawio` | 13.3 | Microsoft Sentinel | Architecture |
| `13-security.drawio` | 13.4 | Defense in depth and compliance tools | Decision |
| `14-observability-ops.drawio` | 14.1 | Azure Monitor data flow | Architecture |
| `14-observability-ops.drawio` | 14.2 | Alerts and action groups | Architecture |
| `14-observability-ops.drawio` | 14.3 | Log Analytics workspace design | Architecture |
| `14-observability-ops.drawio` | 14.4 | Application, container and VM insights | Architecture |
| `14-observability-ops.drawio` | 14.5 | Diagnostics: who did what, what's broken, where is it | Decision |
| `14-observability-ops.drawio` | 14.6 | Operations automation | Decision |
| `15-devops.drawio` | 15.1 | IaC decision | Decision |
| `15-devops.drawio` | 15.2 | CI/CD with OIDC | Architecture |
| `15-devops.drawio` | 15.3 | Deployment strategies | Decision |
| `15-devops.drawio` | 15.4 | App Configuration and feature flags | Architecture |
| `15-devops.drawio` | 15.5 | Chaos Studio and Load Testing | Architecture |
| `16-finops.drawio` | 16.1 | Cost governance pattern | Architecture |
| `16-finops.drawio` | 16.2 | Purchase options and per-service levers | Decision |
| `17-ai.drawio` | 17.1 | AI service decision | Decision |
| `17-ai.drawio` | 17.2 | RAG architecture | Architecture |
| `17-ai.drawio` | 17.3 | OpenAI deployment types | Decision |
| `17-ai.drawio` | 17.4 | AI gateway with API Management | Architecture |
| `17-ai.drawio` | 17.5 | Azure ML MLOps | Architecture |
| `18-extras.drawio` | 18.1 | Well-Architected pillars | Decision |
| `18-extras.drawio` | 18.2 | Cloud design patterns | Decision |
| `18-extras.drawio` | 18.3 | Azure Local and hybrid | Architecture |
| `18-extras.drawio` | 18.4 | Regions, zones and sovereign clouds | Decision |
| `18-extras.drawio` | 18.5 | Static Web Apps | Architecture |
