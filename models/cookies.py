

class Cookies:
    def __init__(self, token: str, session_id: str, portal: str):
        self.cookies = {
            "__RequestVerificationToken" : token,
            "ASP.NET_SessionId" : session_id,
            "UMS.StudentPortal.F5C0A1C9384C2E25E79BA1ABF5D9A037" : portal,
        }