from azdiag import Book

DOM = "Cost management"


def build():
    b = Book("16-finops.drawio", "FinOps", DOM)

    d = b.D("16.1", "Cost governance pattern", "A",
            "Tag resources, set budgets with alerts, review Advisor recommendations, and enforce with Policy.",
            [("Alert on spend", "budgets"), ("Enforce tags", "Azure Policy"), ("Right-size", "Advisor")])
    d.icon("tag", "Subscriptions", "Tags + management groups", "Organizations + tag policies", 0, 0.4)
    d.icon("cm", "Cost_Management", "Cost Management", "Cost Explorer", 1.8, 0.4)
    d.icon("bu", "Cost_Budgets", "Budgets + alerts", "AWS Budgets", 3.6, 0.4)
    d.icon("ad", "Advisor", "Advisor", "Trusted Advisor / Compute Optimizer", 5.4, 0.4)
    d.chain(["tag", "cm", "bu", "ad"], ["group", "alert", "optimize"])

    d = b.D("16.2", "Purchase options and per-service levers", "D",
            "Commit for steady load, use spot for interruptible work, reuse licences with Hybrid Benefit.",
            [("Steady 1-3 year usage", "Reservations / Savings Plan"), ("Interruptible", "Spot"), ("Existing licences", "Hybrid Benefit")])
    d.table(0, 0, [dict(title="Reservations", icon="Reservations", aws="Reserved Instances", w=170), dict(title="Savings Plan", icon="Reservations", aws="Savings Plans", w=170),
                   dict(title="Spot VMs", icon="Virtual_Machine", aws="Spot Instances", w=170), dict(title="Hybrid Benefit", icon="Virtual_Machine", w=170)],
            [("Best for", ["Specific resource, 1 or 3 years", "Flexible compute spend commitment", "★ Batch, stateless, interruptible", "★ Windows Server / SQL licences with SA"])], label_w=90)
    return b
