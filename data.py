import os
import sqlite3
from rich import box
from rich.align import Align
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

daftar_kondisi = {"1": "Mulus", "2": "Baik", "3": "Minus"}

koneksi = None
kursor = None
console = Console()


# ======================================================
# TAMPILAN CANTIK (library rich)
# ======================================================
def aman(teks):
    # supaya tanda [ ] dari input pengguna tidak dianggap kode warna
    return escape(str(teks))


def tampil_banner():
    console.print(Panel(
        Align.center("[bold cyan]B A S I S[/]\n[dim]Toko Jual Beli HP Bekas[/]"),
        box=box.DOUBLE, border_style="cyan", width=50, padding=(1, 2)))


def tampil_judul(judul, warna="cyan"):
    console.print(Panel.fit("[bold]" + judul + "[/]", border_style=warna,
                            box=box.ROUNDED, padding=(0, 4)))


def tampil_header(nama, role, saldo=None):
    isi = "Halo, [bold]" + aman(nama) + "[/]  [dim]([/]" + aman(role) + "[dim])[/]"
    if saldo is not None:
        isi = isi + "\nSaldo : [bold green]Rp " + format_rupiah(saldo) + "[/]"
    console.print(Panel(isi, box=box.DOUBLE, border_style="cyan", width=50))


def tampil_menu(daftar_menu):
    # daftar_menu berisi pasangan (kode, teks)
    tabel = Table(box=box.SIMPLE, show_header=False, width=50)
    tabel.add_column("Kode", style="bold yellow", justify="center", width=6)
    tabel.add_column("Menu")
    for item in daftar_menu:
        tabel.add_row(item[0], item[1])
    console.print(tabel)


def cetak_error(pesan):
    console.print("[bold red]✘ Error:[/] " + pesan)


def cetak_sukses(pesan):
    console.print("[bold green]✔[/] " + pesan)


def cetak_info(pesan):
    console.print("[yellow]![/] " + pesan)


def tanya(teks):
    return console.input("[bold cyan]" + teks + "[/]").strip()


def tanya_rahasia(teks):
    return console.input("[bold cyan]" + teks + "[/]", password=True).strip()


def tunggu(teks="Tekan Enter untuk kembali..."):
    console.input("[dim]" + teks + "[/]")


def tabel_hp(hasil, judul, tampil_status=True):
    tabel = Table(title=judul, box=box.ROUNDED, header_style="bold cyan")
    tabel.add_column("ID", justify="right")
    tabel.add_column("Penjual")
    tabel.add_column("Merk")
    tabel.add_column("Tipe")
    tabel.add_column("Kondisi")
    tabel.add_column("Harga", justify="right", style="green")
    if tampil_status:
        tabel.add_column("Status")
    for h in hasil:
        baris = [str(h["id"]), aman(h["penjual"]), aman(h["merk"]),
                 aman(h["tipe"]), h["kondisi"], "Rp " + format_rupiah(h["harga"])]
        if tampil_status:
            if h["status"] == "Tersedia":
                baris.append("[green]Tersedia[/]")
            else:
                baris.append("[red]Terjual[/]")
        tabel.add_row(*baris)
    console.print(tabel)


def tabel_pengguna(daftar_user):
    tabel = Table(title="Daftar Pengguna", box=box.ROUNDED, header_style="bold cyan")
    tabel.add_column("No", justify="right")
    tabel.add_column("Username")
    tabel.add_column("Role")
    tabel.add_column("Saldo", justify="right", style="green")
    nomor = 1
    for u in daftar_user:
        tabel.add_row(str(nomor), aman(u["username"]), u["role"],
                      "Rp " + format_rupiah(u["saldo"]))
        nomor += 1
    console.print(tabel)


# ---------- DATABASE ----------
def buka_database(nama_db):
    global koneksi, kursor
    koneksi = sqlite3.connect(nama_db)
    koneksi.row_factory = sqlite3.Row
    kursor = koneksi.cursor()
    buat_tabel()
    isi_data_awal()


def tutup_database():
    koneksi.close()


