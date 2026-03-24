#Persoonlijke versie voor thuis gebruik (vanaf versie 6)
#pyinstaller command: pyinstaller power.pyw --onefile -n "power.exe" -i power.ico -w --add-data="stoppowerstartup.ps1:." --add-data="power.png:."

#Volgende update: app kunnen hernoemen, test handmatig updaten

import pystray, os, PIL.Image, shutil, webbrowser, threading, sys, subprocess, time, socket
from subprocess import run as command
from tkinter import messagebox, simpledialog
import tkinter as tk

versie = "6"
standaardNaam = "power.exe"

website = "https://github.com/De-nerd/shutdown"
opstartFolder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
tempFolder = os.getenv('TEMP')
currentFolder = os.getcwd()
appName = "power.exe" #sys.argv[0] #Normaal gezien kan de app nu wel hernoemt worden zonder problemen, maar dit is ook nog niet getest
mainLocatie = os.path.join(opstartFolder, appName)

if not os.path.exists(f"{tempFolder}/power"):
    os.mkdir(f"{tempFolder}/power")

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
ps_script_location = resource_path("stoppowerstartup.ps1")
current_execution_policy = command("powershell -Command Get-ExecutionPolicy -Scope CurrentUser",shell=True, capture_output=True, text=True)
current_execution_policy = current_execution_policy.stdout.strip()
with open(ps_script_location, "r") as original_ps_script_file:
    original_ps_script = original_ps_script_file.read()
with open(f"{tempFolder}/power/stoppowerstartup.ps1", "w") as ps_script:
    ps_script.write(original_ps_script)
def taskkill():
    command("powershell -Command Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser" ,shell=True)
    command(f"powershell -Command {tempFolder}/power/stoppowerstartup.ps1", shell=True)
    time.sleep(10)
    command(f"powershell -Command Set-ExecutionPolicy -ExecutionPolicy {current_execution_policy} -Scope CurrentUser", shell=True)

def checkInternetConnectionToGithub():
    try:
        InterNetCheckGitHub = socket.create_connection(("github.com", 80))
        if InterNetCheckGitHub is not None:
            InterNetCheckGitHub.close()
            return True
    except:
        return False

def checkForUpdates():
    global versie
    def GeenInternetVerbinding():
        messagebox.showwarning("Geen internet verbinding","De app heeft geen toegang tot het internet, check uw internet.\nDe app kan ook werken zonder internet verbinding maar dan kan hij niet controleren voor updates.")
        if messagebox.askyesno("Internet verbinding",'Als u wilt controleren op updates moet u internet verbinding hebben.\nDruk op "ja" als u weer internet verbinding heeft om te controleren op updates, anders drukt u op "nee".'):
            checkForUpdates()
    if not os.path.exists(f"{tempFolder}/power"):
        os.mkdir(f"{tempFolder}/power")

    if checkInternetConnectionToGithub() == True:
        command(f"cd {tempFolder}/power && curl -OL https://raw.githubusercontent.com/De-nerd/shutdown/refs/heads/main/version.info", shell=True)
    else:
        noInternet = threading.Thread(target=GeenInternetVerbinding)
        noInternet.start()
    try:
        with open(f"{tempFolder}/power/version.info", "r") as versieCheckFile:
            if int(versieCheckFile.readline()) <= int(versie):
                if os.path.exists(f"{tempFolder}/power/versie.txt"):
                    with open(f"{tempFolder}/power/versie.txt", "r") as versieCheckFileOld:
                        versieOldLokaal = int(versieCheckFileOld.readline())
                    if versieOldLokaal < int(versie):
                        with open(f"{tempFolder}/power/actie.txt", "w") as actietxt:
                            actietxt.write("updateLocal")
                        with open(f"{tempFolder}/power/versie.txt", "w") as versieCheckFileOld:
                            versieCheckFileOld.write(versie)
                        try:
                            os.remove(f"{tempFolder}/power/{appName}")
                            time.sleep(1)
                        except:
                            pass
                        shutil.copy(os.path.join(currentFolder, appName), f"{tempFolder}/power")
                        subprocess.Popen(f"{tempFolder}/power/{appName}", cwd=f"{tempFolder}/power")
                        time.sleep(1)
                        sys.exit()
                elif not os.path.exists(f"{tempFolder}/power/versie.txt"):
                    with open(f"{tempFolder}/power/actie.txt", "w") as actietxt:
                        actietxt.write("update")
                    try:
                        os.remove(f"{tempFolder}/power/{appName}")
                        time.sleep(1)
                    except:
                        pass
                    shutil.copy(os.path.join(currentFolder, appName), f"{tempFolder}/power")
                    subprocess.Popen(f"{tempFolder}/power/{appName}", cwd=f"{tempFolder}/power")
                    time.sleep(1)
                    sys.exit()
            elif int(versieCheckFile.readline()) > int(versie):
                with open(f"{tempFolder}/power/actie.txt", "w") as actietxt:
                    actietxt.write("update")
                try:
                    os.remove(f"{tempFolder}/power/{appName}")
                    time.sleep(1)
                except:
                    pass
                shutil.copy(os.path.join(currentFolder, appName), f"{tempFolder}/power")
                subprocess.Popen(f"{tempFolder}/power/{appName}", cwd=f"{tempFolder}/power")
                time.sleep(1)
                sys.exit()
    except:
        pass

