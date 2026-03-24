#Aangepast voor KOGEKA
from winotify import Notification, audio
import os
appName = "power.exe"
tempFolder = os.getenv('TEMP')
toast = Notification(
            app_id=appName,
            title="Herstel afsluiten",
            msg="Beste leerling, gelieve met je toestel even langs de ICT-dienst te gaan.\nDoe dit binnen de 5 schooldagen!",
            duration="long",
            icon=f"{tempFolder}/power/power.png",
        )
toast.set_audio(audio.Reminder, loop=True)
toast.show()