import datetime

inventaris = {
    "laptop": {"stok": 10, "harga": 15000000},
    "mouse": {"stok": 20, "harga": 200000},
    "keyboard": {"stok": 15, "harga": 500000},
    "headset": {"stok": 25, "harga": 300000}
}

denda_per_hari = 5000
peminjaman_log = {}

def input_tanggal(keterangan):
    while True:
        try:
            print(f"\nMasukkan {keterangan}:")
            hari = int(input("Hari (1-31): "))
            bulan = int(input("Bulan (1-12): "))
            tahun = int(input("Tahun (contoh: 2024): "))
            tanggal = datetime.date(tahun, bulan, hari)
            return tanggal
        except ValueError:
            print("Tanggal tidak valid. Silakan masukkan kembali.")

def tampilkan_barang():
    for barang, data in inventaris.items():
        print(f"{barang}: {data['stok']} unit (Harga: Rp {data['harga']})")

def tambah_barang():
    nama_barang = input("Masukkan nama barang baru: ")
    jumlah = int(input("Masukkan jumlah barang: "))
    harga = int(input("Masukkan harga barang: "))
    if nama_barang in inventaris:
        print("Barang sudah ada. Stok akan ditambahkan.")
        inventaris[nama_barang]["stok"] += jumlah
    else:
        inventaris[nama_barang] = {"stok": jumlah, "harga": harga}
    print(f"Barang '{nama_barang}' berhasil ditambahkan/diupdate.")

def hapus_barang():
    nama_barang = input("Masukkan nama barang yang ingin dihapus: ")
    if nama_barang in inventaris:
        del inventaris[nama_barang]
        print(f"Barang '{nama_barang}' berhasil dihapus.")
    else:
        print("Barang tidak ditemukan.")


def pinjam_barang():
    print("\n=== Pinjam Barang ===")
    nama_barang = input("Nama barang yang ingin dipinjam: ").lower()
    if nama_barang in inventaris:
        jumlah = int(input("Jumlah yang ingin dipinjam: "))
        if jumlah <= inventaris[nama_barang]["stok"]:
            inventaris[nama_barang]["stok"] -= jumlah
            tanggal_pinjam = input_tanggal("tanggal pinjam")
            peminjaman_log[nama_barang] = {"jumlah": jumlah, "tanggal_pinjam": tanggal_pinjam}
            print(f"Berhasil meminjam {jumlah} unit '{nama_barang}' pada {tanggal_pinjam}.")
        else:
            print("Stok tidak mencukupi.")
    else:
        print("Barang tidak ditemukan.")


def update_pinjaman():
    print("\n=== Update Pinjaman Barang ===")
    nama_barang = input("Masukkan nama barang yang ingin diupdate: ").lower()

    if nama_barang in peminjaman_log:
        print("Apakah Anda ingin menambahkan atau mengurangi jumlah pinjaman?")
        pilihan = input("Ketik 'tambah' untuk menambahkan atau 'kurang' untuk mengurangi: ").lower()

        if pilihan == "tambah":
            jumlah_tambahan = int(input("Masukkan jumlah tambahan yang ingin dipinjam: "))
            if jumlah_tambahan <= inventaris[nama_barang]["stok"]:
                inventaris[nama_barang]["stok"] -= jumlah_tambahan
                peminjaman_log[nama_barang]["jumlah"] += jumlah_tambahan
                jumlah_baru = peminjaman_log[nama_barang]["jumlah"]
                print(f"Jumlah pinjaman '{nama_barang}' berhasil diperbarui menjadi {jumlah_baru}.")
            else:
                print("Stok tidak mencukupi untuk penambahan jumlah pinjaman.")
        
        elif pilihan == "kurang":
            jumlah_pengurangan = int(input("Masukkan jumlah yang ingin dikurangi dari pinjaman: "))
            jumlah_awal = peminjaman_log[nama_barang]["jumlah"]

            if jumlah_pengurangan > jumlah_awal:
                print("Jumlah pengurangan melebihi jumlah pinjaman yang ada.")
            else:
                peminjaman_log[nama_barang]["jumlah"] -= jumlah_pengurangan
                inventaris[nama_barang]["stok"] += jumlah_pengurangan
                jumlah_baru = peminjaman_log[nama_barang]["jumlah"]
                print(f"Jumlah pinjaman '{nama_barang}' berhasil diperbarui menjadi {jumlah_baru}.")
        else:
            print("Pilihan tidak valid. Silakan pilih 'tambah' atau 'kurang'.")
    else:
        print("Barang tidak ditemukan dalam daftar peminjaman.")


def kembalikan_barang():
    print("\n=== Kembalikan Barang ===")
    nama_barang = input("Nama barang yang ingin dikembalikan: ").lower()
    if nama_barang not in peminjaman_log:
        print("Barang tidak terdaftar dalam peminjaman.")
        return

    jumlah = int(input("Jumlah yang ingin dikembalikan: "))
    if jumlah > peminjaman_log[nama_barang]["jumlah"]:
        print("Jumlah yang dikembalikan melebihi jumlah yang dipinjam.")
        return

    tanggal_kembali = input_tanggal("tanggal kembali")
    tanggal_pinjam = peminjaman_log[nama_barang]["tanggal_pinjam"]

    selisih_hari = (tanggal_kembali - tanggal_pinjam).days
    hari_terlambat = max(0, selisih_hari - 7)
    denda_harian = hari_terlambat * denda_per_hari

    inventaris[nama_barang]["stok"] += jumlah
    
    konfirmasi_rusak = input("Apakah ada barang yang rusak? (ya/tidak): ").lower()
    if konfirmasi_rusak == "ya":
        jumlah_rusak = int(input("Jumlah barang yang rusak: "))
        if jumlah_rusak > jumlah or jumlah_rusak < 0:
            print("Jumlah barang rusak tidak valid.")
            return
        denda_kerusakan = inventaris[nama_barang]["harga"] * jumlah_rusak
    else:
        jumlah_rusak = 0
        denda_kerusakan = 0

    total_denda = denda_harian + denda_kerusakan

    if total_denda > 0:
        print(f"\nTotal denda yang harus dibayar: Rp {total_denda:,}.")
        print(f"  - Denda keterlambatan: Rp {denda_harian:,}")
        if jumlah_rusak > 0:
            print(f"  - Denda kerusakan ({jumlah_rusak} unit): Rp {denda_kerusakan:,}")
    else:
        print("\nTidak ada denda yang harus dibayar.")

    if jumlah == peminjaman_log[nama_barang]["jumlah"]:
        del peminjaman_log[nama_barang]
    else:
        peminjaman_log[nama_barang]["jumlah"] -= jumlah


def menu():
    while True:
        print("==================================")
        print("====SELAMAT DATANG DITOKO KAMI====")
        print("==================================")
        print("\n=== Menu Utama ===")
        print("1. Tampilkan Barang")
        print("2. Tambah Barang")
        print("3. Hapus Barang")
        print("4. Pinjam Barang")
        print("5. Update Peminjaman")
        print("6. Kembalikan Barang")
        print("7. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_barang()
        elif pilihan == "2":
            tambah_barang()
        elif pilihan == "3":
            hapus_barang()
        elif pilihan == "4":
            pinjam_barang()
        elif pilihan == "5":
            update_pinjaman()
        elif pilihan == "6":
            kembalikan_barang()
        elif pilihan == "7":
            print("Terima kasih telah meminjam barang.")
            break
        else:
            print("Pilihan tidak ada. Silakan coba lagi.")

menu()






