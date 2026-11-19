from azdiag import Book

DOM = "Identity, governance and monitoring (25-30%)"


def build():
    b = Book("03-encryption-keys.drawio", "Encryption, keys and secrets", DOM)

    # ---------------------------------------------------------------- 3.1
    d = b.D("3.1", "Key Vault design", "A",
            "One vault for keys, secrets and certificates. Authorise with Azure RBAC (not access policies), keep soft delete and purge protection on, reach it through a Private Endpoint and use managed identities instead of secrets.",
            [("Prevent permanent deletion", "purge protection"), ("HSM-protected keys without managing hardware", "Key Vault Premium"),
             ("Customer-managed keys (CMK)", "purge protection is mandatory")])
    d.icon("app", "App_Services", "App with managed identity", "Elastic Beanstalk / App Runner", 0, 1)
    d.icon("pe", "Private_Endpoint", "Private Endpoint + firewall", "VPC endpoint for KMS", 1.5, 1)
    d.box("k1", "Keys (Standard: software FIPS 140-2 L1; Premium: HSM FIPS 140-3 L3)", 3.2, 0, w=300, color="purple")
    d.box("k2", "Secrets", 3.2, 0.7, w=300, color="purple")
    d.box("k3", "Certificates (integrated CAs: DigiCert, GlobalSign, or imported)", 3.2, 1.4, w=300, color="purple")
    d.group("kv", "Key Vault  (AWS: KMS + Secrets Manager + ACM)", ["k1", "k2", "k3"], "purple")
    d.icon("eg", "Event_Grid_Topics", "Event Grid: expiry and rotation events", "EventBridge", 5.0, 1)
    d.chain(["app", "pe"], ["RBAC token"]); d.edge("pe", "k2", "", "private")
    d.edge("k3", "eg", "notify", "async")
    d.table(0, 3.3, [dict(title="Soft delete", w=360), dict(title="Purge protection", w=420)],
            [("Behaviour", ["Always on. Retention 7 to 90 days (default 90), set when the vault is created", "Optional and irreversible once enabled. Blocks permanent deletion during the retention, even for admins. Mandatory for CMK"]),
             ("Other", ["Authorisation: Azure RBAC (recommended, e.g. Key Vault Secrets User, Crypto Officer) or access policies (legacy); one model per vault",
                        "Automatic key rotation. App Service Managed Certificates and Front Door managed certificates give free TLS (AWS ACM). No PKCS#11/JCE/CNG; Key Vault has throttling"])],
            label_w=90)

    # ---------------------------------------------------------------- 3.2
    d = b.D("3.2", "Which key store? Key Vault, Managed HSM, Cloud HSM...", "D",
            "From software-protected keys to dedicated hardware. Choose by tenancy, certification level, API needs (PKCS#11) and whether you need sovereignty or payment-specific HSMs.",
            [("HSM keys without managing hardware", "Key Vault Premium"), ("Single-tenant and sovereignty", "Managed HSM"), ("PKCS#11", "Cloud HSM"),
             ("Card PINs / payments", "Payment HSM"), ("Customer can revoke keys", "CMK")])
    d.table(0, 0, [
        dict(title="Key Vault Standard", icon="Key_Vaults", aws="KMS + Secrets Manager + ACM", w=150),
        dict(title="Key Vault Premium", icon="Key_Vaults", aws="KMS (HSM-backed)", w=150),
        dict(title="Managed HSM", icon="Keys", aws="KMS custom key store / CloudHSM", w=150),
        dict(title="Cloud HSM", icon="Dedicated_HSM", aws="CloudHSM", w=150),
        dict(title="Dedicated HSM", icon="Dedicated_HSM", aws="CloudHSM", w=150),
        dict(title="Payment HSM", icon="Dedicated_HSM", aws="Payment Cryptography", w=150)],
        [("Tenancy", ["Multi-tenant", "Multi-tenant", "★ Single-tenant HSM pool", "Dedicated HSM cluster", "Bare metal", "Bare metal"]),
         ("Certification", ["Software keys, FIPS 140-2 L1", "★ HSM keys, FIPS 140-3 L3", "FIPS 140-3 L3", "FIPS 140-3 L3", "FIPS 140-2 L3", "PCI HSM v3, PCI PIN"]),
         ("Use it when", ["General secrets, keys and certificates", "HSM-protected keys without managing hardware", "Exclusive key control, sovereignty, BYOK/HYOK. Dedicated capacity with no Key Vault throttling",
                          "Migrating apps that already use an on-prem HSM (PKCS#11, JCE, CNG)", "⚠ Being retired in favour of Cloud HSM", "PIN and payment processing"])],
        label_w=100)

    # ---------------------------------------------------------------- 3.3
    d = b.D("3.3", "Encryption map: at rest, in transit, in use", "C",
            "Default encryption needs nothing from you. Add customer-managed keys when you need control or revocation, Always Encrypted when even the DBA must not see data, confidential computing for data in use.",
            [("Customer revokes the keys", "CMK"), ("Not even the DBA sees the data", "Always Encrypted"), ("Encrypted while being processed", "confidential computing"),
             ("Prevent permanent deletion", "purge protection"), ("Regulatory double encryption", "infrastructure encryption (Storage)")])
    d.table(0, 0, [dict(title="Azure feature", w=420), dict(title="AWS", w=250), dict(title="Notes", w=330)],
            [("At rest (default)", ["Storage, SQL and Cosmos DB encrypt with Microsoft-managed keys", "-", "Nothing to configure"]),
             ("At rest with your keys (CMK)", ["Key lives in your Key Vault or Managed HSM; you rotate and can revoke it", "SSE-KMS with CMK", "Purge protection is mandatory"]),
             ("VM disks", ["SSE + CMK via Disk Encryption Set. Encryption at host also covers cache and temp disk", "-", "Azure Disk Encryption (BitLocker / DM-Crypt) is the older option"]),
             ("SQL", ["TDE (default). Always Encrypted: client-side, server never sees clear data. Dynamic Data Masking", "-", "Always Encrypted: not even the DBA"]),
             ("In transit", ["TLS 1.2+, IPsec on VPN, MACsec on ExpressRoute Direct", "-", ""]),
             ("Double encryption", ["Infrastructure encryption in Storage", "-", "For regulatory requirements"]),
             ("In use", ["Confidential computing: confidential VMs and containers (AMD SEV-SNP, Intel TDX)", "Nitro Enclaves", "Data encrypted while being processed"])],
            label_w=150)
    return b