def buat_tabel():
    kursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role     TEXT NOT NULL,
            saldo    INTEGER NOT NULL DEFAULT 0
        )
    """)
    kursor.execute("""
        CREATE TABLE IF NOT EXISTS data_hp (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            penjual TEXT NOT NULL,
            merk    TEXT NOT NULL,
            tipe    TEXT NOT NULL,
            kondisi TEXT NOT NULL,
            harga   INTEGER NOT NULL,
            status  TEXT NOT NULL DEFAULT 'Tersedia'
        )
    """)
    kursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            no      INTEGER PRIMARY KEY AUTOINCREMENT,
            id_hp   INTEGER NOT NULL,
            nama_hp TEXT NOT NULL,
            penjual TEXT NOT NULL,
            pembeli TEXT NOT NULL,
            harga   INTEGER NOT NULL,
            jenis   TEXT NOT NULL,
            metode  TEXT NOT NULL DEFAULT '-'
        )
    """)
    koneksi.commit()


def isi_data_awal():
    kursor.execute("SELECT COUNT(*) FROM users")
    if kursor.fetchone()[0] == 0:
        kursor.executemany(
            "INSERT INTO users (username, password, role, saldo) VALUES (?, ?, ?, ?)",
            [
                ("admin", "admin123", "Admin", 0),
                ("pahri", "123", "Pengguna Biasa", 0),
                ("sari", "123", "Pengguna Biasa", 0),
            ],
        )
        kursor.executemany(
            "INSERT INTO data_hp (penjual, merk, tipe, kondisi, harga, status) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("budi", "Samsung", "Galaxy A52", "Baik", 2500000, "Tersedia"),
                ("sari", "Xiaomi", "Redmi Note 10", "Mulus", 1800000, "Tersedia"),
            ],
        )
        koneksi.commit()


# ---------- ALAT BANTU ----------
def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def cek_angka(teks):
    if teks == "":
        return False
    for huruf in teks:
        if huruf not in "0123456789":
            return False
    return True


