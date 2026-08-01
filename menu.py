import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_scripts():
    scripts = []
    folders = ["bash", "python"]
    for folder in folders:
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.exists(folder_path):
            continue
        for file in sorted(os.listdir(folder_path)):
            full_path = os.path.join(folder_path, file)
            if os.path.isfile(full_path):
                if file.endswith((".sh", ".py")):
                    scripts.append({
                        "name": file,
                        "path": full_path
                    })
    return scripts

def run_script(script):
    print("\nRunning:", script["name"])
    print("-" * 40)

    if script["name"].endswith(".sh"):
        subprocess.run(
            ["bash", script["path"]]
        )
    elif script["name"].endswith(".py"):
        subprocess.run(
            ["py", script["path"]]
        )

def main():
    while True:
        scripts = find_scripts()
        print("\n========== DEVOPS MENU ==========\n")

        for i, script in enumerate(scripts, start=1):
            print(f"{i}. {script['name']}")
        print("\n0. Exit")
        choice = input("\nSelect script: ")

        if choice == "0":
            break
        try:
            choice = int(choice)

            if 1 <= choice <= len(scripts):
                run_script(
                    scripts[choice-1]
                )
            else:
                print("Invalid option")
        except ValueError:
            print("Enter number only")

if __name__ == "__main__":
    main()