

class FollowUpSend:
    def __init__(self):
        self.success = [
            "**Đăng nhập thành công!**",
            "**Đã đăng nhập!**"
        ]
        self.failure = [
            "**Không có thông báo mới nhất!**",
            "**Lỗi khi xem thông báo mới nhất!**",
            "**Đăng nhập thất bại, tài khoản hoặc mật khẩu không đúng!**",
            "**Đăng nhập thất bại, mật khẩu không đúng!**",
            "**Lỗi đăng nhập!**"
        ]