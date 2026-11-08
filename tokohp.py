
import os
import sqlite3

daftar_kondisi = {"1": "Mulus", "2": "Baik", "3": "Minus"}

koneksi = None
kursor = None



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
            role     TEXT NOT NULL
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
            jenis   TEXT NOT NULL
        )
    """)
    koneksi.commit()


def isi_data_awal():
    kursor.execute("SELECT COUNT(*) FROM users")
    if kursor.fetchone()[0] == 0:
        kursor.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            [
                ("admin", "admin123", "Admin"),
                ("pahri", "123", "Pengguna Biasa"),
                ("sari", "123", "Pengguna Biasa"),
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
    if len(password) < 3:
        raise ValueError("Password minimal 3 karakter!")
    kursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, 'Pengguna Biasa')",
        (username, password),
    )
    koneksi.commit()


def ambil_semua_user():
    kursor.execute("SELECT username, role FROM users")
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


def catat_transaksi(id_hp, nama_hp, penjual, pembeli, harga, jenis):
    kursor.execute(
        "INSERT INTO transaksi (id_hp, nama_hp, penjual, pembeli, harga, jenis) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (id_hp, nama_hp, penjual, pembeli, harga, jenis),
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
    catat_transaksi(id_baru, merk + " " + tipe, penjual, "-", harga_angka, "Dijual")
    koneksi.commit()
    return id_baru


def cek_boleh_ubah(id_hp, nama_aktif, role):
    # dipakai sebelum ubah: cek ID, kepemilikan, dan status
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
    return hp


def beli_hp(id_hp, pembeli):
    hp = cek_boleh_beli(id_hp, pembeli)
    kursor.execute("UPDATE data_hp SET status = 'Terjual' WHERE id = ?", (id_hp,))
    catat_transaksi(id_hp, hp["merk"] + " " + hp["tipe"],
                    hp["penjual"], pembeli, hp["harga"], "Terjual")
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