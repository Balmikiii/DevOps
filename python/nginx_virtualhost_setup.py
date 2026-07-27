import os
import re
import sys
import socket
import subprocess

def check_root():
    if os.geteuid() != 0:
        print("Error: Please run this script with sudo (e.g., sudo python3 nginx_doman_setup.py)")
        sys.exit(1)

def get_server_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()
        s.close()
        return ip
    except Exception:
        return "your_server_ip"

def check_and_install_nginx():
    print("Checking if Nginx is installed...")
    nginx_check = subprocess.run(["which", "nginx"], capture_output=True, text=True)
    
    if nginx_check.returncode == 0:
        version_run = subprocess.run(["nginx", "-v"], capture_output=True, text=True)
        version_output = version_run.stderr.strip() if version_run.stderr else version_run.stdout.strip()
        print(f"Nginx is already installed! ({version_output})")
        return True
    
    print("Nginx is NOT installed on this system.")
    choice = input("Kya aap Nginx install karna chahte hain? (y/n): ").strip().lower()
    
    if choice == 'y':
        try:
            print("Running: sudo apt update...")
            subprocess.run(["apt", "update"], check=True)
            
            print("Running: sudo apt install -y nginx...")
            subprocess.run(["apt", "install", "-y", "nginx"], check=True)
            
            print("Starting Nginx service...")
            subprocess.run(["systemctl", "start", "nginx"], check=True)
            
            print("Enabling Nginx to start on boot...")
            subprocess.run(["systemctl", "enable", "nginx"], check=True)
            
            print("Nginx status:")
            subprocess.run(["systemctl", "status", "nginx", "--no-pager"], check=False)
            
            print("Nginx installed and started successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Nginx installation fail ho gaya: {e}")
            sys.exit(1)
    else:
        print("Script aborted because Nginx is required.")
        sys.exit(1)

def get_valid_domain():
    domain_regex = re.compile(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    while True:
        domain = input("\nEnter Domain Name (e.g., mysite.com): ").strip()
        
        if not domain:
            print("Error: Domain name khaali (empty) nahi ho sakta.")
            continue
            
        if " " in domain:
            print("Error: Domain name me spaces nahi ho sakte.")
            continue
            
        if not domain_regex.match(domain):
            print("Error: Invalid domain format! (http:// ya special characters mat use karo).")
            continue
            
        return domain

def get_valid_path(domain):
    default_path = f"/var/www/html/{domain}"
    
    while True:
        path = input(f"Enter Web Root Path [Default: {default_path}]: ").strip()
        
        if not path:
            path = default_path
            
        if " " in path:
            print("Error: Path me spaces nahi ho sakte.")
            continue
            
        if not path.startswith("/"):
            print(f"Warning: Aapne shuruat me '/' nahi lagaya. Converting to: /{path}")
            path = f"/{path}"
            
        if os.path.exists(path):
            choice = input(f"Warning: Path '{path}' pehle se maujood hai. Use it anyway? (y/n): ").strip().lower()
            if choice != 'y':
                continue
                
        return path

def manage_hosts_file(domain):
    choice = input(f"\nKya aap '{domain}' ko /etc/hosts file me add karna chahte hain? (y/n): ").strip().lower()
    if choice != 'y':
        print("Skipped /etc/hosts configuration.")
        return

    hosts_path = "/etc/hosts"
    entry_line = f"127.0.0.1\t{domain} www.{domain}\n"
    
    try:
        with open(hosts_path, "r") as f:
            content = f.read()
        
        if domain in content:
            print(f"Notice: '{domain}' entry pehle se hi /etc/hosts me maujood hai.")
        else:
            with open(hosts_path, "a") as f:
                f.write(entry_line)
            print(f"Successfully added '{domain}' to /etc/hosts.")
    except Exception as e:
        print(f"Error: /etc/hosts update karne me dikkat aayi: {e}")

def main():
    check_root()
    
    print("==============================================")
    print("    Nginx Virtual Host Assistant    ")
    print("==============================================")
    
    check_and_install_nginx()
    
    domain = get_valid_domain()
    web_root = get_valid_path(domain)
    
    conf_file = f"/etc/nginx/sites-available/{domain}"
    symlink_file = f"/etc/nginx/sites-enabled/{domain}"
    
    print(f"\nSetting up Virtual Host for {domain} at {web_root}...")
    
    try:
        os.makedirs(web_root, exist_ok=True)
        
        import pwd, grp
        uid = pwd.getpwnam("www-data").pw_uid
        gid = grp.getgrnam("www-data").gr_gid
        os.chown(web_root, uid, gid)
        os.chmod(web_root, 0o755)
        
        index_file = os.path.join(web_root, "index.html")
        if not os.path.exists(index_file):
            html_content = f"""<!DOCTYPE html>
<html>
<head><title>{domain}</title></head>
<body><h1>Configured {domain} Successfully!</h1></body>
</html>"""
            with open(index_file, "w") as f:
                f.write(html_content)
                
        nginx_config = f"""server {{
    listen 80;
    listen [::]:80;

    server_name {domain} www.{domain};

    root {web_root};
    index index.html index.htm;

    location / {{
        try_files $uri $uri/ =404;
    }}

    access_log /var/log/nginx/{domain}_access.log;
    error_log /var/log/nginx/{domain}_error.log;
}}"""
        
        with open(conf_file, "w") as f:
            f.write(nginx_config)
            
        if os.path.exists(symlink_file) or os.path.islink(symlink_file):
            os.remove(symlink_file)
        os.symlink(conf_file, symlink_file)
        print("Site configuration enabled via symlink.")
        
        print("Testing Nginx configuration (sudo nginx -t)...")
        test_result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)
        
        if test_result.returncode == 0:
            print("Restarting Nginx service...")
            subprocess.run(["systemctl", "restart", "nginx"], check=True)
            
            print("Reloading Nginx configuration...")
            subprocess.run(["systemctl", "reload", "nginx"], check=True)
            
            manage_hosts_file(domain)
            
            server_ip = get_server_ip()
            print("\n==============================================")
            print(f"Success: Virtual host for '{domain}' is live!")
            print(f"Web Root Path: {web_root}")
            print("Test in your browser using these links:")
            print(f"   -> http://{domain}")
            print(f"   -> http://{server_ip}")
            print(f"   -> http://localhost")
            print("==============================================")
        else:
            print("Error: Nginx configuration test fail ho gaya. Rolling back changes...")
            print(test_result.stderr)
            if os.path.exists(conf_file): os.remove(conf_file)
            if os.path.exists(symlink_file): os.remove(symlink_file)
            
    except Exception as e:
        print(f"Somethink is wrong!: {e}")

if __name__ == "__main__":
    main()
