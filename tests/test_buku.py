from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True

    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()

    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_get_all_buku():
    # Menginisialisasi Model
    model = BukuModel()
    
    # Memanipulasi (Mock) koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    
    # Menentukan hasil kembalian (return value) palsu dari database
    mock_cursor.fetchall.return_value = [
        (1, "Belajar Python", "Admin", 2026),
        (2, "Pemrograman MVC", "Developer", 2026)
    ]
    
    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()
    
    # Memverifikasi apakah hasilnya sesuai (berupa list/data)
    assert hasil is not None
    assert len(hasil) == 2
    assert hasil[0][1] == "Belajar Python"
    
    # Memverifikasi apakah query execute dipanggil
    mock_cursor.execute.assert_called_once()