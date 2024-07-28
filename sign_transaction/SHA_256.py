import hashlib
import os

random_data = os.urandom(64)  # Tạo dữ liệu ngẫu nhiên
hash_object = hashlib.sha256(random_data)  # Tạo băm SHA-256
hash_value = hash_object.hexdigest()  # Lấy giá trị băm dạng hexadecimal

print(hash_value)
