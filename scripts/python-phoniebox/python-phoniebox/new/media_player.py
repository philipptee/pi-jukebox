import mpd

def MopidyClient():
    def __init__(self, host="localhost", port=6600):
        self._host = host
        self._port = port
        self._client = mpd.MPDClient(use_unicode=True)
        self.Reset()

    def Reset(self):
        self._client.connect(self._host, self._port)

    def Add(self, uri):
        self._client.add(uri)

    def Play(self):
        self._client.play()
    
    def TogglePlay(self):
        # Pause is really toggling pause/play.
        self._client.pause()