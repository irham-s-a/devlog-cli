# devlog-cli

> Track your daily dev progress right from the terminal.
> Catat progress harianmu langsung dari terminal.

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![by irham-s-a](https://img.shields.io/badge/by-irham--s--a-orange)

---

## 🇮🇩 Bahasa Indonesia

`devlog-cli` adalah tool CLI untuk developer mencatat progress harian, blocker, dan catatan langsung dari terminal — tanpa perlu buka Notion atau aplikasi lain.

### Instalasi

```bash
git clone https://github.com/irham-s-a/devlog-cli.git
cd devlog-cli
pip install -e .
```

### Bahasa

Output perintah **info** (list, stats, export) secara default ditampilkan dalam **Bahasa Inggris**.  
Gunakan flag **`-idn`** untuk menampilkan dalam **Bahasa Indonesia**.  
Perintah **aksi** (add, tambah, delete, hapus) otomatis mengikuti bahasa perintah — tidak perlu `-idn`.

### Cara Pakai

**Tambah entri log:**
```bash
devlog add "Fix bug login" --tag bug
devlog tambah "Selesai modul auth" --tag feature
```

**Lihat daftar log:**
```bash
devlog list                        # log hari ini (English)
devlog list -idn                   # log hari ini (Bahasa Indonesia)
devlog list --week                 # log minggu ini (English)
devlog list --week -idn            # log minggu ini (Bahasa Indonesia)
devlog list --all                  # semua log (English)
devlog list --all -idn             # semua log (Bahasa Indonesia)
devlog list --tag bug              # filter berdasarkan tag (English)
devlog list --tag bug -idn         # filter berdasarkan tag (Bahasa Indonesia)
```

**Export log ke Markdown:**
```bash
devlog export                      # export hari ini (English)
devlog export -idn                 # export hari ini (Bahasa Indonesia)
devlog export --period week        # export minggu ini (English)
devlog export --period week -idn   # export minggu ini (Bahasa Indonesia)
devlog export -o catatanku.md      # export ke file kustom
```

**Hapus entri:**
```bash
devlog delete 3                    # hapus entri berdasarkan ID (English)
devlog hapus 3                     # hapus entri berdasarkan ID (Bahasa Indonesia)
```

**Lihat statistik:**
```bash
devlog stats                       # statistik dev log (English)
devlog stats -idn                  # statistik dev log (Bahasa Indonesia)
devlog statistik -idn              # sama, dengan perintah Indonesia
```

### Teknologi

- Python 3.10+
- [Click](https://click.palletsprojects.com/) — framework CLI
- [Rich](https://rich.readthedocs.io/) — tampilan terminal
- SQLite — database lokal
- pytest — testing

### Kontribusi

Pull request dan issue sangat diterima! Silakan fork repo ini dan buat branch baru untuk fitur atau perbaikan.

---

## 🇬🇧 English

`devlog-cli` is a CLI tool for developers to track daily progress, blockers, and notes right from the terminal — no need to open Notion or other apps.

### Installation

```bash
git clone https://github.com/irham-s-a/devlog-cli.git
cd devlog-cli
pip install -e .
```

### Language

**Info commands** (list, stats, export) display output in **English by default**.  
Use the **`-idn`** flag to display in **Indonesian (Bahasa Indonesia)**.  
**Action commands** (add, tambah, delete, hapus) follow the command language — no `-idn` needed.

### Usage

**Add a log entry:**
```bash
devlog add "Fix login bug" --tag bug
devlog tambah "Selesai modul auth" --tag feature
```

**List log entries:**
```bash
devlog list                        # today's log (English, default)
devlog list -idn                   # today's log (Indonesian)
devlog list --week                 # this week's log (English)
devlog list --week -idn            # this week's log (Indonesian)
devlog list --all                  # all logs (English)
devlog list --all -idn             # all logs (Indonesian)
devlog list --tag bug              # filter by tag (English)
devlog list --tag bug -idn         # filter by tag (Indonesian)
```

**Export log to Markdown:**
```bash
devlog export                      # export today (English)
devlog export -idn                 # export today (Indonesian)
devlog export --period week        # export this week (English)
devlog export --period week -idn   # export this week (Indonesian)
devlog export -o mylog.md          # export to custom file
```

**Delete an entry:**
```bash
devlog delete 3                    # delete entry by ID (English)
devlog hapus 3                     # delete entry by ID (Indonesian)
```

**View statistics:**
```bash
devlog stats                       # dev log statistics (English)
devlog stats -idn                  # dev log statistics (Indonesian)
devlog statistik -idn              # same, with Indonesian command
```

### Tech Stack

- Python 3.10+
- [Click](https://click.palletsprojects.com/) — CLI framework
- [Rich](https://rich.readthedocs.io/) — terminal formatting
- SQLite — local database
- pytest — testing

### Contributing

Pull requests and issues are welcome! Feel free to fork this repo and create a new branch for features or fixes.

---

Made with ❤️ by [irham-s-a](https://github.com/irham-s-a)
