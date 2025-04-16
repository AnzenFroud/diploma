import os
import sys
import subprocess
from pathlib import Path

def is_admin():
    if sys.platform.startswith("win"):
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        # Для Linux/macOS можно добавить проверку на root, если нужно
        return os.geteuid() == 0 if hasattr(os, "geteuid") else True

def run_as_admin():
    import ctypes
    params = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    # Перезапускаем скрипт с правами администратора
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{sys.argv[0]}" {params}', None, 1)
    sys.exit()

def install_requirements():
    print("[*] Установка зависимостей из requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[+] Зависимости успешно установлены.")
    except subprocess.CalledProcessError as e:
        print("[!] Ошибка установки зависимостей:", e)

def build_exe():
    print("[*] Компиляция main.py в main.exe с помощью PyInstaller...")
    main_py = Path(__file__).parent / "elements" / "main.py"
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            str(main_py)
        ])
        print("[+] Компиляция завершена.")
    except subprocess.CalledProcessError as e:
        print("[!] Ошибка компиляции main.py в exe:", e)

def create_shortcut():
    print("[*] Создание ярлыка...")
    desktop = Path.home() / "Desktop"
    shortcut_name = "MyTkApp"

    if sys.platform.startswith("win"):
        try:
            from win32com.client import Dispatch

            exe_path = Path(__file__).parent / "dist" / "main.exe"
            if not exe_path.exists():
                print(f"[!] Ошибка: файл {exe_path} не найден. Сначала скомпилируйте main.py в main.exe.")
                return

            shortcut_path = desktop / f"{shortcut_name}.lnk"

            # Удаляем старый ярлык, если он есть
            if shortcut_path.exists():
                try:
                    shortcut_path.unlink()
                except PermissionError:
                    print(f"[!] Не удалось удалить существующий ярлык {shortcut_path}. Закройте все приложения, использующие этот файл.")
                    return

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(exe_path)
            shortcut.WorkingDirectory = str(exe_path.parent)
            shortcut.IconLocation = str(exe_path)
            shortcut.save()
            print("[+] Ярлык создан на рабочем столе.")
        except ImportError:
            print("[!] Ошибка: не установлены необходимые библиотеки pywin32.")
            print("Установите их командой: pip install pywin32")
        except PermissionError:
            print("[!] Ошибка: отказано в доступе при сохранении ярлыка. Попробуйте запустить скрипт от имени администратора.")
        except Exception as e:
            print("[!] Ошибка создания ярлыка (Windows):", e)

    elif sys.platform == "darwin":  # macOS
        shortcut = desktop / shortcut_name
        main_path = Path(__file__).parent / "elements" / "main.py"
        try:
            with open(shortcut, 'w') as f:
                f.write(f'#!/bin/bash\npython3 "{main_path}"\n')
            os.chmod(shortcut, 0o755)
            print("[+] Ярлык создан на рабочем столе (macOS).")
        except Exception as e:
            print("[!] Ошибка создания ярлыка (macOS):", e)

    elif sys.platform.startswith("linux"):
        shortcut = desktop / f"{shortcut_name}.desktop"
        main_path = Path(__file__).parent / "elements" / "main.py"
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

def main():
    if sys.platform.startswith("win") and not is_admin():
        print("[*] Запуск с повышенными правами администратора...")
        run_as_admin()

    install_requirements()
    build_exe()
    create_shortcut()
    print("✔ Установка завершена.")

if __name__ == "__main__":
    main()
