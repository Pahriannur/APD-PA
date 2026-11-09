
import lib_toko_hp as toko


def jalankan_program():
    toko.buka_database("toko_hp.db")

    program_jalan = True

    while program_jalan:
        toko.bersihkan_layar()
        print("=" * 42)
        print("      TOKO JUAL BELI HP BEKAS")
        print("=" * 42)
        print("HP tersedia saat ini :", toko.hitung_hp_tersedia())
        print("-" * 42)
        print("[1] Login")
        print("[2] Register")
        print("[3] Keluar")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            percobaan = 0
            sudah_login = False
            nama_aktif = ""
            role_aktif = ""

            while percobaan < 3:
                toko.bersihkan_layar()
                print("=== LOGIN ===")
                username = input("Username : ").strip()
                password = input("Password : ").strip()

                user = toko.cek_login(username, password)
                if user is not None:
                    sudah_login = True
                    nama_aktif = user["username"]
                    role_aktif = user["role"]

                if sudah_login:
                    print("Login Berhasil")
                    input("Tekan Enter untuk lanjut...")
                    break
                else:
                    percobaan += 1
                    print("Login Gagal. Sisa percobaan:", 3 - percobaan)
                    input("Tekan Enter untuk lanjut...")

            if percobaan == 3 and not sudah_login:
                print("Percobaan habis. Program berakhir.")
                program_jalan = False

            while sudah_login:
                toko.bersihkan_layar()
                print("=" * 42)
                print("Halo,", nama_aktif, "(" + role_aktif + ")")
                print("=" * 42)
                print("[1] Jual HP              (Create)")
                print("[2] Lihat / Cari HP      (Read)")
                print("[3] Ubah Data HP         (Update)")
                print("[4] Hapus HP             (Delete)")
                if role_aktif == "Admin":
                    print("[5] Kelola Pengguna")
                    print("[6] Riwayat Semua Transaksi")
                else:
                    print("[5] Beli HP")
                    print("[6] Riwayat Transaksi Saya")
                print("[0] Logout")
                menu = input("Pilih menu: ").strip()

                # ---------- CREATE ----------
                if menu == "1":
                    toko.bersihkan_layar()
                    print("=== JUAL HP ===")
                    merk = input("Merk          : ").strip()
                    tipe = input("Tipe          : ").strip()
                    print("Kondisi: [1] Mulus  [2] Baik  [3] Minus")
                    kondisi = input("Pilih kondisi : ").strip()
                    harga = input("Harga (Rp)    : ").strip()
                    try:
                        id_baru = toko.tambah_hp(nama_aktif, merk, tipe, kondisi, harga)
                    except ValueError as pesan_error:
                        print("Error:", pesan_error)
                    else:
                        print("HP berhasil didaftarkan dengan ID", id_baru)
                    finally:
                        input("Tekan Enter untuk kembali...")

                # ---------- READ ----------
                elif menu == "2":
                    toko.bersihkan_layar()
                    print("=== LIHAT / CARI HP ===")
                    print("[1] Tampilkan semua")
                    print("[2] Cari berdasarkan merk")
                    sub = input("Pilih: ").strip()
                    if sub != "1" and sub != "2":
                        print("Error: Pilihan tidak tersedia!")
                    else:
                        kata = ""
                        if sub == "2":
                            kata = input("Masukkan merk : ").lower().strip()
                        hasil = toko.cari_hp(kata)
                        print("-" * 78)
                        print("ID | Penjual | Merk | Tipe | Kondisi | Harga | Status")
                        print("-" * 78)
                        if len(hasil) == 0:
                            print("Data HP tidak ditemukan.")
                        else:
                            for h in hasil:
                                print(h["id"], "|", h["penjual"], "|", h["merk"], "|",
                                      h["tipe"], "|", h["kondisi"], "| Rp",
                                      toko.format_rupiah(h["harga"]), "|", h["status"])
                            print("-" * 78)
                            print("Jumlah data:", len(hasil))
                    input("Tekan Enter untuk kembali...")

                # ---------- UPDATE ----------
                elif menu == "3":
                    toko.bersihkan_layar()
                    print("=== UBAH DATA HP ===")
                    id_input = input("Masukkan ID HP yang ingin diubah : ").strip()
                    try:
                        if not toko.cek_angka(id_input):
                            raise ValueError("ID harus berupa angka!")
                        id_hp = int(id_input)
                        hp = toko.cek_boleh_ubah(id_hp, nama_aktif, role_aktif)

                        print("Data lama:", hp["merk"], hp["tipe"], "|", hp["kondisi"],
                              "| Rp", toko.format_rupiah(hp["harga"]))
                        print("(Kosongkan input jika tidak ingin mengubah)")
                        merk_baru = input("Merk baru    : ").strip()
                        tipe_baru = input("Tipe baru    : ").strip()
                        print("Kondisi: [1] Mulus  [2] Baik  [3] Minus")
                        kondisi_baru = input("Kondisi baru : ").strip()
                        harga_baru = input("Harga baru   : ").strip()

                        toko.ubah_hp(id_hp, merk_baru, tipe_baru, kondisi_baru, harga_baru)
                    except ValueError as pesan_error:
                        print("Error:", pesan_error)
                    except KeyError:
                        print("Error: ID tidak ditemukan!")
                    else:
                        print("Data HP berhasil diubah.")
                    finally:
                        input("Tekan Enter untuk kembali...")

                # ---------- DELETE ----------
                elif menu == "4":
                    toko.bersihkan_layar()
                    print("=== HAPUS HP ===")
                    id_input = input("Masukkan ID HP yang ingin dihapus : ").strip()
                    try:
                        if not toko.cek_angka(id_input):
                            raise ValueError("ID harus berupa angka!")
                        id_hp = int(id_input)
                        toko.cek_boleh_hapus(id_hp, nama_aktif, role_aktif)

                        yakin = input("Yakin ingin menghapus? (Y/T) : ").upper().strip()
                        if yakin != "Y" and yakin != "T":
                            raise ValueError("Pilihan harus Y atau T!")
                    except ValueError as pesan_error:
                        print("Error:", pesan_error)
                    except KeyError:
                        print("Error: ID tidak ditemukan!")
                    else:
                        if yakin == "Y":
                            toko.hapus_hp(id_hp)
                            print("Data HP berhasil dihapus.")
                        else:
                            print("Penghapusan dibatalkan.")
                    finally:
                        input("Tekan Enter untuk kembali...")

                # ---------- KELOLA PENGGUNA (ADMIN) ----------
                elif menu == "5" and role_aktif == "Admin":
                    toko.bersihkan_layar()
                    print("=== KELOLA PENGGUNA ===")
                    print("No | Username | Role")
                    print("-" * 35)
                    nomor = 1
                    for u in toko.ambil_semua_user():
                        print(nomor, "|", u["username"], "|", u["role"])
                        nomor += 1
                    print("-" * 35)
                    hapus = input("Username yang ingin dihapus (kosong = batal) : ").strip()
                    if hapus != "":
                        try:
                            toko.hapus_user(hapus)
                        except ValueError as pesan_error:
                            print("Error:", pesan_error)
                        except KeyError:
                            print("Error: Username tidak ditemukan!")
                        else:
                            print("Pengguna dan HP miliknya berhasil dihapus.")
                    input("Tekan Enter untuk kembali...")

                # ---------- BELI HP (PENGGUNA BIASA) ----------
                elif menu == "5" and role_aktif != "Admin":
                    toko.bersihkan_layar()
                    print("=== BELI HP ===")
                    print("Daftar HP yang tersedia:")
                    print("-" * 70)
                    daftar_beli = toko.daftar_hp_untuk_dibeli(nama_aktif)
                    for h in daftar_beli:
                        print(h["id"], "|", h["penjual"], "|", h["merk"], h["tipe"],
                              "|", h["kondisi"], "| Rp", toko.format_rupiah(h["harga"]))
                    print("-" * 70)

                    if len(daftar_beli) == 0:
                        print("Belum ada HP yang bisa dibeli.")
                    else:
                        id_input = input("Masukkan ID HP yang ingin dibeli : ").strip()
                        try:
                            if not toko.cek_angka(id_input):
                                raise ValueError("ID harus berupa angka!")
                            id_hp = int(id_input)
                            toko.cek_boleh_beli(id_hp, nama_aktif)

                            yakin = input("Yakin ingin membeli? (Y/T) : ").upper().strip()
                            if yakin != "Y" and yakin != "T":
                                raise ValueError("Pilihan harus Y atau T!")
                        except ValueError as pesan_error:
                            print("Error:", pesan_error)
                        except KeyError:
                            print("Error: ID tidak ditemukan!")
                        else:
                            if yakin == "Y":
                                toko.beli_hp(id_hp, nama_aktif)
                                print("Pembelian berhasil!")
                            else:
                                print("Pembelian dibatalkan.")
                    input("Tekan Enter untuk kembali...")

                # ---------- RIWAYAT ----------
                elif menu == "6":
                    toko.bersihkan_layar()
                    print("=== RIWAYAT TRANSAKSI ===")
                    print("-" * 70)
                    print("ID HP | Nama HP | Penjual | Pembeli | Harga | Jenis")
                    print("-" * 70)
                    hasil = toko.ambil_transaksi(nama_aktif, role_aktif)
                    if len(hasil) == 0:
                        print("Belum ada transaksi.")
                    else:
                        for t in hasil:
                            print(t["id_hp"], "|", t["nama_hp"], "|", t["penjual"], "|",
                                  t["pembeli"], "| Rp", toko.format_rupiah(t["harga"]),
                                  "|", t["jenis"])
                    input("Tekan Enter untuk kembali...")

                elif menu == "0":
                    sudah_login = False

                else:
                    print("Error: Menu tidak tersedia!")
                    input("Tekan Enter untuk kembali...")

        elif pilih == "2":
            toko.bersihkan_layar()
            print("=== REGISTER ===")
            user_baru = input("Username baru : ").strip()
            pass_baru = input("Password baru (min. 3 karakter) : ").strip()
            try:
                toko.register_user(user_baru, pass_baru)
            except ValueError as pesan_error:
                print("Error:", pesan_error)
            else:
                print("Registrasi berhasil! Silakan login.")
            finally:
                input("Tekan Enter untuk kembali...")

        elif pilih == "3":
            print("Terima kasih. Program selesai.")
            program_jalan = False

        else:
            print("Error: Menu tidak tersedia!")
            input("Tekan Enter untuk kembali...")

    toko.tutup_database()


if __name__ == "__main__":
    jalankan_program()