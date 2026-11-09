import data


def menu_admin(nama_aktif):
    role_aktif = "Admin"
    sudah_login = True

    while sudah_login:
        data.bersihkan_layar()
        data.tampil_header(nama_aktif, role_aktif)
        data.tampil_menu([
            ("1", "Jual HP              (Create)"),
            ("2", "Lihat / Cari HP      (Read)"),
            ("3", "Ubah Data HP         (Update)"),
            ("4", "Hapus HP             (Delete)"),
            ("5", "Kelola Pengguna"),
            ("6", "Riwayat Semua Transaksi"),
            ("7", "Beli HP dari Pengguna"),
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
            kelola_pengguna()

        elif menu == "6":
            data.tampil_riwayat(nama_aktif, role_aktif)

        elif menu == "7":
            data.tampil_beli_hp(nama_aktif, role_aktif)

        elif menu == "0":
            sudah_login = False

        else:
            data.cetak_error("Menu tidak tersedia!")
            data.tunggu()


def kelola_pengguna():
    data.bersihkan_layar()
    data.tampil_judul("KELOLA PENGGUNA")
    data.tabel_pengguna(data.ambil_semua_user())
    hapus = data.tanya("Username yang ingin dihapus (kosong = batal) : ")
    if hapus != "":
        try:
            data.hapus_user(hapus)
        except ValueError as pesan_error:
            data.cetak_error(str(pesan_error))
        except KeyError:
            data.cetak_error("Username tidak ditemukan!")
        else:
            data.cetak_sukses("Pengguna dan HP miliknya berhasil dihapus.")
    data.tunggu()