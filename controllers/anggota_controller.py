from models.anggota_model import AnggotaModel

class AnggotaController:
    def __init__(self, view):
        self.view = view
        self.model = AnggotaModel()
        self.load_data()
        self.init_ui()

    def load_data(self):
        data = self.model.get_all_anggota()
        # Masukkan data ke tabel anggota di view

    def init_ui(self):
        # Hubungkan tombol simpan, hapus, perbarui ke fungsi masing-masing
        pass