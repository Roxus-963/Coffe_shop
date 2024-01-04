import os
import time
import pandas as pd
import sys
from header import header_display
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import print as rich_print
from rich.prompt import Prompt
from pwinput import pwinput
'''
===================================================================
|                MOHON UNTUK MENGINSTALL MODULE                   |
|    [os, time, pandas, sys, rich, pwinput, dan colorama]         |
|     dan jalankan program ini di direktori yang berbeda          |
|                        TERIMAKASIH!                             |
===================================================================
|                Kekurangan dari program ini yaitu                |
|        pada input nama kopi, nama kopi terlalu sensitif         |
|        maka inputlah sesuai yang ada di dalam file csv!         |
===================================================================
'''
console = Console()

def get_bold_white_input(prompt):
    return console.input(f"[bold white]{prompt}[/]")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_currency(amount):
    return f"Rp.{amount:,.0f}"

def load_admin_data():
    try:
        admin_data = pd.read_csv('data_admin.csv')
        return admin_data
    except FileNotFoundError:
        console.print("Identitas Tidak Ditemukan!", style="bold red")
        exit()

def load_menu_kopi():
    try:
        menu_kopi = pd.read_csv('menu_kopi.csv')
        menu_kopi = menu_kopi.drop(columns=['Unnamed: 2'], errors='ignore')
        return menu_kopi
    except FileNotFoundError:
        console.print("File menu_kopi.csv tidak ditemukan. Buat file tersebut dengan format yang sesuai.", style="bold red")
        exit()


def main_menu():
    clear_screen()
    header_display()
    console.print("\n[bold yellow][center][size=14]Selamat Datang Di Coffee Shop Kami![/size][/center][/bold yellow]\n", style="underline")

    console.print("[1] Admin", style="bold white")
    console.print("[2] Menu", style="bold white")
    console.print("[3] Exit", style="bold white")
    user_type = get_bold_white_input("\nPilih: ")

    if user_type == '1':
        admin_login()
    elif user_type == '2':
        clear_screen()
        member_menu()
    elif user_type == '3':
        console.print("Terima kasih telah menggunakan program ini. Sampai jumpa!", style="bold blue")
        time.sleep(1)
        clear_screen()
        sys.exit()
    else:
        console.print("Pilihan tidak valid. Silakan coba lagi.", style="bold red")
        time.sleep(1)
        clear_screen()
        main_menu()

def admin_login():
    admin_data = load_admin_data()

    username = input("Masukkan username admin: ")
    password = pwinput("Masukkan password admin: ")

    if admin_data[(admin_data['user'] == username) & (admin_data['password'] == password)].empty:
        console.print("\nLogin gagal. Username atau password salah.", style="bold red")
        time.sleep(1)
        clear_screen()
        main_menu()
    else:
        console.print(f"\nSelamat Bertugas, {username}!", style="bold green")
        time.sleep(1)
        clear_screen()
        admin_menu()

def admin_menu():
    header_display()
    console.print("\n[bold blue][center][size=14]Ruang Admin[/size][/center][/bold blue]\n", style="underline")
    console.print("[1] Tambah Menu", style="bold white")
    console.print("[2] Hapus Menu", style="bold white")
    console.print("[3] Ubah Harga Kopi", style="bold white")
    console.print("[4] Melihat List Data", style="bold white")
    console.print("[5] Kembali ke Menu Awal", style="bold white")

    choice = get_bold_white_input("\nPilih: ")

    if choice == '1':
        tambah_menu()
    elif choice == '2':
        hapus_menu()
    elif choice == '3':
        ubah_harga_menu()
    elif choice == '4':
        melihat_list()
    elif choice == '5':
        console.print("\nKembali ke Menu Awal.", style="bold blue")
        time.sleep(1)
        clear_screen()
        main_menu()
    else:
        console.print("\nPilihan tidak valid. Silakan coba lagi.", style="bold red")
        time.sleep(1)
        clear_screen()
        admin_menu()

