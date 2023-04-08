# Website - Phát hiện lỗi bảo mật trên các mã nguồn mở

# Chức Năng:
- Báo các lỗi xuất hiện tình trạng mất an toàn trên các mã nguồn mở có các đường link như: .gov, .vn, .gov, .vn, ...
- Thông báo đến người dùng qua SMS khi xuất hiện lỗi nghiêm trọng
- CRUD giúp người dùng tự tạo ra database lỗi bảo mật riêng

# Công nghệ sử dụng
- Python django
- Mysql
- MISP tool

# Hướng dẫn sử dụng

## Chuẩn bị môi trường
- Cài đặt python
- Cài đặt mysql community server
## Cài đặt

```text
Step 1: pip install virtualenv 
Step 2: pip freeze requirements.txt
Step 3: pip install -r requirements.txt
Bước 4: Tiến hành vào folder Web -> chọn file settings.py -> thay đổi value của trường password trong file settings.py thành mật khẩu của mysql mà bạn đã cài đặt.
Bước 5: python manage.py migrate
Bước 6: python manage.py makemigrations
Bước 7: python manage.py runserver
```

Sau khi cài đặt hoàn tất bạn có thể sử dụng website và tự config nguồn tin được lấy từ MISP và ZONE-H.