import os
import re
import sys
import socket
import subprocess
import glob


# ============================================================
# Nginx + PHP-FPM Virtual Host Setup Assistant
# ============================================================


def check_root():
    if os.geteuid() != 0:
        print("Error: Please run this script with sudo.")
        print("Example:")
        print("sudo python3 nginx_domain_setup.py")
        sys.exit(1)


def run_command(command, check=False):
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=check
        )
    except FileNotFoundError:
        return None


# ============================================================
# Server IP
# ============================================================

def get_server_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "your_server_ip"


# ============================================================
# Nginx
# ============================================================

def check_and_install_nginx():
    print("\nChecking if Nginx is installed...")

    nginx_check = run_command(["which", "nginx"])

    if nginx_check and nginx_check.returncode == 0:

        version_run = run_command(["nginx", "-v"])

        if version_run:
            version_output = (
                version_run.stderr.strip()
                if version_run.stderr
                else version_run.stdout.strip()
            )

            print(f"Nginx is already installed!")
            print(f"Version: {version_output}")

        return True

    print("Nginx is NOT installed.")

    choice = input(
        "Kya aap Nginx install karna chahte hain? (y/n): "
    ).strip().lower()

    if choice != "y":
        print("Script aborted because Nginx is required.")
        sys.exit(1)

    try:

        print("\nRunning apt update...")
        subprocess.run(
            ["apt", "update"],
            check=True
        )

        print("Installing Nginx...")
        subprocess.run(
            ["apt", "install", "-y", "nginx"],
            check=True
        )

        print("Starting Nginx...")
        subprocess.run(
            ["systemctl", "start", "nginx"],
            check=True
        )

        print("Enabling Nginx on boot...")
        subprocess.run(
            ["systemctl", "enable", "nginx"],
            check=True
        )

        print("Nginx installed successfully.")

        return True

    except subprocess.CalledProcessError as e:

        print(f"Nginx installation failed: {e}")
        sys.exit(1)


# ============================================================
# PHP Detection
# ============================================================

def get_php_version():

    print("\nChecking PHP installation...")

    php_check = run_command(["which", "php"])

    if not php_check or php_check.returncode != 0:

        print("PHP is NOT installed.")

        choice = input(
            "Kya aap PHP install karna chahte hain? (y/n): "
        ).strip().lower()

        if choice != "y":
            print("PHP is required for this setup.")
            sys.exit(1)

        try:

            print("Running apt update...")

            subprocess.run(
                ["apt", "update"],
                check=True
            )

            print("Installing PHP...")

            subprocess.run(
                ["apt", "install", "-y", "php"],
                check=True
            )

        except subprocess.CalledProcessError as e:

            print(f"PHP installation failed: {e}")
            sys.exit(1)

    version_result = run_command(
        ["php", "-r", "echo PHP_MAJOR_VERSION.'.'.PHP_MINOR_VERSION;"]
    )

    if not version_result or version_result.returncode != 0:

        print("Could not detect PHP version.")
        sys.exit(1)

    php_version = version_result.stdout.strip()

    if not re.match(r"^\d+\.\d+$", php_version):

        print(f"Invalid PHP version detected: {php_version}")
        sys.exit(1)

    print(f"PHP version detected: {php_version}")

    return php_version


# ============================================================
# PHP-FPM Detection
# ============================================================

def find_php_fpm_socket():

    socket_patterns = [
        "/run/php/php*-fpm.sock",
        "/var/run/php/php*-fpm.sock"
    ]

    sockets = []

    for pattern in socket_patterns:
        sockets.extend(glob.glob(pattern))

    sockets = list(dict.fromkeys(sockets))

    if not sockets:
        return None

    # Prefer actual socket files
    valid_sockets = []

    for socket_path in sockets:

        if os.path.exists(socket_path):

            if os.path.exists(socket_path):
                valid_sockets.append(socket_path)

    if not valid_sockets:
        return None

    # Sort versions naturally
    valid_sockets.sort(reverse=True)

    return valid_sockets[0]


def get_fpm_service_from_socket(socket_path):

    if not socket_path:
        return None

    filename = os.path.basename(socket_path)

    match = re.match(
        r"php(\d+\.\d+)-fpm\.sock",
        filename
    )

    if not match:
        return None

    version = match.group(1)

    return f"php{version}-fpm"