def updateApp():
    time.sleep(10)
    taskkill()
    os.remove(mainLocatie)
    time.sleep(1)
    command(f"cd {opstartFolder} && curl -OL https://github.com/De-nerd/shutdown/releases/latest/download/power.exe", shell=True)
    time.sleep(2)
    with open(f"{tempFolder}/power/version.info", "r") as versieCheckFile:
        versieNew = int(versieCheckFile.readline())
    try:
        with open(f"{tempFolder}/power/versie.txt", "r") as oldVersieCheckFile:
            global versieOld
            versieOld = int(oldVersieCheckFile.readline())
    except:
        versieOld = int(versie)
    with open(f"{tempFolder}/power/versie.txt", "w") as versieFile:
        versieFile.write(str(versieNew))
    if messagebox.askyesno(appName,f'De app is succesvol bijgewerkt. Om de update van versie {int(versieOld)} naar versie {versieNew} te voltooien moet u uw computer opnieuw opstarten.\nDruk op "ja" om uw computer opnieuw op te starten.'):
        command('shutdown /r /t 10 /c "Uw computer wordt opnieuw opgestart om de update te voltooien."')

if currentFolder == f"{tempFolder}\\power":
    with open(f"{tempFolder}/power/actie.txt", "r") as actieInTempFolder:
        actie = actieInTempFolder.readline()
        if actie == "remove":
            time.sleep(10)
            try:
                taskkill()
                time.sleep(1)
            except:
                pass
            os.remove(mainLocatie)
            messagebox.showinfo("remove power", "De power app is succesvol van uw apparaat verwijderd!")
        if actie == "update":
            updateApp()
        if actie == "updateLocal":
            time.sleep(10)
            try:
                taskkill()
                time.sleep(1)
            except:
                pass
            os.remove(mainLocatie)
            shutil.copy(f"{tempFolder}/power/power.exe", mainLocatie)
            if messagebox.askyesno(appName, f'De app is succesvol bijgewerkt. Om de update naar versie {versie} te voltooien moet u uw computer opnieuw opstarten.\nDruk op "ja" om uw computer opnieuw op te starten.'):
                command('shutdown /r /t 10 /c "Uw computer wordt opnieuw opgestart om de update te voltooien."')

    os.remove(f"{tempFolder}/power/actie.txt")
    sys.exit()
