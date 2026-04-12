import csv
import random
import uuid

CATEGORIES = {
    "Infrastructure": [
        ("Server {server} keeps crashing with out of memory exception.", "Increase RAM allocation to {server} by 16GB and restart daemon."),
        ("Deployment pipeline failing for {app_name} on EC2 instances.", "Clear IAM cache on the runner and restart the Jenkins pipeline."),
        ("High CPU utilization warning on main compute cluster.", "Scale out autoscaling group parameters locally and monitor graph drops."),
        ("Kubernetes pod stuck in crash loop backoff.", "Delete the failing pod to force replica set recreation and inspect container logs."),
        ("Disk space alert on production VM.", "Execute log rotation algorithm and purge generic temp files via script.")
    ],
    "Application": [
        ("Users reporting 500 internal server error on checkout.", "Rollback the last hotfix release {version} and check application load balancer endpoints."),
        ("The {module} module is returning blank pages intermittently.", "Restart the node backend processes processing frontend API calls."),
        ("Payment form throwing 'Invalid Token' upon submission.", "Regenerate Stripe API keys and update the secret manager cache."),
        ("App crashes when uploading files larger than 10MB.", "Change the nginx.conf client_max_body_size setting mapping to 50M."),
        ("Login button is unresponsive on mobile Safari.", "Update the frontend JS polyfills supporting legacy Safari engine.")
    ],
    "Security": [
        ("Detected suspicious login attempt from external IP block.", "Block IP range temporarily in WAF and force password reset for user {user}."),
        ("Vulnerability scan flagged outdated OpenSSL library.", "Patch the OS images across the fleet to the latest LTS security patch."),
        ("Unencrypted S3 bucket alert.", "Enable AES256 server-side encryption via AWS console policies."),
        ("Malware detected on workstation {host}.", "Isolate {host} from the network, run deep antivirus scan, and reinstall OS if needed."),
        ("API endpoint vulnerable to SQL Injection.", "Sanitize input parameters immediately via parameterized queries update.")
    ],
    "Database": [
        ("Database connection pool timeout causing slow loading.", "Increase PostgreSQL max_connections setting from 100 to 500."),
        ("Long running analytical queries blocking OLTP transactions.", "Kill PID {pid} mapping to the slow query and route analytics to the read replica."),
        ("Index fragmentation leading to slow SELECT performance.", "Run REINDEX TABLE manually during off-peak hours."),
        ("Database backup failed last night.", "Check S3 backup bucket permissions and manually trigger the cron snapshot."),
        ("Deadlock detected between transaction engines.", "Refactor the commit ordering sequence in the backend ORM mapped models.")
    ],
    "Network": [
        ("VPN connection failing for remote users in branch office.", "Restart the Cisco AnyConnect headend router and clear active sessions."),
        ("Packet loss spikes detected between core switches.", "Check physical fiber connections and spanning tree protocol logs."),
        ("DNS resolution failing for internal domain {domain}.", "Flush DNS cache locally and re-sync internal records on Active Directory."),
        ("Slow internet speeds reported across campus network.", "Identify top bandwidth hogging devices and apply QoS rate limiting."),
        ("BGP route flapping on the outbound gateway.", "Contact ISP to verify ASN route advertisement stability policies.")
    ],
    "Access Management": [
        ("User {user} needs access to Github repository.", "Add {user} to the 'Developers' GitHub organization group with write permissions."),
        ("Contractor {user} requires Jira access.", "Provision a standard license for {user} and assign to the Contractor user-tier."),
        ("Employee left company, please revoke permissions.", "Execute offboarding script to disable AD, email, and internal VPN accounts."),
        ("Password reset requested for executive account.", "Verify identity via phone callback and issue temporary secure password link."),
        ("Missing permissions to deploy to production AWS account.", "Assign IAM role 'Prod-Deployer' temporarily for 24 hours to {user}.")
    ]
}

SERVERS = ["web-prod-1", "db-prod-2", "cache-server-01", "auth-cluster-A", "analytics-node"]
APPS = ["Billing API", "Customer Portal", "Inventory System", "HR Dashboard", "Mobile Gateway"]
USERS = ["jdoe", "asmith", "kmiller", "rjohnson", "bwilliams"]
HOSTS = ["LAPTOP-72A", "DESKTOP-99B", "WS-ENGINEERING-1", "MAC-DESIGN-8"]
DOMAINS = ["corp.local", "intranet.internal", "dev.staging"]

def populate_template(text):
    text = text.replace("{server}", random.choice(SERVERS))
    text = text.replace("{app_name}", random.choice(APPS))
    text = text.replace("{module}", random.choice(APPS))
    text = text.replace("{user}", random.choice(USERS))
    text = text.replace("{host}", random.choice(HOSTS))
    text = text.replace("{domain}", random.choice(DOMAINS))
    text = text.replace("{version}", f"v{random.randint(1,4)}.{random.randint(0,9)}.{random.randint(0,9)}")
    text = text.replace("{pid}", str(random.randint(1000, 9999)))
    
    # Add slight random variations for semantic richness
    prefixes = ["Help: ", "Urgent: ", "Issue: ", "[Ticket] ", "Error: ", ""]
    suffixes = [" Please fix ASAP.", " Need assistance.", " This is blocking us.", " Happens intermittently.", ""]
    if random.random() > 0.6:
        text = random.choice(prefixes) + text
    if random.random() > 0.7:
        text = text + random.choice(suffixes)
    return text

def generate_csv(num_tickets=1000):
    with open('tickets.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "description", "category", "resolution", "priority"])
        
        for i in range(1, num_tickets + 1):
            category = random.choice(list(CATEGORIES.keys()))
            template_desc, template_res = random.choice(CATEGORIES[category])
            
            description = populate_template(template_desc)
            resolution = populate_template(template_res)
            
            # Extract a sensible title from the description
            title = description[:40] + "..." if len(description) > 40 else description
            title = title.replace("Help: ", "").replace("Urgent: ", "")
            
            priority = random.choice(["Low", "Medium", "High", "Critical"])
            if "fail" in description.lower() or "crash" in description.lower():
                priority = random.choice(["High", "Critical"])
                
            writer.writerow([f"TKT-{i:04d}", title, description, category, resolution, priority])

if __name__ == "__main__":
    generate_csv(1000)
    print("Generated tickets.csv with 1000 synthetic enterprise records.")