def tambah_menu():
    console.print("\n[bold white][center][size=14]Tambah Menu[/size][/center][/bold white]\n", style="underline")

    nama_kopi = input("Masukkan nama kopi baru: ")
    try:
        harga_kopi = int(input("Masukkan harga kopi baru (dalam rupiah): "))
    except ValueError:
        console.print("Harga kopi harus berupa angka.", style="bold red")
        time.sleep(1)
        clear_screen()
        admin_menu()
        return

    new_menu = pd.DataFrame({'Nama Kopi': [nama_kopi], 'Harga': [harga_kopi]})
    save_menu_kopi(new_menu)

    console.print(f"\nMenu {nama_kopi}Berhasil ditambahkan ✅", style="bold green")
    time.sleep(1)
    clear_screen()
    admin_menu()



def save_menu_kopi(new_menu):
    try:
        menu_kopi_existing = pd.read_csv('menu_kopi.csv')
    except FileNotFoundError:
        menu_kopi_existing = pd.DataFrame(columns=['Nama Kopi', 'Harga'])

    menu_kopi_updated = pd.concat([menu_kopi_existing, new_menu], axis=0, ignore_index=True)

    menu_kopi_updated = menu_kopi_updated.loc[:, ~menu_kopi_updated.columns.str.contains('^Unnamed')]

    menu_kopi_updated.to_csv('menu_kopi.csv', index=False)


def hapus_menu():
    console.print("\n[bold white][center][size=14]Hapus Menu[/size][/center][/bold white]\n", style="underline")

    nama_kopi = input("Masukkan nama kopi yang ingin dihapus: ")

    menu_kopi = pd.read_csv('menu_kopi.csv')
    if not menu_kopi[menu_kopi['Nama Kopi'] == nama_kopi].empty:
        menu_kopi = menu_kopi[menu_kopi['Nama Kopi'] != nama_kopi]
        menu_kopi.to_csv('menu_kopi.csv', index=False)
        console.print(f"\nMenu {nama_kopi} Berhasil dihapus ✅", style="bold green")
    else:
        console.print(f"\nMenu {nama_kopi} Tidak ditemukan.", style="bold red")

    time.sleep(2)
    clear_screen()
    admin_menu()

def ubah_harga_menu():
    console.print("\n[bold white][center][size=14]Ubah Harga Menu[/size][/center][/bold white]\n", style="underline")

    nama_kopi = input("Masukkan nama kopi yang ingin diubah harganya: ")
    harga_kopi_baru = int(input("Masukkan harga baru untuk kopi tersebut (dalam rupiah): "))

    try:
        menu_kopi = pd.read_csv('menu_kopi.csv')
        if nama_kopi in menu_kopi['Nama Kopi'].values:
            menu_kopi.loc[menu_kopi['Nama Kopi'] == nama_kopi, 'Harga'] = harga_kopi_baru
            menu_kopi.to_csv('menu_kopi.csv', index=False)
            console.print(f"\nHarga untuk {nama_kopi} Berhasil diubah menjadi Rp.{harga_kopi_baru:,.0f} ✅", style="bold green")
        else:
            console.print(f"\nMenu {nama_kopi} tidak ditemukan.", style="bold red")
    except FileNotFoundError:
        console.print("\nFile menu_kopi.csv tidak ditemukan.", style="bold red")

    time.sleep(1)
    clear_screen()
    admin_menu()

def melihat_list():
    console.print("\n[bold white][center][size=14]List Data[/size][/center][/bold white]\n", style="underline")

    console.print("\n[bold white][center][size=12]Data Admin[/size][/center][/bold white]", style="underline")
    display_table(load_admin_data())

    console.print("\n[bold white][center][size=12]Data Menu[/size][/center][/bold white]", style="underline")
    display_table(load_menu_kopi())

    Prompt.ask("\n[bold blue]Tekan [Enter] untuk kembali...[/]", show_default=False)
    clear_screen()
    admin_menu()

def display_table(data):
    table = Table(show_header=True, header_style="bold magenta")
    for col in data.columns:
        table.add_column(col, justify="center", style="cyan")
    for _, row in data.iterrows():
        table.add_row(*[str(row[col]) for col in data.columns])
    rich_print(table)

