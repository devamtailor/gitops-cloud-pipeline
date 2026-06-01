# GitOps & Multi-Tool Cloud Orchestration Pipeline

Welcome to the **GitOps & Multi-Tool Cloud Orchestration Pipeline** repository. This project demonstrates enterprise-level infrastructure-as-code (IaC), automated configuration management, and GitOps practices to deploy a highly secure AWS infrastructure running a custom-configured Nginx web server.

---

## 🏗️ Architecture Overview

The system implements a classic **GitOps pipeline** dividing responsibilities between **Terraform** (declarative infrastructure provisioning) and **Ansible** (procedural configuration management).

```text
                  +-----------------------+
                  |  Local Workstation    |
                  +-----------+-----------+
                              | git push
                              v
                  +-----------+-----------+
                  |   GitHub Repository   |
                  +-----------+-----------+
                              | triggers GHA
                              v
    ================== GitHub Actions Runner ==================
   |                                                           |
   |   +-------------------+       +-----------------------+   |
   |   |  Terraform Init   |       |  Ansible Playbook     |   |
   |   |  Terraform Apply  |=====> |  Configures Nginx     |   |
   |   +---------+---------+       +-----------+-----------+   |
   |             |                             |               |
    =============|=============================|===============
                 | provisions                  | configures
                 v                             v
   +-------------+-------------+       +-------+---------------+
   | AWS VPC & Security Groups |=====> | Ubuntu EC2 Web Server |
   +---------------------------+       +-----------------------+
```

### Flow Detail
1. **Infrastructure Provisioning**: Terraform connects to AWS to provision a Virtual Private Cloud (VPC), Public Subnet, Route Table, Internet Gateway, Security Group (restricting SSH access and allowing HTTP access), and an Ubuntu EC2 instance.
2. **Configuration Management**: Once the EC2 instance is active, Ansible updates the operating system, installs Nginx, configures system directories, and deploys a beautifully styled landing portal displaying deployment details.
3. **CI/CD Automation (GitOps)**: A GitHub Actions workflow automates the entire process on every merge/push to the `main` branch.

---

## 📂 Repository Structure

```
gitops-cloud-pipeline/
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions continuous deployment workflow
├── terraform/
│   ├── main.tf               # Terraform core resource declarations
│   ├── variables.tf          # Terraform input variables
│   └── outputs.tf            # Output outputs (Public IP, DNS, VPC ID)
├── ansible/
│   ├── playbook.yml          # Ansible tasks for OS patching and web deployment
│   └── inventory.ini         # Target inventory variables template
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started (Local Deployment)

If you prefer to run the orchestration manually from your local command line, follow the steps below.

### Prerequisites
* [Terraform CLI](https://developer.hashicorp.com/terraform/downloads) (>= 1.0.0)
* [Ansible CLI](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* AWS Credentials configured (`aws configure`)
* SSH Keypair created in AWS (default name: `gitops-deployer-key`)

### Step 1: Provision Infrastructure with Terraform
Navigate to the `terraform/` directory:
```bash
cd terraform
```

Initialize, validate, and preview changes:
```bash
terraform init
terraform validate
terraform plan
```

Apply the configuration:
```bash
terraform apply -auto-approve
```
*Note the output `instance_public_ip`.*

### Step 2: Configure the Target Host using Ansible
Navigate to the `ansible/` directory:
```bash
cd ../ansible
```

Update [inventory.ini](file:///C:/Users/HP/.gemini/antigravity-ide/scratch/gitops-cloud-pipeline/ansible/inventory.ini) by replacing the placeholder `nginx_server ansible_host=127.0.0.1` with the public IP from Terraform:
```ini
nginx_server ansible_host=<YOUR_EC2_PUBLIC_IP> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/gitops-deployer-key.pem
```

Execute the Ansible Playbook:
```bash
ansible-playbook -i inventory.ini playbook.yml
```

Once completed, open your browser and navigate to `http://<YOUR_EC2_PUBLIC_IP>` to see the interactive GitOps portal!

---

## 🔧 Automated GitOps with GitHub Actions

To implement the fully automated pipeline:

1. Create a private or public GitHub repository.
2. In your repository settings, navigate to **Secrets and Variables > Actions** and add the following secrets:
   * `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
   * `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
   * `SSH_PRIVATE_KEY`: The contents of your SSH private key (`.pem`) matching the AWS key pair.
3. Push this repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit of infrastructure and configuration code"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```
4. GitHub Actions will trigger automatically, provision your server, and run the configuration playbook.

---

## 🔒 Security Best Practices Implemented
* **VPC Isolation**: The infrastructure is contained in its own isolated AWS VPC.
* **Strict Security Group**: SSH inbound traffic is restricted by default to a specific CIDR (configurable in `variables.tf`).
* **Encrypted Storage**: The EC2 instance storage uses `gp3` encrypted EBS volumes to secure data at rest.
* **Least Privilege**: The CI/CD pipelines use parameterized credentials injected via repository secrets.
