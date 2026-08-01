import os
import subprocess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


SCRIPTS = {
    "Bash Scripts": {
        "apache_virtualhost_setup.sh": "bash/apache_virtualhost_setup.sh",
        "basic_tool_install_on_the_server.sh": "bash/basic_tool_install_on_the_server.sh",
        "change_php_version.sh": "bash/change_php_version.sh",
        "create_db.sh": "bash/create_db.sh",
        "laravel_project_setup.sh": "bash/laravel_project_setup.sh",
    },

    "Python Scripts": {
        "email_testing.py": "python/email_testing.py",
        "nginx_virtualhost_setup.py": "python/nginx_virtualhost_setup.py",
        "ssh_connect.py": "python/ssh_connect.py",
    }
}


def run_script(path):

    full_path = os.path.join(BASE_DIR, path)

    print("\nRunning:", full_path)
    print("-" * 40)

    if path.endswith(".sh"):
        subprocess.run(["bash", full_path])

    elif path.endswith(".py"):
        subprocess.run(["python", full_path])


def main():

    while True:

        print("\n========== DEVOPS MENU ==========\n")

        options = []

        count = 1

        for category, scripts in SCRIPTS.items():

            print(f"\n[{category}]")

            for name, path in scripts.items():
                print(f"{count}. {name}")

                options.append(path)
                count += 1


        print("\n0. Exit")


        choice = input("\nSelect script: ")


        if choice == "0":
            print("Bye...")
            break


        try:
            choice = int(choice)

            if 1 <= choice <= len(options):
                run_script(options[choice-1])
            else:
                print("Invalid option")

        except ValueError:
            print("Enter number only")


if __name__ == "__main__":
    main()