def format_rupiah(angka):
    if angka < 1000:
        return str(angka)
    sisa = str(angka % 1000)
    while len(sisa) < 3:
        sisa = "0" + sisa
    return format_rupiah(angka // 1000) + "." + sisa


# ---------- USER ----------
def cek_login(username, password):
    # mengembalikan data user, atau None kalau salah
    kursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    return kursor.fetchone()


def register_user(username, password):
    if username == "" or " " in username:
        raise ValueError("Username tidak boleh kosong atau mengandung spasi!")
    kursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if kursor.fetchone() is not None:
        raise ValueError("Username sudah dipakai!")
    if len(password) < 10:
        raise ValueError("Password minimal 10 karakter!")
    kursor.execute(
        "INSERT INTO users (username, password, role, saldo) "
        "VALUES (?, ?, 'Pengguna Biasa', 0)",
        (username, password),
    )
    koneksi.commit()


def ambil_semua_user():
    kursor.execute("SELECT username, role, saldo FROM users")
    return kursor.fetchall()


def hapus_user(username):
    kursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    target = kursor.fetchone()
    if target is None:
        raise KeyError(username)
    if target["role"] == "Admin":
        raise ValueError("Akun Admin tidak boleh dihapus!")
    kursor.execute("DELETE FROM users WHERE username = ?", (username,))
    kursor.execute("DELETE FROM data_hp WHERE penjual = ?", (username,))
    koneksi.commit()


# ---------- SALDO ----------
def ambil_saldo(username):
    kursor.execute("SELECT saldo FROM users WHERE username = ?", (username,))
    baris = kursor.fetchone()
    if baris is None:
        return 0
    return baris["saldo"]


def ambil_role(username):
    kursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    baris = kursor.fetchone()
    if baris is None:
        return ""
    return baris["role"]


def top_up(username, nominal_input):
    if not cek_angka(nominal_input):
        raise ValueError("Nominal harus berupa angka bulat positif!")
    nominal = int(nominal_input)
    if nominal < 10000:
        raise ValueError("Top up minimal Rp 10.000!")
    if nominal > 10000000:
        raise ValueError("Top up maksimal Rp 10.000.000!")

    kursor.execute("UPDATE users SET saldo = saldo + ? WHERE username = ?",
                   (nominal, username))
    catat_transaksi(0, "Top Up Saldo", "-", username, nominal, "Top Up", "-")
    koneksi.commit()
    return ambil_saldo(username)


# ---------- HP ----------
def hitung_hp_tersedia():
    kursor.execute("SELECT COUNT(*) FROM data_hp WHERE status = 'Tersedia'")
    return kursor.fetchone()[0]


def ambil_hp(id_hp):
    kursor.execute("SELECT * FROM data_hp WHERE id = ?", (id_hp,))
    baris = kursor.fetchone()
    if baris is None:
        raise KeyError(id_hp)
    return baris


def cari_hp(kata_cari):
    kursor.execute(
        "SELECT * FROM data_hp WHERE LOWER(merk) LIKE ? ORDER BY id",
        ("%" + kata_cari + "%",),
    )
    return kursor.fetchall()


def catat_transaksi(id_hp, nama_hp, penjual, pembeli, harga, jenis, metode):
    kursor.execute(
        "INSERT INTO transaksi (id_hp, nama_hp, penjual, pembeli, harga, jenis, metode) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (id_hp, nama_hp, penjual, pembeli, harga, jenis, metode),
    )


def tambah_hp(penjual, merk, tipe, kondisi, harga):
    if merk == "" or tipe == "":
        raise ValueError("Merk dan tipe tidak boleh kosong!")
    if kondisi not in daftar_kondisi:
        raise ValueError("Kondisi harus 1, 2, atau 3!")
    if not cek_angka(harga):
        raise ValueError("Harga harus berupa angka bulat positif!")
    harga_angka = int(harga)
    if harga_angka <= 0:
        raise ValueError("Harga harus lebih dari 0!")

    kursor.execute(
        "INSERT INTO data_hp (penjual, merk, tipe, kondisi, harga, status) "
        "VALUES (?, ?, ?, ?, ?, 'Tersedia')",
        (penjual, merk, tipe, daftar_kondisi[kondisi], harga_angka),
    )
    id_baru = kursor.lastrowid
    catat_transaksi(id_baru, merk + " " + tipe, penjual, "-", harga_angka, "Dijual", "-")
    koneksi.commit()
    return id_baru


def cek_boleh_ubah(id_hp, nama_aktif, role):
    hp = ambil_hp(id_hp)
    if role != "Admin" and hp["penjual"] != nama_aktif:
        raise ValueError("Anda hanya boleh mengubah HP milik sendiri!")
    if hp["status"] == "Terjual":
        raise ValueError("HP yang sudah terjual tidak bisa diubah!")
    return hp


def ubah_hp(id_hp, merk_baru, tipe_baru, kondisi_baru, harga_baru):
    # input kosong = tidak diubah
    if kondisi_baru != "" and kondisi_baru not in daftar_kondisi:
        raise ValueError("Kondisi harus 1, 2, atau 3!")
    if harga_baru != "":
        if not cek_angka(harga_baru):
            raise ValueError("Harga harus berupa angka bulat positif!")
        if int(harga_baru) <= 0:
            raise ValueError("Harga harus lebih dari 0!")

    if merk_baru != "":
        kursor.execute("UPDATE data_hp SET merk = ? WHERE id = ?", (merk_baru, id_hp))
    if tipe_baru != "":
        kursor.execute("UPDATE data_hp SET tipe = ? WHERE id = ?", (tipe_baru, id_hp))
    if kondisi_baru != "":
        kursor.execute("UPDATE data_hp SET kondisi = ? WHERE id = ?",
                       (daftar_kondisi[kondisi_baru], id_hp))
    if harga_baru != "":
        kursor.execute("UPDATE data_hp SET harga = ? WHERE id = ?",
                       (int(harga_baru), id_hp))
    koneksi.commit()


def cek_boleh_hapus(id_hp, nama_aktif, role):
    hp = ambil_hp(id_hp)
    if role != "Admin" and hp["penjual"] != nama_aktif:
        raise ValueError("Anda hanya boleh menghapus HP milik sendiri!")
    return hp


def hapus_hp(id_hp):
    kursor.execute("DELETE FROM data_hp WHERE id = ?", (id_hp,))
    koneksi.commit()


def daftar_hp_untuk_dibeli(nama_aktif):
    kursor.execute(
        "SELECT * FROM data_hp WHERE status = 'Tersedia' AND penjual != ? ORDER BY id",
        (nama_aktif,),
    )
    return kursor.fetchall()


def cek_boleh_beli(id_hp, nama_aktif):
    hp = ambil_hp(id_hp)
    if hp["penjual"] == nama_aktif:
        raise ValueError("Anda tidak bisa membeli HP sendiri!")
    if hp["status"] == "Terjual":
        raise ValueError("HP sudah terjual!")
    # Admin tidak perlu cek saldo
    if ambil_role(nama_aktif) != "Admin":
        saldo = ambil_saldo(nama_aktif)
        if saldo < hp["harga"]:
            raise ValueError("Saldo tidak cukup! Kurang Rp " +
                             format_rupiah(hp["harga"] - saldo))
    return hp


def beli_hp(id_hp, pembeli):
    hp = cek_boleh_beli(id_hp, pembeli)
    kursor.execute("UPDATE data_hp SET status = 'Terjual' WHERE id = ?", (id_hp,))

    if ambil_role(pembeli) == "Admin":
        metode = "Dibeli Admin"
    else:
        metode = "Saldo"
        # saldo pembeli berkurang (khusus pengguna biasa)
        kursor.execute("UPDATE users SET saldo = saldo - ? WHERE username = ?",
                       (hp["harga"], pembeli))

    # saldo penjual selalu bertambah
    kursor.execute("UPDATE users SET saldo = saldo + ? WHERE username = ?",
                   (hp["harga"], hp["penjual"]))
    catat_transaksi(id_hp, hp["merk"] + " " + hp["tipe"],
                    hp["penjual"], pembeli, hp["harga"], "Terjual", metode)
    koneksi.commit()


# ---------- TRANSAKSI ----------
def ambil_transaksi(nama_aktif, role):
    if role == "Admin":
        kursor.execute("SELECT * FROM transaksi ORDER BY no")
    else:
        kursor.execute(
            "SELECT * FROM transaksi WHERE penjual = ? OR pembeli = ? ORDER BY no",
            (nama_aktif, nama_aktif),
        )
    return kursor.fetchall()


# ======================================================
# LAYAR YANG DIPAKAI BERSAMA (Admin & Pengguna Biasa)
# ======================================================
def tampil_jual_hp(nama_aktif):
    bersihkan_layar()
    tampil_judul("JUAL HP")
    merk = tanya("Merk          : ")
    tipe = tanya("Tipe          : ")
    console.print("Kondisi : [bold yellow]1[/] Mulus   [bold yellow]2[/] Baik   [bold yellow]3[/] Minus")
    kondisi = tanya("Pilih kondisi : ")
    harga = tanya("Harga (Rp)    : ")
    try:
        id_baru = tambah_hp(nama_aktif, merk, tipe, kondisi, harga)
    except ValueError as pesan_error:
        cetak_error(str(pesan_error))
    else:
        cetak_sukses("HP berhasil didaftarkan dengan ID [bold]" + str(id_baru) + "[/]")
    finally:
        tunggu()


def tampil_lihat_hp():
    bersihkan_layar()
    tampil_judul("LIHAT / CARI HP")
    tampil_menu([("1", "Tampilkan semua"), ("2", "Cari berdasarkan merk")])
    sub = tanya("Pilih : ")
    if sub != "1" and sub != "2":
        cetak_error("Pilihan tidak tersedia!")
    else:
        kata = ""
        if sub == "2":
            kata = tanya("Masukkan merk : ").lower()
        hasil = cari_hp(kata)
        if len(hasil) == 0:
            cetak_info("Data HP tidak ditemukan.")
        else:
            tabel_hp(hasil, "Daftar HP")
            console.print("Jumlah data : [bold]" + str(len(hasil)) + "[/]")
    tunggu()


def tampil_ubah_hp(nama_aktif, role_aktif):
    bersihkan_layar()
    tampil_judul("UBAH DATA HP", "yellow")
    id_input = tanya("Masukkan ID HP yang ingin diubah : ")
    try:
        if not cek_angka(id_input):
            raise ValueError("ID harus berupa angka!")
        id_hp = int(id_input)
        hp = cek_boleh_ubah(id_hp, nama_aktif, role_aktif)

        console.print("Data lama : [bold]" + aman(hp["merk"]) + " " + aman(hp["tipe"]) +
                      "[/] | " + hp["kondisi"] + " | [green]Rp " +
                      format_rupiah(hp["harga"]) + "[/]")
        cetak_info("Kosongkan input jika tidak ingin mengubah")
        merk_baru = tanya("Merk baru    : ")
        tipe_baru = tanya("Tipe baru    : ")
        console.print("Kondisi : [bold yellow]1[/] Mulus   [bold yellow]2[/] Baik   [bold yellow]3[/] Minus")
        kondisi_baru = tanya("Kondisi baru : ")
        harga_baru = tanya("Harga baru   : ")

        ubah_hp(id_hp, merk_baru, tipe_baru, kondisi_baru, harga_baru)
    except ValueError as pesan_error:
        cetak_error(str(pesan_error))
    except KeyError:
        cetak_error("ID tidak ditemukan!")
    else:
        cetak_sukses("Data HP berhasil diubah.")
    finally:
        tunggu()


def tampil_hapus_hp(nama_aktif, role_aktif):
    bersihkan_layar()
    tampil_judul("HAPUS HP", "red")
    id_input = tanya("Masukkan ID HP yang ingin dihapus : ")
    try:
        if not cek_angka(id_input):
            raise ValueError("ID harus berupa angka!")
        id_hp = int(id_input)
        cek_boleh_hapus(id_hp, nama_aktif, role_aktif)

        yakin = tanya("Yakin ingin menghapus? (Y/T) : ").upper()
        if yakin != "Y" and yakin != "T":
            raise ValueError("Pilihan harus Y atau T!")
    except ValueError as pesan_error:
        cetak_error(str(pesan_error))
    except KeyError:
        cetak_error("ID tidak ditemukan!")
    else:
        if yakin == "Y":
            hapus_hp(id_hp)
            cetak_sukses("Data HP berhasil dihapus.")
        else:
            cetak_info("Penghapusan dibatalkan.")
    finally:
        tunggu()


def tampil_riwayat(nama_aktif, role_aktif):
    bersihkan_layar()
    tampil_judul("RIWAYAT TRANSAKSI")
    hasil = ambil_transaksi(nama_aktif, role_aktif)
    if len(hasil) == 0:
        cetak_info("Belum ada transaksi.")
    else:
        tabel = Table(box=box.ROUNDED, header_style="bold cyan")
        tabel.add_column("ID HP", justify="right")
        tabel.add_column("Nama HP")
        tabel.add_column("Penjual")
        tabel.add_column("Pembeli")
        tabel.add_column("Harga", justify="right", style="green")
        tabel.add_column("Jenis")
        tabel.add_column("Metode")
        for t in hasil:
            if t["jenis"] == "Dijual":
                jenis = "[yellow]Dijual[/]"
            elif t["jenis"] == "Terjual":
                jenis = "[green]Terjual[/]"
            else:
                jenis = "[cyan]" + t["jenis"] + "[/]"
            tabel.add_row(str(t["id_hp"]), aman(t["nama_hp"]), aman(t["penjual"]),
                          aman(t["pembeli"]), "Rp " + format_rupiah(t["harga"]),
                          jenis, t["metode"])
        console.print(tabel)
    tunggu()


def tampil_beli_hp(nama_aktif, role_aktif):
    bersihkan_layar()
    tampil_judul("BELI HP", "green")
    if role_aktif != "Admin":
        console.print("Saldo Anda : [bold green]Rp " +
                      format_rupiah(ambil_saldo(nama_aktif)) + "[/]")
    daftar_beli = daftar_hp_untuk_dibeli(nama_aktif)

    if len(daftar_beli) == 0:
        cetak_info("Belum ada HP yang bisa dibeli.")
    else:
        tabel_hp(daftar_beli, "HP yang tersedia", False)
        id_input = tanya("Masukkan ID HP yang ingin dibeli : ")
        try:
            if not cek_angka(id_input):
                raise ValueError("ID harus berupa angka!")
            id_hp = int(id_input)
            hp = cek_boleh_beli(id_hp, nama_aktif)

            console.print("Harga HP : [bold green]Rp " + format_rupiah(hp["harga"]) + "[/]")
            yakin = tanya("Yakin ingin membeli? (Y/T) : ").upper()
            if yakin != "Y" and yakin != "T":
                raise ValueError("Pilihan harus Y atau T!")
        except ValueError as pesan_error:
            cetak_error(str(pesan_error))
        except KeyError:
            cetak_error("ID tidak ditemukan!")
        else:
            if yakin == "Y":
                beli_hp(id_hp, nama_aktif)
                cetak_sukses("Pembelian berhasil!")
                if role_aktif != "Admin":
                    console.print("Sisa saldo : [bold green]Rp " +
                                  format_rupiah(ambil_saldo(nama_aktif)) + "[/]")
                else:
                    console.print("Saldo penjual [bold]" + aman(hp["penjual"]) +
                                  "[/] bertambah [bold green]Rp " +
                                  format_rupiah(hp["harga"]) + "[/]")
            else:
                cetak_info("Pembelian dibatalkan.")
    tunggu()