def check_and_install_php_fpm(php_version):

    print("\nChecking PHP-FPM...")

    socket_path = find_php_fpm_socket()

    if socket_path:

        service_name = get_fpm_service_from_socket(
            socket_path
        )

        print("PHP-FPM socket detected:")
        print(f"  {socket_path}")

        if service_name:

            print("PHP-FPM service:")
            print(f"  {service_name}")

            service_check = run_command(
                [
                    "systemctl",
                    "is-active",
                    service_name
                ]
            )

            if (
                not service_check
                or service_check.stdout.strip() != "active"
            ):

                print(
                    f"\nPHP-FPM service '{service_name}' "
                    f"is not running."
                )

                choice = input(
                    "Kya aap PHP-FPM service start karna "
                    "chahte hain? (y/n): "
                ).strip().lower()

                if choice == "y":

                    try:

                        subprocess.run(
                            [
                                "systemctl",
                                "start",
                                service_name
                            ],
                            check=True
                        )

                        subprocess.run(
                            [
                                "systemctl",
                                "enable",
                                service_name
                            ],
                            check=True
                        )

                        print(
                            f"{service_name} started successfully."
                        )

                    except subprocess.CalledProcessError as e:

                        print(
                            f"Could not start PHP-FPM: {e}"
                        )
                        sys.exit(1)

                else:

                    print(
                        "PHP-FPM must be running for PHP websites."
                    )
                    sys.exit(1)

        return find_php_fpm_socket()

    # --------------------------------------------------------
    # No FPM socket found
    # --------------------------------------------------------

    print("PHP-FPM is NOT installed or no FPM socket was found.")

    package_name = f"php{php_version}-fpm"

    print(
        f"\nDetected PHP version: {php_version}"
    )

    print(
        f"Required PHP-FPM package: {package_name}"
    )

    choice = input(
        f"Kya aap {package_name} install karna chahte hain? (y/n): "
    ).strip().lower()

    if choice != "y":

        print(
            "PHP-FPM is required for PHP websites."
        )
        sys.exit(1)

    try:

        print("\nRunning apt update...")

        subprocess.run(
            ["apt", "update"],
            check=True
        )

        print(
            f"Installing {package_name}..."
        )

        subprocess.run(
            [
                "apt",
                "install",
                "-y",
                package_name
            ],
            check=True
        )

        service_name = package_name

        print(
            f"Starting {service_name}..."
        )

        subprocess.run(
            [
                "systemctl",
                "start",
                service_name
            ],
            check=True
        )

        print(
            f"Enabling {service_name} on boot..."
        )

        subprocess.run(
            [
                "systemctl",
                "enable",
                service_name
            ],
            check=True
        )

    except subprocess.CalledProcessError as e:

        print(
            f"PHP-FPM installation failed: {e}"
        )
        sys.exit(1)

    # Check socket again
    socket_path = find_php_fpm_socket()

    if not socket_path:

        print(
            "PHP-FPM installed but socket could not be found."
        )
        print(
            "Please check /run/php/ manually."
        )
        sys.exit(1)

    print(
        f"PHP-FPM socket detected: {socket_path}"
    )

    return socket_path


# ============================================================
# Domain Validation
# ============================================================

def get_valid_domain():

    domain_regex = re.compile(
        r"^(?=.{1,253}$)"
        r"(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
        r"[a-zA-Z]{2,63}$"
    )

    while True:

        domain = input(
            "\nEnter Domain Name (e.g., mysite.com): "
        ).strip().lower()

        if not domain:

            print(
                "Error: Domain name khaali nahi ho sakta."
            )
            continue

        if " " in domain:

            print(
                "Error: Domain name me spaces nahi ho sakte."
            )
            continue

        if "://" in domain or "/" in domain:

            print(
                "Error: Sirf domain name enter karein."
            )
            print(
                "Example: example.com"
            )
            continue

        if not domain_regex.match(domain):

            print(
                "Error: Invalid domain format."
            )
            continue

        return domain


# ============================================================
# Web Root
# ============================================================

