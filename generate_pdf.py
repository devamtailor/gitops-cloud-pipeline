import os
import urllib.request
from fpdf import FPDF
from PIL import Image

class PortfolioPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(100, 116, 139) # Slate gray
            self.cell(0, 10, 'GitOps & Multi-Tool Cloud Orchestration Pipeline', border=0, align='L', new_x="RIGHT", new_y="TOP")
            self.cell(0, 10, 'Project Documentation', border=0, align='R', new_x="LMARGIN", new_y="NEXT")
            self.ln(2)
            self.set_draw_color(226, 232, 240) # Light border
            self.set_line_width(0.5)
            self.line(20, 18, 190, 18)
            self.ln(4)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(100, 116, 139)
            # Line above footer
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.5)
            self.line(20, 282, 190, 282)
            # Page number
            self.cell(0, 10, f'Page {self.page_no()} of {{nb}}', border=0, align='C', new_x="RIGHT", new_y="TOP")
            self.set_x(20)
            self.cell(0, 10, 'Project By: Devam Tailor', border=0, align='L', new_x="LMARGIN", new_y="NEXT")

def add_heading_1(pdf, text):
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(15, 23, 42) # Slate 900
    pdf.cell(0, 10, text, border=0, new_x="LMARGIN", new_y="NEXT")
    # Highlight accent bar
    pdf.set_draw_color(99, 102, 241) # Indigo 500
    pdf.set_line_width(1)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 40, pdf.get_y())
    pdf.ln(6)

def add_heading_2(pdf, text):
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 8, text, border=0, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

def add_body_text(pdf, text):
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(71, 85, 105) # Slate 600
    pdf.multi_cell(0, 6, text)
    pdf.ln(4)

def add_bullet_point(pdf, bold_prefix, text):
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(6, 6, "-", border=0, new_x="RIGHT", new_y="TOP")
    pdf.cell(pdf.get_string_width(bold_prefix) + 2, 6, bold_prefix, border=0, new_x="RIGHT", new_y="TOP")
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(71, 85, 105)
    pdf.multi_cell(0, 6, text)
    pdf.ln(2)

def insert_screenshot_dynamic(pdf, img_path, title, max_width=150):
    if not os.path.exists(img_path):
        print(f"Warning: Screenshot {img_path} not found.")
        return
        
    with Image.open(img_path) as img:
        w, h = img.size
        aspect = h / w

    # Calculate remaining vertical space on page (Safe bottom boundary is 265mm to avoid overlapping footer)
    y_current = pdf.get_y()
    available_height = 265 - y_current - 12 # 12mm buffer for title/margins
    
    target_width = max_width
    target_height = target_width * aspect
    
    # If the image height at max_width doesn't fit on the page, dynamically shrink it
    if target_height > available_height:
        target_height = available_height
        target_width = target_height / aspect
        
        # If it shrinks too much (width less than 85mm), push the whole section or image to a new page to maintain readability
        if target_width < 85:
            pdf.add_page()
            target_width = max_width
            target_height = target_width * aspect

    # Center the image horizontally
    x_centered = (210 - target_width) / 2
    
    pdf.set_font('helvetica', 'I', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, f'Figure: {title}', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    y_img = pdf.get_y()
    pdf.image(img_path, x=x_centered, y=y_img, w=target_width)
    
    # Draw border around the image
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.3)
    pdf.rect(x_centered, y_img, target_width, target_height)
    
    pdf.set_y(y_img + target_height + 6)

