def getRisk(name: str):
    # Search for an occurrance of a risky name in the action name.
    dangerousNames = ["admin", "password", "update", "login", "factory", "reset", "remote", "register", "default",
                      "ssh", "debug", "cmd", "shell", "ftp", "test", "root", "sudo"]
    riskyNames = ["setup", "database", "shutdown", "email", "import", "sql", "cli", "cgi", "upload", "download"]
    infoNames = ["info", "export", "csv", "details"]

    # Go through each "danger list" and return the danger level
    for searchName in dangerousNames:
        if searchName.lower().find(name):
            return 1
    for searchName in riskyNames:
        if searchName.lower().find(name):
            return 2
    for searchName in infoNames:
        if searchName.lower().find(name):
            return 3
    return 0
