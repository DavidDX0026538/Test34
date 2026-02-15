class ServiceWatchdog:
    def __init__(self):
        self.state = "stopped"
        self.current_time = 0
        self.start_time = None

        self.TIME_STARTING = 2
        self.TIME_FAILED = 1
        self.TIME_RESTARTING = 3

    def log(self, msg):
        print(f"[t={self.current_time}] {msg}")

    # ---------- события ----------

    def handle_command(self, cmd):
        self.log(f"COMMAND -> {cmd}")

        if self.state == "stopped":
            self.stopped(cmd)
        elif self.state == "starting":
            self.starting(cmd)
        elif self.state == "running":
            self.running(cmd)
        elif self.state == "failed":
            self.failed(cmd)
        elif self.state == "restarting":
            self.restarting(cmd)

    def tick(self):
        self.current_time += 1
        self.log("TICK")

        if self.state == "starting":
            self.starting(None)
        elif self.state == "failed":
            self.failed(None)
        elif self.state == "restarting":
            self.restarting(None)
        # running и stopped на тик не реагируют

        self.log(f"CURRENT STATE = {self.state}")

    # ---------- состояния ----------

    def stopped(self, cmd):
        if cmd == "start":
            self.state = "starting"
            self.start_time = self.current_time
            self.log("STATE -> starting")
        else:
            self.log("IGNORED (stopped)")

    def starting(self, cmd):
        if self.current_time - self.start_time >= self.TIME_STARTING:
            self.state = "running"
            self.log("STATE -> running")

    def running(self, cmd):
        if cmd == "stop":
            self.state = "stopped"
            self.log("STATE -> stopped")
        elif cmd == "crash":
            self.state = "failed"
            self.start_time = self.current_time
            self.log("STATE -> failed")
        else:
            self.log("IGNORED (running)")

    def failed(self, cmd):
        if self.current_time - self.start_time >= self.TIME_FAILED:
            self.state = "restarting"
            self.start_time = self.current_time
            self.log("STATE -> restarting")

    def restarting(self, cmd):
        if self.current_time - self.start_time >= self.TIME_RESTARTING:
            self.state = "stopped"
            self.log("STATE -> stopped")


# ---------- запуск ----------

watchdog = ServiceWatchdog()

print("Команды: start | stop | crash | tick | exit")
watchdog.log("SYSTEM START")

while True:
    cmd = input("> ").strip().lower()

    if cmd == "exit":
        watchdog.log("EXIT")
        break

    if cmd == "tick":
        watchdog.tick()
    else:
        watchdog.handle_command(cmd)
