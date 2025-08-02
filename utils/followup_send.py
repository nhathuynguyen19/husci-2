

class FollowUpSend:
    def __init__(self):
        self.success = [
            "*Đăng nhập thành công!*",
            "*Đã đăng nhập!*",
            "*Đã đăng xuất!*",
        ]
        self.failure = [
            "*Không có thông báo mới nhất!*",
            "*Lỗi khi xem thông báo mới nhất!*",
            "*Đăng nhập thất bại, tài khoản hoặc mật khẩu không chính xác!*",
            "*Đăng nhập thất bại, mật khẩu không chính xác!*",
            "*Lỗi khi đăng nhập!*",
            "*Vui lòng đăng nhập (`/login`) để sử dụng tính năng này!*",
            "*Lỗi hệ thống vui lòng thử lại sau!*",
        ]