def get_valid_path(domain):

    default_path = f"/var/www/html/{domain}"

    while True:

        path = input(
            f"Enter Web Root Path "
            f"[Default: {default_path}]: "
        ).strip()

        if not path:

            path = default_path

        if " " in path:

            print(
                "Error: Path me spaces nahi hone chahiye."
            )
            continue

        if not path.startswith("/"):

            print(
                f"Converting path to: /{path}"
            )

            path = f"/{path}"

        if os.path.exists(path):

            choice = input(
                f"\nWarning: Path '{path}' already exists."
                "\nUse it anyway? (y/n): "
            ).strip().lower()

            if choice != "y":
                continue

        return path


# ============================================================
# Hosts File
# ============================================================

def manage_hosts_file(domain):

    choice = input(
        f"\nKya aap '{domain}' ko /etc/hosts me add "
        f"karna chahte hain? (y/n): "
    ).strip().lower()

    if choice != "y":

        print(
            "Skipped /etc/hosts configuration."
        )
        return

    print(
        "\nWarning:"
    )
    print(
        "Production server par public domain ko"
    )
    print(
        "127.0.0.1 par point karna normally required nahi hai."
    )

    confirm = input(
        "Phir bhi /etc/hosts me add karein? (y/n): "
    ).strip().lower()

    if confirm != "y":

        print(
            "Skipped /etc/hosts configuration."
        )
        return

    hosts_path = "/etc/hosts"

    try:

        with open(hosts_path, "r") as f:
            content = f.read()

        pattern = rf"(^|\s){re.escape(domain)}(\s|$)"

        if re.search(pattern, content, re.MULTILINE):

            print(
                f"Notice: '{domain}' already exists in /etc/hosts."
            )
            return

        entry_line = (
            f"127.0.0.1\t{domain} www.{domain}\n"
        )

        with open(hosts_path, "a") as f:
            f.write(entry_line)

        print(
            f"Successfully added '{domain}' to /etc/hosts."
        )

    except Exception as e:

        print(
            f"Error updating /etc/hosts: {e}"
        )


# ============================================================
# Create Index PHP
# ============================================================

def create_index_php(web_root, domain):

    index_file = os.path.join(
        web_root,
        "index.php"
    )

    if os.path.exists(index_file):

        print(
            f"index.php already exists:"
        )

        print(
            f"  {index_file}"
        )

        choice = input(
            "Do you want to overwrite it? (y/n): "
        ).strip().lower()

        if choice != "y":

            print(
                "Existing index.php preserved."
            )
            return

    php_content = f"""<?php

echo "<!DOCTYPE html>";
echo "<html lang='en'>";
echo "<head>";
echo "<meta charset='UTF-8'>";
echo "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
echo "<title>{domain}</title>";
echo "</head>";
echo "<body>";
echo "<h1>Configured {domain} Successfully!</h1>";
echo "<p>Nginx and PHP-FPM are working.</p>";
echo "</body>";
echo "</html>";

?>
"""

    with open(index_file, "w") as f:
        f.write(php_content)

    print(
        f"Created: {index_file}"
    )


# ============================================================
# Nginx Config
# ============================================================

def create_nginx_config(
    domain,
    web_root,
    fpm_socket
):

    conf_file = (
        f"/etc/nginx/sites-available/{domain}"
    )

    symlink_file = (
        f"/etc/nginx/sites-enabled/{domain}"
    )

    nginx_config = f"""server {{
    listen 80;
    listen [::]:80;

    server_name {domain} www.{domain};

    root {web_root};
    index index.php index.html index.htm;

    location / {{
        try_files $uri $uri/ /index.php?$query_string;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:{fpm_socket};
    }}

    location ~ /\\.ht {{
        deny all;
    }}

    access_log /var/log/nginx/{domain}_access.log;
    error_log /var/log/nginx/{domain}_error.log;
}}
"""

    try:

        with open(conf_file, "w") as f:
            f.write(nginx_config)

        print(
            f"Created Nginx config:"
        )
        print(
            f"  {conf_file}"
        )

        if (
            os.path.exists(symlink_file)
            or os.path.islink(symlink_file)
        ):

            os.remove(symlink_file)

        os.symlink(
            conf_file,
            symlink_file
        )

        print(
            "Nginx site enabled successfully."
        )

        return conf_file, symlink_file

    except Exception as e:

        print(
            f"Could not create Nginx configuration: {e}"
        )
        sys.exit(1)


# ============================================================
# Nginx Test
# ============================================================

