import data


def menu_pengguna(nama_aktif):
    role_aktif = "Pengguna Biasa"
    sudah_login = True

    while sudah_login:
        data.bersihkan_layar()
        print("=" * 42)
        print("Halo,", nama_aktif, "(" + role_aktif + ")")
        print("Saldo : Rp", data.format_rupiah(data.ambil_saldo(nama_aktif)))
        print("=" * 42)
        print("[1] Jual HP              (Create)")
        print("[2] Lihat / Cari HP      (Read)")
        print("[3] Ubah Data HP         (Update)")
        print("[4] Hapus HP             (Delete)")
        print("[5] Beli HP")
        print("[6] Riwayat Transaksi Saya")
        print("[7] Top Up Saldo")
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
            data.tampil_beli_hp(nama_aktif, role_aktif)

        elif menu == "6":
            data.tampil_riwayat(nama_aktif, role_aktif)

        elif menu == "7":
            top_up_saldo(nama_aktif)

        elif menu == "0":
            sudah_login = False

        else:
            print("Error: Menu tidak tersedia!")
            input("Tekan Enter untuk kembali...")


def top_up_saldo(nama_aktif):
    data.bersihkan_layar()
    print("=== TOP UP SALDO ===")
    print("Saldo saat ini : Rp", data.format_rupiah(data.ambil_saldo(nama_aktif)))
    print("(Minimal Rp 10.000, maksimal Rp 10.000.000)")
    nominal = input("Nominal top up (Rp) : ").strip()
    try:
        saldo_baru = data.top_up(nama_aktif, nominal)
    except ValueError as pesan_error:
        print("Error:", pesan_error)
    else:
        print("Top up berhasil!")
        print("Saldo sekarang : Rp", data.format_rupiah(saldo_baru))
    finally:
        input("Tekan Enter untuk kembali...")