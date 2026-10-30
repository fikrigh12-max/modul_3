
import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        self.selected_id = None

        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        # Menghubungkan tombol dengan fungsi
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_logout.configure(command=self.logout)

        # Memilih data dari tabel
        self.view.tabel.bind(
            "<<TreeviewSelect>>", self.pilih_data
        )

        # Hak akses anggota
        if self.user_role != "admin":
            self.view.btn_simpan.configure(
                state="disabled",
                text="Akses Terkunci (Khusus Admin)"
            )
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    # MENAMPILKAN DATA BUKU
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["penulis"],
                    buku["tahun_terbit"]
                )
            )

    # MEMILIH DATA DARI TABEL
    def pilih_data(self, event):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            return

        data = self.view.tabel.item(pilihan[0], "values")

        self.selected_id = data[0]

        # Mengosongkan form
        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")

        # Memasukkan data ke form
        self.view.entry_judul.insert(0, data[1])
        self.view.entry_penulis.insert(0, data[2])
        self.view.entry_tahun.insert(0, data[3])

    # MENYIMPAN DATA BUKU
    def simpan_data(self):
        if self.user_role != "admin":
            messagebox.showwarning(
                "Akses Ditolak",
                "Hanya admin yang dapat menambahkan buku."
            )
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        if not tahun.isdigit():
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!"
            )
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil disimpan."
            )

            self.kosongkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Gagal",
                "Data buku gagal disimpan."
            )

    # MEMPERBARUI DATA BUKU
    def update_data(self):
        if self.user_role != "admin":
            messagebox.showwarning(
                "Akses Ditolak",
                "Hanya admin yang dapat memperbarui data."
            )
            return

        if self.selected_id is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku dari tabel terlebih dahulu!"
            )
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        if not tahun.isdigit():
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!"
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah kamu yakin ingin memperbarui data buku ini?"
        )

        if konfirmasi:
            berhasil = self.model.update_buku(
                self.selected_id,
                judul,
                penulis,
                tahun
            )

            if berhasil:
                messagebox.showinfo(
                    "Berhasil",
                    "Data buku berhasil diperbarui."
                )

                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror(
                    "Gagal",
                    "Data buku gagal diperbarui."
                )

    # MENGHAPUS DATA BUKU
    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showwarning(
                "Akses Ditolak",
                "Hanya admin yang dapat menghapus data."
            )
            return

        if self.selected_id is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku dari tabel terlebih dahulu!"
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            "Apakah kamu yakin ingin menghapus data buku ini?"
        )

        if konfirmasi:
            berhasil = self.model.delete_buku(self.selected_id)

            if berhasil:
                messagebox.showinfo(
                    "Berhasil",
                    "Data buku berhasil dihapus."
                )

                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror(
                    "Gagal",
                    "Data buku gagal dihapus."
                )

    # MENGOSONGKAN FORM
    def kosongkan_form(self):
        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")

        self.selected_id = None

        for item in self.view.tabel.selection():
            self.view.tabel.selection_remove(item)

    # LOGOUT
    def logout(self):
        konfirmasi = messagebox.askyesno(
            "Logout",
            "Apakah kamu yakin ingin keluar?"
        )

        if konfirmasi:
            self.view.destroy()

            from controllers.auth_controller import AuthController

            login = AuthController()
            login.run()

    # MENJALANKAN APLIKASI
    def run(self):
        self.view.mainloop()