def test_nginx():

    print(
        "\nTesting Nginx configuration..."
    )

    result = subprocess.run(
        ["nginx", "-t"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        print(
            "Nginx configuration test successful!"
        )

        if result.stderr:
            print(result.stderr)

        return True

    print(
        "Nginx configuration test FAILED!"
    )

    if result.stderr:
        print(result.stderr)

    return False


# ============================================================
# Certbot
# ============================================================

def check_certbot():

    print(
        "\nChecking Certbot..."
    )

    certbot_check = run_command(
        ["which", "certbot"]
    )

    if (
        certbot_check
        and certbot_check.returncode == 0
    ):

        version = run_command(
            ["certbot", "--version"]
        )

        if version:

            output = (
                version.stdout.strip()
                if version.stdout
                else version.stderr.strip()
            )

            print(
                f"Certbot is already installed: {output}"
            )

        return True

    print(
        "Certbot is NOT installed."
    )

    choice = input(
        "Kya aap Certbot install karna chahte hain? (y/n): "
    ).strip().lower()

    if choice != "y":

        print(
            "HTTPS setup skipped."
        )
        return False

    try:

        print(
            "Running apt update..."
        )

        subprocess.run(
            ["apt", "update"],
            check=True
        )

        print(
            "Installing Certbot and Nginx plugin..."
        )

        subprocess.run(
            [
                "apt",
                "install",
                "-y",
                "certbot",
                "python3-certbot-nginx"
            ],
            check=True
        )

        print(
            "Certbot installed successfully."
        )

        return True

    except subprocess.CalledProcessError as e:

        print(
            f"Certbot installation failed: {e}"
        )
        return False


# ============================================================
# HTTPS Setup
# ============================================================

def setup_https(domain):

    print(
        "\n=============================================="
    )
    print(
        "              HTTPS / SSL SETUP"
    )
    print(
        "=============================================="
    )

    choice = input(
        f"Do you want to enable HTTPS for "
        f"'{domain}'? (y/n): "
    ).strip().lower()

    if choice != "y":

        print(
            "HTTPS setup skipped."
        )
        return False

    print(
        "\nBefore continuing, make sure:"
    )

    print(
        f"1. {domain} DNS is pointing to this server."
    )

    print(
        "2. Port 80 is open."
    )

    print(
        "3. Port 443 is open."
    )

    print(
        "4. HTTP website is accessible."
    )

    confirm = input(
        "\nContinue with HTTPS setup? (y/n): "
    ).strip().lower()

    if confirm != "y":

        print(
            "HTTPS setup cancelled."
        )
        return False

    if not check_certbot():

        return False

    print(
        f"\nRunning:"
    )

    print(
        f"certbot --nginx -d {domain}"
    )

    result = subprocess.run(
        [
            "certbot",
            "--nginx",
            "-d",
            domain
        ],
        text=True
    )

    if result.returncode == 0:

        print(
            "\nHTTPS certificate installed successfully."
        )

        print(
            f"HTTPS URL: https://{domain}"
        )

        return True

    print(
        "\nCertbot failed."
    )

    return False


# ============================================================
# Main
# ============================================================

def main():

    check_root()

    print(
        "=============================================="
    )

    print(
        "       Nginx + PHP-FPM Virtual Host"
    )

    print(
        "              Setup Assistant"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # Nginx
    # --------------------------------------------------------

    check_and_install_nginx()

    # --------------------------------------------------------
    # PHP
    # --------------------------------------------------------

    php_version = get_php_version()

    # --------------------------------------------------------
    # PHP-FPM
    # --------------------------------------------------------

    fpm_socket = check_and_install_php_fpm(
        php_version
    )

    if not fpm_socket:

        print(
            "ERROR: PHP-FPM socket not found."
        )
        sys.exit(1)

    print(
        "\nUsing PHP-FPM socket:"
    )

    print(
        f"  {fpm_socket}"
    )

    # --------------------------------------------------------
    # Domain
    # --------------------------------------------------------

    domain = get_valid_domain()

    # --------------------------------------------------------
    # Web Root
    # --------------------------------------------------------

    web_root = get_valid_path(
        domain
    )

    # --------------------------------------------------------
    # Paths
    # --------------------------------------------------------

    conf_file = (
        f"/etc/nginx/sites-available/{domain}"
    )

    symlink_file = (
        f"/etc/nginx/sites-enabled/{domain}"
    )

    print(
        "\n=============================================="
    )

    print(
        f"Setting up domain: {domain}"
    )

    print(
        f"Web Root: {web_root}"
    )

    print(
        f"PHP Version: {php_version}"
    )

    print(
        f"PHP-FPM Socket: {fpm_socket}"
    )

    print(
        "=============================================="
    )

    try:

        # ----------------------------------------------------
        # Create Web Root
        # ----------------------------------------------------

        os.makedirs(
            web_root,
            exist_ok=True
        )

        # ----------------------------------------------------
        # www-data ownership
        # ----------------------------------------------------

        try:

            import pwd
            import grp

            uid = pwd.getpwnam(
                "www-data"
            ).pw_uid

            gid = grp.getgrnam(
                "www-data"
            ).gr_gid

            os.chown(
                web_root,
                uid,
                gid
            )

            os.chmod(
                web_root,
                0o755
            )

            print(
                "Web root permissions configured."
            )

        except KeyError:

            print(
                "Warning: www-data user/group not found."
            )

        # ----------------------------------------------------
        # Create index.php
        # ----------------------------------------------------

        create_index_php(
            web_root,
            domain
        )

        # ----------------------------------------------------
        # Create Nginx Config
        # ----------------------------------------------------

        create_nginx_config(
            domain,
            web_root,
            fpm_socket
        )

        # ----------------------------------------------------
        # Test Nginx
        # ----------------------------------------------------

        if not test_nginx():

            print(
                "\nRolling back Nginx configuration..."
            )

            if os.path.islink(
                symlink_file
            ):

                os.remove(
                    symlink_file
                )

            if os.path.exists(
                conf_file
            ):

                os.remove(
                    conf_file
                )

            sys.exit(1)

        # ----------------------------------------------------
        # Reload Nginx
        # ----------------------------------------------------

        print(
            "\nReloading Nginx..."
        )

        subprocess.run(
            [
                "systemctl",
                "reload",
                "nginx"
            ],
            check=True
        )

        print(
            "Nginx reloaded successfully."
        )

        # ----------------------------------------------------
        # Hosts
        # ----------------------------------------------------

        manage_hosts_file(
            domain
        )

        # ----------------------------------------------------
        # HTTP Result
        # ----------------------------------------------------

        server_ip = get_server_ip()

        print(
            "\n=============================================="
        )

        print(
            "          HTTP SETUP COMPLETE"
        )

        print(
            "=============================================="
        )

        print(
            f"Domain     : http://{domain}"
        )

        print(
            f"Server IP  : http://{server_ip}"
        )

        print(
            f"Web Root   : {web_root}"
        )

        print(
            f"PHP        : {php_version}"
        )

        print(
            f"PHP-FPM    : {fpm_socket}"
        )

        print(
            "=============================================="
        )

        # ----------------------------------------------------
        # HTTPS
        # ----------------------------------------------------

        https_enabled = setup_https(
            domain
        )

        # ----------------------------------------------------
        # Final Test
        # ----------------------------------------------------

        print(
            "\nRunning final Nginx configuration test..."
        )

        if not test_nginx():

            print(
                "Warning: Final Nginx test failed."
            )

            sys.exit(1)

        subprocess.run(
            [
                "systemctl",
                "reload",
                "nginx"
            ],
            check=True
        )

        # ----------------------------------------------------
        # Final Output
        # ----------------------------------------------------

        print(
            "\n=============================================="
        )

        print(
            "              SETUP COMPLETE"
        )

        print(
            "=============================================="
        )

        print(
            f"Domain    : {domain}"
        )

        print(
            f"Web Root  : {web_root}"
        )

        print(
            f"PHP       : {php_version}"
        )

        print(
            f"PHP-FPM   : {fpm_socket}"
        )

        print(
            f"HTTP      : http://{domain}"
        )

        if https_enabled:

            print(
                f"HTTPS     : https://{domain}"
            )

        else:

            print(
                "HTTPS     : Not configured"
            )

        print(
            "=============================================="
        )

    except subprocess.CalledProcessError as e:

        print(
            f"\nCommand failed: {e}"
        )

        sys.exit(1)

    except KeyboardInterrupt:

        print(
            "\n\nSetup cancelled by user."
        )

        sys.exit(1)

    except Exception as e:

        print(
            f"\nSomething went wrong: {e}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()