
import csv

file_asli = "Books.csv"
file_kecil = "Books_10000.csv"

with open(file_asli, "r", encoding="utf-8-sig", newline="") as sumber:
    pembaca = csv.reader(sumber)
    header = next(pembaca)

    with open(file_kecil, "w", encoding="utf-8", newline="") as tujuan:
        penulis = csv.writer(tujuan)
        penulis.writerow(header)

        for i, baris in enumerate(pembaca):
            if i >= 10000:
                break
            penulis.writerow(baris)

print("Berhasil! File Books_10000.csv sudah dibuat.")