def member_menu():
    header_display()
    console.print("\n[bold blue][center][size=14]Menu[/size][/center][/bold blue]\n", style="underline")
    console.print("[1] Pesan Kopi", style="bold white")
    console.print("[2] Kembali ke Menu Awal", style="bold white")

    choice = get_bold_white_input("\nPilih: ")

    if choice == '1':
        console.print('''[bold white]
Selamat datang di Coffee Shop Kami!
Beli 5 kopi Apapun, Dan dapatkan diskon 2%
Diskon dapat mencapai maksimal 30% LOHHH![/bold white]''')
        tampilkan_menu_kopi()
        pesan_langsung()
    elif choice == '2':
        console.print("Kembali ke Menu Awal.", style="bold blue")
        time.sleep(1)
        clear_screen()
        main_menu()
    else:
        console.print("Pilihan tidak valid. Silakan coba lagi.", style="bold red")
        time.sleep(1)
        clear_screen()
        header_display()
        member_menu()

def tampilkan_menu_kopi():
    menu_kopi = load_menu_kopi()

    console.print("\n[bold blue][center][size=14]Daftar Menu Kopi[/size][/center][/bold blue]\n", style="underline")
    display_table(menu_kopi)

def pesan_langsung():
    menu_kopi = load_menu_kopi()

    nama_kopi = get_bold_white_input("Masukkan nama kopi yang ingin dipesan: ")
    kuantitas = int(get_bold_white_input("Masukkan jumlah kopi yang ingin dipesan: "))

    harga_kopi = menu_kopi.loc[menu_kopi['Nama Kopi'] == nama_kopi, 'Harga'].values[0]
    total_harga = kuantitas * harga_kopi

    global total_pembelian
    total_pembelian += kuantitas
    diskon_rate = min((total_pembelian // 5) * 2, 30)
    diskon_amount = (diskon_rate / 100) * total_harga
    total_harga -= diskon_amount

    console.print(f"\nTotal harga setelah diskon {diskon_rate}%: {format_currency(total_harga)}", style="bold blue")

    for _ in range(3):
        uang = int(get_bold_white_input("Masukkan jumlah uang: Rp."))
        kembalian = uang - total_harga

        if kembalian >= 0:
            tampilkan_struk(nama_kopi, kuantitas, total_harga, uang, kembalian, diskon_rate)
            console.print("Transaksi berhasil ✅", style="bold green")
            rate = Prompt.ask("[bold white]\nApakah Anda Puas Berbelanja Di Toko Kami? (Puas/Tidak Puas)")
            console.print("\n[bold yellow][size=20]Terimakasih Atas Masukan Anda, Kami Senang Melayani Anda![/size][/bold yellow]")
            time.sleep(3)
            clear_screen()
            member_menu()
        else:
            console.print("Jumlah uang tidak mencukupi. Silakan coba lagi.", style="bold red")
    else:
        console.print("Transaksi gagal. Jumlah percobaan habis. Kembali ke Menu Awal.", style="bold red")
        time.sleep(1)
        clear_screen()
        main_menu()



def tampilkan_struk(nama_kopi, kuantitas, total_harga, uang, kembalian, diskon_rate):
    console = Console()

    table = Table(show_header=False, show_lines=True, header_style="bold white")
    table.add_column("[bold white]Item[/bold white]")
    table.add_column("[bold white]Detail[/bold white]")

    table.add_row("[yellow]Nama Kopi[/yellow]", nama_kopi)
    table.add_row("[yellow]Jumlah Beli[/yellow]", str(kuantitas))

    table.add_row("[yellow]Diskon[/yellow]", f"{diskon_rate}%")
    table.add_row("[yellow]Total Harga[/yellow]", format_currency(total_harga))
    table.add_row("[yellow]Jumlah Uang[/yellow]", format_currency(uang))
    table.add_row("[yellow]Kembalian[/yellow]", format_currency(kembalian))

    title = Text("\nSTRUK PEMBAYARAN", style="bold white")
    console.print(title)
    console.print(table)

total_pembelian = 0

def main():
    while True:
        main_menu()

if __name__ == "__main__":
    main()