def main():
    # 1. Download official tech logos (using User-Agent header)
    logos_dir = 'screenshots/logos'
    os.makedirs(logos_dir, exist_ok=True)
    
    logo_urls = {
        'aws': 'https://img.icons8.com/color/512/amazon-web-services.png',
        'terraform': 'https://img.icons8.com/color/512/terraform.png',
        'ansible': 'https://img.icons8.com/color/512/ansible.png',
        'github': 'https://img.icons8.com/color/512/github.png'
    }
    
    for name, url in logo_urls.items():
        path = os.path.join(logos_dir, f'{name}.png')
        if not os.path.exists(path):
            try:
                print(f"Downloading {name} logo...")
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Could not download {name} logo: {e}")

    # Initialize PDF
    pdf = PortfolioPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    
    # ----------------------------------------------------
    # PAGE 1: COVER PAGE
    # ----------------------------------------------------
    pdf.add_page()
    
    # Deep slate-navy header block
    pdf.set_fill_color(15, 23, 42) # Slate 900
    pdf.rect(0, 0, 210, 120, 'F')
    
    # Header text (White)
    pdf.set_y(35)
    pdf.set_font('helvetica', 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'GITOPS & MULTI-TOOL CLOUD', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, 'ORCHESTRATION PIPELINE', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Decorative line
    pdf.ln(5)
    pdf.set_draw_color(99, 102, 241) # Indigo 500
    pdf.set_line_width(1.5)
    pdf.line(65, pdf.get_y(), 145, pdf.get_y())
    
    # Subtitle
    pdf.ln(8)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(203, 213, 225) # Slate 300
    pdf.cell(0, 8, 'Automated AWS Infrastructure Provisioning and Configuration Management', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Bottom half details
    pdf.set_y(150)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(15, 23, 42) # Slate 900
    pdf.cell(0, 8, 'PROJECT DOCUMENTATION', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    # "Project By: Devam Tailor" banner
    pdf.set_y(175)
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 10, 'Project By: Devam Tailor', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Logo placement
    pdf.set_y(225)
    pdf.set_font('helvetica', 'B', 9)
    pdf.set_text_color(148, 163, 184) # Slate 400
    pdf.cell(0, 6, 'TECHNOLOGY INTEGRATION', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    # Render logos in a neat row
    logo_width = 16
    start_x = 42
    y_pos = 238
    
    for i, name in enumerate(['aws', 'terraform', 'ansible', 'github']):
        p = os.path.join(logos_dir, f'{name}.png')
        if os.path.exists(p):
            pdf.image(p, x=start_x + (i * 35), y=y_pos, w=logo_width)
            
    # ----------------------------------------------------
    # PAGE 2: EXECUTIVE SUMMARY & PROJECT GOALS
    # ----------------------------------------------------
    pdf.add_page()
    add_heading_1(pdf, '1. Executive Summary & Project Goals')
    
    add_body_text(pdf, 
        "This project implements a fully automated, cloud-native GitOps deployment pipeline using Amazon Web Services (AWS) "
        "to provision, secure, and configure a highly performant web server instance. The core objective is to eliminate manual "
        "infrastructure drifts, configuration hand-offs, and administrative errors by establishing Git as the single source "
        "of truth for both the infrastructure layers (declared via Terraform) and the system/software configurations (managed via Ansible)."
    )
    
    add_body_text(pdf, 
        "Modern cloud environments require absolute consistency. Traditional manual infrastructure tweaks lead to undocumented configuration "
        "drifts, making servers fragile and difficult to scale or replicate. This architecture addresses these pain points by integrating "
        "declarative Infrastructure as Code (IaC) and procedural configuration management into a unified continuous delivery pipeline."
    )
    
    add_body_text(pdf, "The pipeline is designed around several key goals, explained in detail below:")
    
    add_bullet_point(pdf, "Infrastructure Declarativity (Terraform):", 
        "All cloud resources, including isolated networks, subnets, gateway routings, and security boundaries are declared as code. "
        "This eliminates the risk of human error during resource allocation and guarantees identical deployments.")
        
    add_bullet_point(pdf, "Server Configuration Reproducibility (Ansible):", 
        "Once compute nodes are provisioned, configuration engines configure the host system. This ensures package updates, "
        "dependency alignments, service statuses, and folder boundaries conform exactly to defined standards.")
        
    add_bullet_point(pdf, "GitOps Delivery Automation (GitHub Actions):", 
        "The entire provisioning and configuration workflow is automated. Code merges to the main branch trigger "
        "immediate code linting, validation plans, and execution, removing local workstation differences.")
        
    add_bullet_point(pdf, "Remote State Isolation & Tracking:", 
        "Rather than local state tracking, a secure, isolated remote state backend is deployed. State changes are "
        "recorded directly in an AWS S3 bucket, preventing local state file loss or corruption.")

    # ----------------------------------------------------
    # PAGE 3: SYSTEM ARCHITECTURE
    # ----------------------------------------------------
    pdf.add_page()
    add_heading_1(pdf, '2. System Architecture & Component Design')
    
    add_body_text(pdf, 
        "The project architecture segments responsibilities between network provisioning and application configuration. "
        "All compute components reside in an isolated AWS Virtual Private Cloud (VPC), securing administrative boundaries "
        "while letting public clients access HTTP port 80."
    )
    
    add_body_text(pdf, "Core components and design patterns include:")
    
    add_bullet_point(pdf, "AWS Virtual Private Cloud (VPC):", 
        "An isolated virtual network using CIDR block 10.0.0.0/16, providing complete boundary control.")
        
    add_bullet_point(pdf, "Public Subnet & IGW Routing:", 
        "A public subnet (10.0.1.0/24) associated with an Internet Gateway (IGW) and public route tables to "
        "map dynamic public IP addresses to EC2 instances.")
        
    add_bullet_point(pdf, "AWS Security Groups (Web SG):", 
        "Inbound firewall rules allowing public HTTP (TCP port 80) and restricting SSH (TCP port 22) connections. "
        "Outbound rules permit all egress traffic, letting the host fetch software patches from external repositories.")
        
    add_bullet_point(pdf, "EC2 Compute Host (Ubuntu 22.04 LTS):", 
        "A micro compute instance configured with encrypted gp3 EBS volume storage, protecting data at rest.")
        
    insert_screenshot_dynamic(pdf, 'screenshots/ArchitechtureDiagram.png', 'VPC Network Topology and Provisioning Flow Diagram.')

    # ----------------------------------------------------
    # PAGE 4: CI/CD PIPELINE
    # ----------------------------------------------------
    pdf.add_page()
    add_heading_1(pdf, '3. CI/CD GitOps Pipeline (GitHub Actions)')
    
    add_body_text(pdf,
        "The automation engine runs under GitHub Actions, orchestrating a checkout, credential injection, "
        "Terraform plan validations, and Ansible playbooks. Reviewing the execution logs highlights a progression of fixes:"
    )
    
    add_bullet_point(pdf, "Authentication Setup (Runs 1 & 2):", 
        "The first runs failed early (under 18 seconds) because AWS keys and SSH private parameters were not yet "
        "configured in GitHub repository Secrets. This confirmed runner authentication locks.")
        
    add_bullet_point(pdf, "Manual Trigger Condition Gate (Run 3):", 
        "Enabling a manual trigger ('workflow_dispatch') succeeded in 17s but skipped all deployment stages. "
        "The cause was isolated to strict conditional gates (github.event_name == 'push') on individual jobs.")
        
    add_bullet_point(pdf, "First Complete Pipeline Execution (Run 4):", 
        "By adjusting conditional statements to allow push and dispatch triggers, the pipeline ran all 12 stages, "
        "provisioning cloud layers and running Ansible playbooks in 2m 34s.")
        
    add_bullet_point(pdf, "Remote State Backend Errors (Run 5):", 
        "Switching to remote state failed in 10s due to S3 bucket naming mismatches or missing IAM upload policies. "
        "Resolving these let Run 6 run successfully in 2m 9s with remote tracking active.")
    
    insert_screenshot_dynamic(pdf, 'screenshots/GithubActions.png', 'GitHub Actions workflow runs execution history.')

    # ----------------------------------------------------
    # PAGE 5: TERRAFORM PROVISIONING
    # ----------------------------------------------------
    pdf.add_page()
    add_heading_1(pdf, '4. Infrastructure Provisioning (Terraform)')
    
    add_body_text(pdf,
        "Terraform acts as the declarative infrastructure engine. It connects to the AWS provider API to verify "
        "current resource statuses, calculate delta plans, and provision VPC boundaries."
    )
    
    add_body_text(pdf, "Key resource definitions within the HCL files include:")
    
    add_bullet_point(pdf, "Dynamic AMI Queries:", 
        "Rather than hardcoding machine image IDs, data sources query canonical owner filters for the latest "
        "Ubuntu 22.04 LTS HVM SSD AMI, ensuring the OS includes current security patches.")
        
    add_bullet_point(pdf, "Compute Instance Configuration:", 
        "An aws_instance resource couples the dynamic AMI, the target public subnet, and the web security group. "
        "It attaches a secure SSH key pair for configuration engine access.")
        
    add_bullet_point(pdf, "EBS Block Storage Encryption:", 
        "Root storage uses gp3 solid-state drives configured with volume sizes of 20GB and volume encryption set to "
        "true, verifying data-at-rest protection policies.")
        
    add_bullet_point(pdf, "Output Variables:", 
        "Outputs expose the instance's public IP address, allowing CI/CD runners to feed IPs into Ansible inventories.")
    
    insert_screenshot_dynamic(pdf, 'screenshots/EC2Instance.png', 'AWS EC2 management console showing active web server instance.')

    # ----------------------------------------------------
    # PAGE 6: AWS S3 STATE BACKEND
    # ----------------------------------------------------
    pdf.add_page()
    add_heading_1(pdf, '5. AWS S3 Remote State Isolation')
    
    add_body_text(pdf,
        "Terraform relies on state files to map declared resources to real-world cloud objects. Storing state files locally "
        "presents significant security vulnerabilities, limits CI/CD runners from querying state history, and increases the "
        "risk of concurrent deployment conflicts. To resolve these, the backend is isolated to an AWS S3 bucket."
    )
    
    add_body_text(pdf, "Remote state best practices implemented in this architecture include:")
    
    add_bullet_point(pdf, "State Isolation:", 
        "Keeps state details, variables, and sensitive resource parameters out of the Git history, protecting public codebases.")
        
    add_bullet_point(pdf, "Encryption at Rest:", 
        "Configures the S3 backend block with encryption enabled, using S3 managed keys to secure infrastructure mapping data.")
        
    add_bullet_point(pdf, "Unified State Tracking:", 
        "Enables both local manual deployment debugging and automated CI/CD runners to share a single, accurate view "
        "of the AWS landscape, preventing state duplication errors.")
    
    insert_screenshot_dynamic(pdf, 'screenshots/S3.png', 'AWS S3 bucket state directory showing the encrypted tfstate object.')

    # ----------------------------------------------------
    # PAGE 7: ANSIBLE CONFIGURATION
    # ----------------------------------------------------
    pdf.add_page()
    add_heading_1(pdf, '6. Configuration Management (Ansible)')
    
    add_body_text(pdf,
        "Once compute instances respond to network queries, Ansible handles software configuration and landing portal "
        "deployment, ensuring the application configuration matches the desired system design."
    )
    
    add_body_text(pdf, "The Ansible playbook automates several configuration stages:")
    
    add_bullet_point(pdf, "System Patching & Updates:", 
        "Runs apt updates, retrieves remote repositories, and upgrades operating system packages to their latest stable releases.")
        
    add_bullet_point(pdf, "Nginx Service Provisioning:", 
        "Installs the Nginx web engine, registers the service under systemd, and configures it to run on boot.")
        
    add_bullet_point(pdf, "Web Root Permissions:", 
        "Configures ownership boundaries of the /var/www/html directory to the www-data owner group, protecting the web directory.")
        
    add_bullet_point(pdf, "Application Deployment:", 
        "Deploys an interactive landing page portal that visualizes the pipeline's progress directly onto the instance.")
        
    add_bullet_point(pdf, "Dynamic Host Resolution:", 
        "The GitHub Actions runner executes sed replacements to swap local inventory placeholder IPs (127.0.0.1) with "
        "the dynamic public IP outputted by Terraform, linking provisioning and configuration stages.")
    
    insert_screenshot_dynamic(pdf, 'screenshots/AnsibleOutput.png', 'Ansible playbook execution logs showing zero failed tasks in PLAY RECAP.')

    # ----------------------------------------------------
    # PAGE 8: LIVE PORTAL UI & CONCLUSION
    # ----------------------------------------------------
    pdf.add_page()
    add_heading_1(pdf, '7. Live Application Verification & Portal UI')
    
    add_body_text(pdf,
        "Upon successful pipeline runs, the deployment is validated by connecting to the EC2 instance's public IP address. "
        "The custom landing page utilizes Google Fonts (Plus Jakarta Sans and Space Grotesk), dark mode styling, "
        "and interactive JavaScript animations to visualize the deployment workflow stages."
    )
    
    add_body_text(pdf, 
        "This project demonstrates that combining Terraform's declarative cloud provisioning with Ansible's configuration "
        "capabilities creates a robust DevOps framework. It eliminates manual administration overhead, "
        "guarantees environment consistency, and provides a clear deployment path from developer commit to live production server."
    )
    
    add_body_text(pdf, "Recommended next steps to scale this deployment include:")
    
    add_bullet_point(pdf, "DynamoDB State Locking:", 
        "Adding an AWS DynamoDB table to lock state files during concurrent Terraform executions, preventing state corruption.")
        
    add_bullet_point(pdf, "Domain Integration:", 
        "Hooking the public IP address up to a custom domain using AWS Route53 DNS zones, and installing automated Let's Encrypt SSL certificates.")
        
    add_bullet_point(pdf, "Application Telemetry:", 
        "Installing Prometheus nodes and Grafana dashboards to monitor server health, CPU loads, and network bandwidth in real-time.")
    
    insert_screenshot_dynamic(pdf, 'screenshots/PublicIPOP.png', 'Live GitOps Cloud Portal web interface indicating successful rollout.')
    
    # Save PDF
    pdf.output('GitOps_Pipeline_Documentation.pdf')
    print("PDF generation completed successfully.")

if __name__ == '__main__':
    main()
