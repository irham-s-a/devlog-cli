# devlog-cli

> Catat progress harianmu langsung dari terminal.
> Track your daily dev progress right from the terminal.

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

### Cara Pakai

**Tambah entri log:**
```bash
devlog tambah "Selesai modul auth, masih stuck di refresh token"
devlog tambah "Fix bug login" --tag bug
```

**Lihat daftar log:**
```bash
devlog list                    # log hari ini (default)
devlog list --minggu           # log minggu ini
devlog list --semua            # semua log
devlog list --tag bug          # filter berdasarkan tag
```

**Export log ke Markdown:**
```bash
devlog export                  # export hari ini ke devlog-YYYY-MM-DD.md
devlog export --periode minggu # export log minggu ini
devlog export -o catatanku.md  # export ke file kustom
```

**Hapus entri:**
```bash
devlog hapus 3                 # hapus entri berdasarkan ID (ada konfirmasi)
```

**Lihat statistik:**
```bash
devlog statistik               # total entri, streak, tag terbanyak
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

### Usage

**Add a log entry:**
```bash
devlog tambah "Finished auth module, still stuck on refresh token"
devlog tambah "Fix login bug" --tag bug
```

**List log entries:**
```bash
devlog list                    # today's log (default)
devlog list --minggu           # this week's log
devlog list --semua            # all logs
devlog list --tag bug          # filter by tag
```

**Export log to Markdown:**
```bash
devlog export                  # export today to devlog-YYYY-MM-DD.md
devlog export --periode minggu # export this week's log
devlog export -o mylog.md      # export to custom file
```

**Delete an entry:**
```bash
devlog hapus 3                 # delete entry by ID (with confirmation)
```

**View statistics:**
```bash
devlog statistik               # total entries, streak, top tags
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
