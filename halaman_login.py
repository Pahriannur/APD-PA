import data


def login():
    # mengembalikan data user kalau berhasil, None kalau 3x gagal
    percobaan = 0

    while percobaan < 3:
        data.bersihkan_layar()
        data.tampil_judul("LOGIN")
        username = data.tanya("Username : ")
        password = data.tanya_rahasia("Password : ")

        user = data.cek_login(username, password)
        if user is not None:
            data.cetak_sukses("Login Berhasil")
            data.tunggu("Tekan Enter untuk lanjut...")
            return user

        percobaan += 1
        data.cetak_error("Login Gagal. Sisa percobaan : " + str(3 - percobaan))
        data.tunggu("Tekan Enter untuk lanjut...")

    return None


def register():
    data.bersihkan_layar()
    data.tampil_judul("REGISTER")
    user_baru = data.tanya("Username baru : ")
    pass_baru = data.tanya_rahasia("Password baru (min. 3 karakter) : ")
    try:
        data.register_user(user_baru, pass_baru)
    except ValueError as pesan_error:
        data.cetak_error(str(pesan_error))
    else:
        data.cetak_sukses("Registrasi berhasil! Silakan login.")
    finally:
        data.tunggu()