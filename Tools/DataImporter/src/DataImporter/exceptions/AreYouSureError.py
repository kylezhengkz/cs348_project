# AreYouSureError: Exception used as the last line of defence for some dangerous,
#   irreversible actions
class AreYouSureError(Exception):
    def __init__(self, action: str):
        super().__init__(f"ARE YOU SURE YOU WANT TO: {action}")