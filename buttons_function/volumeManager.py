from playsound import playsound
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

class VolumeManager():
    def __init__(self):
        self.isOn = False
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            # print(f"\tok1\t{session}")
            program = str(session)
            # print(program.split(": ")[1])
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if program.split(": ")[1] == "python.exe":
                if float(volume.GetMasterVolume()) == 1:
                    self.isOn = True
                else:
                    self.isOn = False


    def volumeOn(self):
        return self.isOn

    def setVolume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:

            program = str(session)

            volume = session._ctl.QueryInterface(ISimpleAudioVolume)

            if program.split(": ")[1] == "python.exe":
                # print("-----------------------------------------------volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
                if self.isOn:
                    volume.SetMasterVolume(0, None)
                    # print("OFF "+ str(volume.GetMasterVolume())+" "+str(self.isOn))
                    self.isOn = False
                else:
                    volume.SetMasterVolume(1, None)
                    # print("ON "+ str(volume.GetMasterVolume())+" "+str(self.isOn))
                    playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\enable.wav")
                    self.isOn = True