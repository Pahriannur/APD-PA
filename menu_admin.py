import data


def menu_admin(nama_aktif):
    role_aktif = "Admin"
    sudah_login = True

    while sudah_login:
        data.bersihkan_layar()
        print("=" * 42)
        print("Halo,", nama_aktif, "(" + role_aktif + ")")
        print("=" * 42)
        print("[1] Jual HP              (Create)")
        print("[2] Lihat / Cari HP      (Read)")
        print("[3] Ubah Data HP         (Update)")
        print("[4] Hapus HP             (Delete)")
        print("[5] Kelola Pengguna")
        print("[6] Riwayat Semua Transaksi")
        print("[7] Beli HP dari Pengguna")
        print("[0] Logout")
        menu = input("Pilih menu: ").strip()

        if menu == "1":
            data.tampil_jual_hp(nama_aktif)

        elif menu == "2":
            data.tampil_lihat_hp()

        elif menu == "3":
            data.tampil_ubah_hp(nama_aktif, role_aktif)

        elif menu == "4":
            data.tampil_hapus_hp(nama_aktif, role_aktif)

        elif menu == "5":
            kelola_pengguna()

        elif menu == "6":
            data.tampil_riwayat(nama_aktif, role_aktif)

        elif menu == "7":
            data.tampil_beli_hp(nama_aktif, role_aktif)

        elif menu == "0":
            sudah_login = False

        else:
            print("Error: Menu tidak tersedia!")
            input("Tekan Enter untuk kembali...")


def kelola_pengguna():
    data.bersihkan_layar()
    print("=== KELOLA PENGGUNA ===")
    print("No | Username | Role | Saldo")
    print("-" * 45)
    nomor = 1
    for u in data.ambil_semua_user():
        print(nomor, "|", u["username"], "|", u["role"], "| Rp",
              data.format_rupiah(u["saldo"]))
        nomor += 1
    print("-" * 45)
    hapus = input("Username yang ingin dihapus (kosong = batal) : ").strip()
    if hapus != "":
        try:
            data.hapus_user(hapus)
        except ValueError as pesan_error:
            print("Error:", pesan_error)
        except KeyError:
            print("Error: Username tidak ditemukan!")
        else:
            print("Pengguna dan HP miliknya berhasil dihapus.")
    input("Tekan Enter untuk kembali...")