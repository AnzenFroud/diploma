import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    print("[*] Установка зависимостей из requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[+] Зависимости успешно установлены.")
    except subprocess.CalledProcessError as e:
        print("[!] Ошибка установки зависимостей:", e)

def create_shortcut():
    print("[*] Создание ярлыка...")
    main_path = Path(__file__).parent / "elements" / "main.py"
    desktop = Path.home() / "Desktop"
    shortcut_name = "MyTkApp"

    if sys.platform.startswith("win"):
        try:
            import winshell
            from win32com.client import Dispatch

            shortcut = desktop / f"{shortcut_name}.lnk"
            shell = Dispatch('WScript.Shell')
            shortcut_obj = shell.CreateShortCut(str(shortcut))
            shortcut_obj.Targetpath = sys.executable
            shortcut_obj.Arguments = f'"{main_path}"'
            shortcut_obj.WorkingDirectory = str(main_path.parent)
            shortcut_obj.IconLocation = str(sys.executable)
            shortcut_obj.save()
            print("[+] Ярлык создан на рабочем столе.")
        except Exception as e:
            print("[!] Ошибка создания ярлыка (Windows):", e)
            print("Убедитесь, что установлены pywin32 и winshell: pip install pywin32 winshell")

    elif sys.platform == "darwin":  # macOS
        shortcut = desktop / shortcut_name
        try:
            with open(shortcut, 'w') as f:
                f.write(f'#!/bin/bash\npython3 "{main_path}"\n')
            os.chmod(shortcut, 0o755)
            print("[+] Ярлык создан на рабочем столе (macOS).")
        except Exception as e:
            print("[!] Ошибка создания ярлыка (macOS):", e)

    elif sys.platform.startswith("linux"):
        shortcut = desktop / f"{shortcut_name}.desktop"
        try:
            with open(shortcut, "w") as f:
                f.write(f"""[Desktop Entry]
Type=Application
Name={shortcut_name}
Exec=python3 "{main_path}"
Icon=utilities-terminal
Terminal=false
""")
            os.chmod(shortcut, 0o755)
            print("[+] Ярлык создан на рабочем столе (Linux).")
        except Exception as e:
            print("[!] Ошибка создания ярлыка (Linux):", e)

if __name__ == "__main__":
    install_requirements()
    create_shortcut()
    print("✔ Установка завершена.")
