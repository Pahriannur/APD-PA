import data


def menu_pengguna(nama_aktif):
    role_aktif = "Pengguna Biasa"
    sudah_login = True

    while sudah_login:
        data.bersihkan_layar()
        data.tampil_header(nama_aktif, role_aktif, data.ambil_saldo(nama_aktif))
        data.tampil_menu([
            ("1", "Jual HP              (Create)"),
            ("2", "Lihat / Cari HP      (Read)"),
            ("3", "Ubah Data HP         (Update)"),
            ("4", "Hapus HP             (Delete)"),
            ("5", "Beli HP"),
            ("6", "Riwayat Transaksi Saya"),
            ("7", "Top Up Saldo"),
            ("0", "Logout"),
        ])
        menu = data.tanya("Pilih menu : ")

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
            data.cetak_error("Menu tidak tersedia!")
            data.tunggu()


def top_up_saldo(nama_aktif):
    data.bersihkan_layar()
    data.tampil_judul("TOP UP SALDO", "green")
    data.console.print("Saldo saat ini : [bold green]Rp " +
                       data.format_rupiah(data.ambil_saldo(nama_aktif)) + "[/]")
    data.cetak_info("Minimal Rp 10.000, maksimal Rp 10.000.000")
    nominal = data.tanya("Nominal top up (Rp) : ")
    try:
        saldo_baru = data.top_up(nama_aktif, nominal)
    except ValueError as pesan_error:
        data.cetak_error(str(pesan_error))
    else:
        data.cetak_sukses("Top up berhasil!")
        data.console.print("Saldo sekarang : [bold green]Rp " +
                           data.format_rupiah(saldo_baru) + "[/]")
    finally:
        data.tunggu()