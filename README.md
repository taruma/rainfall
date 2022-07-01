# Rainfall Data Explorer (hidrokit-rainfall)

<div align="center">
<img src="./_readme/fiakodev-rainfall-thumbnail.png" alt="hidrokit-rainfall thumbnail"><br>

<img alt="developed by" src="https://img.shields.io/badge/developed%20by-taruma%20%26%20fiakodev-orange">
<img alt="project by" src="https://img.shields.io/badge/project%20by-taruma%20%26%20PT.%20FIAKO%20ENJINIRING%20INDONESIA-blue">
<img alt="License" src="https://img.shields.io/github/license/fiakoenjiniring/rainfall.svg">
<br>
<img alt="GitHub release" src="https://img.shields.io/github/release/fiakoenjiniring/rainfall.svg?logo=github">
<img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/fiakoenjiniring/rainfall.svg?logo=github">
</div>

__Rainfall Data Explorer__ (`hidrokit-rainfall`) adalah _dashboard_ untuk mengeksplorasi data hujan di setiap stasiunnya dan membandingkannya baik secara numerik maupun visual. `hidrokit-rainfall` dibuat menggunakan teknologi [Dash + Plotly](https://plotly.com/) dengan bahasa pemrograman Python. Proyek `hidrokit-rainfall` bersifat _open-source_ dengan lisensi MIT.

## Cara Menjalankan Dashboard (Lokal)

Sangat dianjurkan untuk menjalankan dashboard ini menggunakan mesin lokal.

- Buat _virtual environment_ menggunakan `environment.yml` (untuk conda) atau `requirements.txt` (untuk venv).
- Jalankan `app.py` di terminal.
- Buka alamat `http://127.0.0.1:8050/` di browser.

## Cara Penggunaan



## Catatan

- ~~Dashboard ini seharusnya bergantung pada paket hidrokit terutama pada modul `hidrokit.contrib.taruma.hk98` mengenai rekap data (tabel analisis). Akan tetapi ditemukan isu di hidrokit/hidrokit#219. Sehingga untuk sementara modul tersebut terpisah dengan dashboard ini.~~ Sudah menggunakan hidrokit versi 0.4.1.

## LISENSI

[MIT LICENSE](./LICENSE)

```
Copyright ©️ 2022 Taruma Sakti Megariansyah, PT. FIAKO ENJINIRING INDONESIA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```