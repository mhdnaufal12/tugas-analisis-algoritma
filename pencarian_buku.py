"""
Tugas 1 - Analisis Algoritma Pencarian Buku
Cara menjalankan:
  python pencarian_buku.py --csv books.csv
Jika nama file berbeda:
  python pencarian_buku.py --csv "nama_dataset.csv"

Program membaca CSV, memilih kolom judul secara otomatis, lalu membandingkan
Linear Search dan Binary Search berdasarkan judul buku. Binary Search memakai
salinan data yang diurutkan berdasarkan judul.
"""
import argparse
import csv
import random
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    """Menyimpan hasil pencarian dan jumlah perbandingan."""
    book: dict | None
    comparisons: int


def normalize(value):
    """Membuat teks seragam agar pencarian tidak peka huruf besar/kecil."""
    return str(value or "").strip().casefold()


def load_books(csv_path):
    """Membaca seluruh baris CSV dan mengembalikannya sebagai list of dict."""
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV tidak memiliki header kolom.")
        rows = [dict(row) for row in reader]
    if not rows:
        raise ValueError("Dataset CSV kosong.")
    return rows


def find_title_column(books):
    """Menentukan kolom judul dengan nama kolom yang umum digunakan."""
    columns = list(books[0].keys())
    preferred = ("title", "book title", "name", "judul")
    for wanted in preferred:
        for column in columns:
            if normalize(column) == wanted:
                return column
    # Jika nama kolom tidak umum, gunakan kolom pertama sebagai fallback.
    return columns[0]


def linear_search(books, title, title_column):
    """Mencari judul dari awal hingga akhir; tidak memakai pencarian bawaan."""
    target = normalize(title)
    comparisons = 0
    for book in books:
        comparisons += 1
        if normalize(book.get(title_column, "")) == target:
            return SearchResult(book, comparisons)
    return SearchResult(None, comparisons)


def binary_search(sorted_books, title, title_column):
    """Binary Search iteratif; data wajib terurut berdasarkan judul."""
    target = normalize(title)
    low = 0
    high = len(sorted_books) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        current = normalize(sorted_books[mid].get(title_column, ""))
        comparisons += 1
        if current == target:
            return SearchResult(sorted_books[mid], comparisons)
        if current < target:
            low = mid + 1
        else:
            high = mid - 1
    return SearchResult(None, comparisons)


def print_result(label, result):
    """Menampilkan status, atribut buku, dan jumlah perbandingan."""
    print(f"\n{label}")
    if result.book is None:
        print("Buku tidak ditemukan.")
    else:
        for key, value in result.book.items():
            print(f"{key}: {value}")
    print(f"Jumlah perbandingan: {result.comparisons}")


def benchmark(books, title_column):
    """Uji n=100, 1.000, 10.000 (sebatas ukuran dataset yang tersedia)."""
    print("\n=== BENCHMARK ===")
    print(f"{'n':>7} {'Algoritma':<16} {'Skenario':<18} {'Perbandingan':>14} {'Waktu (ms)':>12}")
    sorted_all = sorted(books, key=lambda b: normalize(b.get(title_column, "")))
    for n in (100, 1000, 10000):
        if len(books) < n:
            print(f"Catatan: dataset hanya memiliki {len(books)} baris; n={n} dilewati.")
            continue
        sample = books[:n]
        sorted_sample = sorted(sample, key=lambda b: normalize(b.get(title_column, "")))
        targets = [
            ("awal", sample[0].get(title_column, "")),
            ("tengah", sample[n // 2].get(title_column, "")),
            ("akhir", sample[-1].get(title_column, "")),
            ("tidak ditemukan", "__judul_yang_tidak_ada_928374__"),
        ]
        sorted_targets = [
            ("awal", sorted_sample[0].get(title_column, "")),
            ("tengah", sorted_sample[n // 2].get(title_column, "")),
            ("akhir", sorted_sample[-1].get(title_column, "")),
            ("tidak ditemukan", "__judul_yang_tidak_ada_928374__"),
        ]
        for scenario, target in targets:
            start = time.perf_counter()
            result = linear_search(sample, target, title_column)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"{n:7} {'Linear Search':<16} {scenario:<18} {result.comparisons:14} {elapsed:12.4f}")
        for scenario, target in sorted_targets:
            start = time.perf_counter()
            result = binary_search(sorted_sample, target, title_column)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"{n:7} {'Binary Search':<16} {scenario:<18} {result.comparisons:14} {elapsed:12.4f}")


def main():
    parser = argparse.ArgumentParser(description="Pencarian buku dengan Linear dan Binary Search.")
    parser.add_argument("--csv", default="books.csv", help="Lokasi file dataset CSV.")
    args = parser.parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(
            f"File '{csv_path}' tidak ditemukan. Unduh dataset Kaggle, ekstrak CSV, "
            "lalu jalankan ulang dengan --csv nama_file.csv."
        )

    books = load_books(csv_path)
    title_column = find_title_column(books)
    sorted_books = sorted(books, key=lambda b: normalize(b.get(title_column, "")))

    print(f"Jumlah data: {len(books)}")
    print(f"Kolom judul yang dipakai: {title_column}")
    query = input("Masukkan judul buku yang dicari: ")

    print_result("=== LINEAR SEARCH ===", linear_search(books, query, title_column))
    print_result("=== BINARY SEARCH ===", binary_search(sorted_books, query, title_column))
    benchmark(books, title_column)


if __name__ == "__main__":
    main()
