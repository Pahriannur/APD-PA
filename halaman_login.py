import data


def login():
    # mengembalikan data user kalau berhasil, None kalau 3x gagal
    percobaan = 0

    while percobaan < 3:
        data.bersihkan_layar()
        print("=== LOGIN ===")
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        user = data.cek_login(username, password)
        if user is not None:
            print("Login Berhasil")
            input("Tekan Enter untuk lanjut...")
            return user

        percobaan += 1
        print("Login Gagal. Sisa percobaan:", 3 - percobaan)
        input("Tekan Enter untuk lanjut...")

    return None


def register():
    data.bersihkan_layar()
    print("=== REGISTER ===")
    user_baru = input("Username baru : ").strip()
    pass_baru = input("Password baru (min. 3 karakter) : ").strip()
    try:
        data.register_user(user_baru, pass_baru)
    except ValueError as pesan_error:
        print("Error:", pesan_error)
    else:
        print("Registrasi berhasil! Silakan login.")
    finally:
        input("Tekan Enter untuk kembali...")