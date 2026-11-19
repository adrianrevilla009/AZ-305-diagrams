from azdiag import Book

DOM = "Infrastructure and DevOps"


def build():
    b = Book("15-devops.drawio", "DevOps and IaC", DOM)

    d = b.D("15.1", "IaC decision", "D",
            "Bicep is the Azure-native choice, ARM is the underlying JSON, Terraform for multicloud.",
            [("Azure-native IaC", "Bicep"), ("Multicloud IaC", "Terraform")])
    d.table(0, 0, [dict(title="Bicep", icon="Template_Specs", aws="CloudFormation / CDK", w=170), dict(title="ARM templates", icon="Template_Specs", aws="CloudFormation", w=170),
                   dict(title="Terraform", icon="Template_Specs", w=170)],
            [("Pick it when", ["★ Azure-only, day-0 support", "Existing JSON templates", "★ Multicloud or existing Terraform"])], label_w=100)

    d = b.D("15.2", "CI/CD with OIDC", "A",
            "Pipelines authenticate to Azure with workload identity federation (OIDC), so no secrets are stored.",
            [("No stored secrets", "OIDC federation")])
    d.icon("gh", "Azure_DevOps", "GitHub Actions / Azure Pipelines", "CodePipeline", 0, 0.4)
    d.icon("id", "Azure_Active_Directory", "Entra app + federated credential", "IAM OIDC role", 1.8, 0.4)
    d.icon("az", "Subscriptions", "Azure subscription", None, 3.6, 0.4)
    d.edge("gh", "id", "OIDC token", "ctrl"); d.edge("id", "az", "RBAC deploy", "data")

    d = b.D("15.3", "Deployment strategies", "D",
            "Blue/green swaps slots, canary shifts a percentage, rolling updates in batches.",
            [("Zero-downtime swap", "deployment slots")])
    d.table(0, 0, [dict(title="Blue/green", icon="App_Services", w=170), dict(title="Canary", icon="App_Services", w=170), dict(title="Rolling", icon="App_Services", w=170)],
            [("How", ["Deploy to staging slot, swap", "Route small % of traffic", "Update instances in batches"]), ("Rollback", ["★ Swap back", "Shift traffic back", "Halt and redeploy"])], label_w=90)

    d = b.D("15.4", "App Configuration and feature flags", "A",
            "Central configuration and feature flags with Key Vault references.",
            [("Feature flags", "App Configuration")])
    d.icon("app", "App_Services", "App", None, 0, 0.4)
    d.icon("ac", "App_Configuration", "App Configuration", "Parameter Store / AppConfig", 1.8, 0.4)
    d.icon("kv", "Key_Vaults", "Key Vault (secrets)", "Secrets Manager", 3.6, 0.4)
    d.edge("app", "ac", "read", "data"); d.edge("ac", "kv", "reference", "ctrl")

    d = b.D("15.5", "Chaos Studio and Load Testing", "A",
            "Validate resilience with fault injection and performance with load tests before production.",
            [("Fault injection", "Chaos Studio"), ("Load tests", "Azure Load Testing")])
    d.icon("ch", "Azure_Chaos_Studio", "Chaos Studio", "Fault Injection Service", 0, 0.4)
    d.icon("t", "App_Services", "Target workload", None, 1.8, 0.4)
    d.icon("lt", "Azure_Load_Testing", "Azure Load Testing", "Distributed Load Testing", 3.6, 0.4)
    d.edge("ch", "t", "faults", "bad"); d.edge("lt", "t", "load", "data", src="l", dst="r")
    return b
