import data
import halaman_login
import menu_admin
import menu_pengguna


def jalankan_program():
    data.buka_database("basis.db")

    program_jalan = True

    while program_jalan:
        data.bersihkan_layar()
        data.tampil_banner()
        data.console.print("HP tersedia saat ini : [bold green]" +
                           str(data.hitung_hp_tersedia()) + "[/]")
        data.tampil_menu([
            ("1", "Login"),
            ("2", "Register"),
            ("3", "Keluar"),
        ])
        pilih = data.tanya("Pilih menu : ")

        if pilih == "1":
            user = halaman_login.login()

            if user is None:
                data.cetak_error("Percobaan habis. Program berakhir.")
                program_jalan = False
            elif user["role"] == "Admin":
                menu_admin.menu_admin(user["username"])
            else:
                menu_pengguna.menu_pengguna(user["username"])

        elif pilih == "2":
            halaman_login.register()

        elif pilih == "3":
            data.cetak_sukses("Terima kasih telah menggunakan BASIS. Program selesai.")
            program_jalan = False

        else:
            data.cetak_error("Menu tidak tersedia!")
            data.tunggu()

    data.tutup_database()


if __name__ == "__main__":
    jalankan_program()