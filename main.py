import data
import halaman_login
import menu_admin
import menu_pengguna


def jalankan_program():
    data.buka_database("toko_hp.db")

    program_jalan = True

    while program_jalan:
        data.bersihkan_layar()
        print("=" * 42)
        print("      TOKO JUAL BELI HP BEKAS")
        print("=" * 42)
        print("HP tersedia saat ini :", data.hitung_hp_tersedia())
        print("-" * 42)
        print("[1] Login")
        print("[2] Register")
        print("[3] Keluar")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            user = halaman_login.login()

            if user is None:
                print("Percobaan habis. Program berakhir.")
                program_jalan = False
            elif user["role"] == "Admin":
                menu_admin.menu_admin(user["username"])
            else:
                menu_pengguna.menu_pengguna(user["username"])

        elif pilih == "2":
            halaman_login.register()

        elif pilih == "3":
            print("Terima kasih. Program selesai.")
            program_jalan = False

        else:
            print("Error: Menu tidak tersedia!")
            input("Tekan Enter untuk kembali...")

    data.tutup_database()


if __name__ == "__main__":
    jalankan_program()