else:
    if not os.path.exists(mainLocatie):
        shutil.copy(os.path.join(currentFolder, appName), opstartFolder)
        if messagebox.askyesno(appName, f'De app "power.exe" versie {versie} is succesvol geïnstalleerd. Om de installatie te voltooien moet u uw computer opnieuw opstarten.\nDruk op "ja" om uw computer opnieuw op te starten.'):
            command('shutdown /r /t 10 /c "Uw computer wordt opnieuw opgestart om de installatie te voltooien."')
    else:
        if not os.path.exists(f"{tempFolder}/power/"):
            os.mkdir(f"{tempFolder}/power/")
        if currentFolder == opstartFolder:
            with open(f"{tempFolder}/power/versie.txt", "w") as versietxt:
                versietxt.write(versie)
        checkForUpdates()

        if not os.path.exists(f"{tempFolder}/power/power.png"):
            shutil.copy(str(resource_path("power.png")), f"{tempFolder}/power/power.png")
        img = PIL.Image.open(f"{tempFolder}/power/power.png")

        def remove(icon):
            if messagebox.askokcancel('Bevestig verwijderen', 'Druk op "Ok" om het verwijderen van deze app van uw computer te bevestigen.'):
                shutil.copy(os.path.join(currentFolder, appName), f"{tempFolder}/power")
                with open(f"{tempFolder}/power/actie.txt", "w") as actieInTempFolder:
                    actieInTempFolder.write("remove")
                subprocess.Popen(f"{tempFolder}/power/{appName}", cwd=f"{tempFolder}/power")
                time.sleep(1)
                icon.stop()
                sys.exit()
        def toonVersie():
            messagebox.showinfo("Versie", f"Versie: {versie}")

        def shutdown():
            command('shutdown /s /t 10 /c "Afsluiten in 10 seconden"', shell=True)
        def reboot():
            command('shutdown /r /t 10 /c "Opnieuw opstarten in 10 seconden"', shell=True)
        def logout():
            command('shutdown /l', shell=True)
        def sleep():
            command('shutdown /h', shell=True)
        def lock():
            command('%systemroot%\\system32\\rundll32.exe user32.dll,LockWorkStation', shell=True)
        def cancel ():
            command('shutdown /a', shell=True)
        def stop ():
            icon.stop()
        def info():
            webbrowser.open(website)
        def WhatsappChannel():
            webbrowser.open("https://whatsapp.com/channel/0029VbAZ1ZWKmCPW6QSjAR3Q")
        def WhatsappCommunity():
            webbrowser.open("https://chat.whatsapp.com/HzLlIRzwzGm19uz9zNIRnp")
        def verwijder():
            rem = threading.Thread(target=remove, args=[icon])
            rem.start()
        def showVersion():
            showVer = threading.Thread(target=toonVersie)
            showVer.start()


        def RunCustomAction():
            tkRoot = tk.Tk()
            tkRoot.iconphoto(True, tk.PhotoImage(file=f"{tempFolder}/power/power.png"))
            tkRoot.withdraw()
            CustomAction = simpledialog.askinteger("Actie", "Voer de actienummer in:", parent=tkRoot)
            if CustomAction == 69: # start Rickroll
                webbrowser.open("https://youtu.be/dQw4w9WgXcQ?si=guIr4AdITuDCGO6M")
            tkRoot.destroy()
            exit()
        def startCustomActionThread():
            TrCA = threading.Thread(target=RunCustomAction)
            TrCA.start()


        icon = pystray.Icon(name="power", icon=img, title="Energie opties", menu=pystray.Menu(
            pystray.MenuItem("Afsluiten", shutdown, default=True),
            pystray.MenuItem("Opnieuw opstarten", reboot),
            pystray.MenuItem("Afmelden", logout),
            pystray.MenuItem("Slaapstand", sleep),
            pystray.MenuItem("Vergrendelen", lock),
            pystray.MenuItem("Annuleer afsluiten of opnieuw opstarten", cancel),
            pystray.MenuItem("Info", pystray.Menu(
                pystray.MenuItem("Versie", showVersion),
                pystray.MenuItem("Github", info),
                pystray.MenuItem("WhatsApp Channel", WhatsappChannel),
                pystray.MenuItem("WhatsApp Community", WhatsappCommunity),
            )),
            pystray.MenuItem("Actie", startCustomActionThread), #voer een actie uit
            pystray.MenuItem("Check voor updates", checkForUpdates),#Check voor nieuwere versie en installeer indien beschikbaar #checken werkt, maar echt installeren kan nog een foutmelding geven omdat de systemtray icon al actief is. Dit is nog niet getest
            pystray.MenuItem("Verwijder", verwijder),
            pystray.MenuItem("Exit", stop),
        )
                            )
        icon.run()
