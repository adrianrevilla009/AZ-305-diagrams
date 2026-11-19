from azdiag import Book

DOM = "AI and ML"


def build():
    b = Book("17-ai.drawio", "AI", DOM)

    d = b.D("17.1", "AI service decision", "D",
            "Prebuilt AI services for common tasks, Azure OpenAI for generative, Azure ML for custom models.",
            [("Generative AI", "Azure OpenAI / Foundry"), ("Custom model training", "Azure Machine Learning"), ("OCR/forms", "Document Intelligence")])
    d.table(0, 0, [dict(title="AI services", icon="Cognitive_Services", aws="Rekognition / Textract / Comprehend", w=170), dict(title="Azure OpenAI", icon="Azure_OpenAI", aws="Bedrock", w=170),
                   dict(title="Azure ML", icon="Machine_Learning", aws="SageMaker", w=170), dict(title="Foundry", icon="AI_Foundry", aws="Bedrock + SageMaker Studio", w=170)],
            [("Pick it when", ["★ Prebuilt vision, speech, language, forms", "★ GPT-type generation, embeddings", "★ Train, deploy, MLOps custom models", "Build and manage AI apps and agents"])], label_w=90)

    d = b.D("17.2", "RAG architecture", "A",
            "Retrieve relevant chunks from a search index, then ground the model's answer in them.",
            [("Grounded answers", "RAG"), ("Vector + keyword search", "AI Search")])
    d.icon("u", "Virtual_Machine", "User / app", None, 0, 0.4)
    d.icon("s", "Cognitive_Services", "AI Search (vector + keyword)", "OpenSearch / Kendra", 1.8, 0)
    d.icon("o", "Azure_OpenAI", "Azure OpenAI", "Bedrock", 1.8, 1.9)
    d.icon("st", "Storage_Accounts", "Documents (Blob)", "S3", 3.6, 0)
    d.edge("u", "s", "1. query", "data"); d.edge("s", "o", "2. context", "data"); d.edge("st", "s", "index", "async")

    d = b.D("17.3", "OpenAI deployment types", "D",
            "Standard is pay per token, Provisioned reserves throughput, Batch is cheap and asynchronous; regional or global variants.",
            [("Predictable latency", "Provisioned"), ("Offline bulk", "Batch")])
    d.table(0, 0, [dict(title="Standard", icon="Azure_OpenAI", w=170), dict(title="Provisioned (PTU)", icon="Azure_OpenAI", w=170), dict(title="Batch", icon="Azure_OpenAI", w=170)],
            [("Billing", ["Pay per token", "Reserved throughput units", "Discounted, 24h turnaround"]), ("Pick it when", ["Variable, general", "★ Predictable latency and volume", "★ Bulk, non-urgent"])], label_w=90)

    d = b.D("17.4", "AI gateway with API Management", "A",
            "APIM fronts model endpoints for auth, token limits, load balancing and logging.",
            [("Token limits and load balancing", "APIM AI gateway")])
    d.icon("c", "Virtual_Machine", "Clients", None, 0, 0.4)
    d.icon("g", "API_Management_Services", "APIM AI gateway", "API Gateway", 1.8, 0.4)
    d.icon("o", "Azure_OpenAI", "Azure OpenAI (multiple)", "Bedrock", 3.6, 0.4)
    d.edge("c", "g", "call", "data"); d.edge("g", "o", "balance + limit", "data")

    d = b.D("17.5", "Azure ML MLOps", "A",
            "Train in a workspace, register the model, deploy to managed online endpoints, monitor and retrain.",
            [("Managed endpoint", "online endpoint")])
    d.icon("d", "Storage_Accounts", "Data", "S3", 0, 0.4)
    d.icon("t", "Machine_Learning", "Training job", "SageMaker Training", 1.6, 0.4)
    d.icon("r", "Machine_Learning", "Model registry", "SageMaker Model Registry", 3.2, 0.4)
    d.icon("e", "Machine_Learning", "Managed online endpoint", "SageMaker Endpoint", 4.8, 0.4)
    d.chain(["d", "t", "r", "e"], ["train", "register", "deploy"])
    return b
