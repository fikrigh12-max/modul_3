from models.anggota_model import AnggotaModel

anggota = AnggotaModel()

# Mengirimkan 3 parameter: id_anggota, nama, alamat
anggota.create_anggota("6", "Jaki", "Jl. Thamrin")
print("Data anggota berhasil ditambahkan!")

# Menampilkan daftar anggota terbaru
print("=== Daftar Anggota ===")
daftar_anggota = anggota.get_all_anggota()
for a in daftar_anggota:
    print(f"[{a['id_anggota']}] {a['nama']} - {a['alamat']}")