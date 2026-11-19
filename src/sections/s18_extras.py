from azdiag import Book

DOM = "Architecture extras"


def build():
    b = Book("18-extras.drawio", "Extras", DOM)

    d = b.D("18.1", "Well-Architected pillars", "D",
            "Five pillars guide trade-offs.",
            [("Security", "least privilege"), ("Reliability", "redundancy")])
    d.table(0, 0, [dict(title=t, icon="Advisor", w=140) for t in ["Reliability", "Security", "Cost Optimization", "Operational Excellence", "Performance Efficiency"]],
            [("Focus", ["Resilience and recovery", "Protect data and systems", "Maximize value", "Run and monitor well", "Scale to demand"])], label_w=70)

    d = b.D("18.2", "Cloud design patterns", "D",
            "Common patterns map to problems.",
            [("Decouple", "queue-based load leveling"), ("Protect backends", "circuit breaker")])
    d.table(0, 0, [dict(title="Pattern", w=200), dict(title="Solves", w=400)],
            [("Circuit breaker", ["Stops calls to a failing dependency"]), ("Queue-based load leveling", ["Smooths bursts"]),
             ("CQRS", ["Separates reads and writes"]), ("Strangler fig", ["Incremental migration"]), ("Claim check", ["Large messages by reference"])], label_w=90)

    d = b.D("18.3", "Azure Local and hybrid", "A",
            "Run Azure services on-premises with Azure Local, managed through Arc.",
            [("On-prem with Azure management", "Azure Local + Arc")])
    d.icon("l", "Azure_Local", "Azure Local", "Outposts", 0, 0.4)
    d.icon("a", "Azure_Arc", "Azure Arc", "Systems Manager hybrid", 1.8, 0.4)
    d.icon("c", "Management_Groups", "Azure control plane", None, 3.6, 0.4)
    d.edge("l", "a", "connect", "ctrl"); d.edge("a", "c", "manage", "ctrl")

    d = b.D("18.4", "Regions, zones and sovereign clouds", "D",
            "Regions contain zones; paired regions help DR; sovereign clouds serve regulated needs.",
            [("Data residency", "region choice")])
    d.table(0, 0, [dict(title="Region", w=170), dict(title="Availability zone", w=170), dict(title="Sovereign cloud", w=170)],
            [("Meaning", ["Geography with datacenters", "Isolated datacenter in a region", "Separate Azure for government or China"])], label_w=90)

    d = b.D("18.5", "Static Web Apps", "A",
            "Static front end with integrated serverless API and global CDN.",
            [("Static site + API", "Static Web Apps")])
    d.icon("r", "Subscriptions", "Git repo", "CodeCommit", 0, 0.4)
    d.icon("s", "Static_Apps", "Static Web Apps", "Amplify Hosting", 1.8, 0.4)
    d.icon("f", "Function_Apps", "Functions API", "Lambda", 3.6, 0.4)
    d.edge("r", "s", "deploy", "data"); d.edge("s", "f", "/api", "data")
    return b
