Dashboard ini bisa membaca berkas berformat '.csv' dengan:

- Kolom pertama merupakan tanggal dengan format yang dapat dibaca oleh fitur `parse_dates` yang tersedia di `pandas`. Direkomendasikan mengubahnya menjadi format `YYYY-MM-DD`. 
- Kolom lainnya merupakan data hujan dengan header. 
- Baris pertama akan dibaca sebagai header tabel, sehingga dianjurkan menambahkan label untuk setiap kolomnya. Gunakan label `DATE` untuk kolom tanggal yang akan digunakan sebagai index.

Navigasi dashboard ini antara lain:

- _Drag and Drop_ berkas atau pilih berkas pada tombol "Drag and Drop or Select Files". Klik "Use Example Data" jika ingin melihat demonstrasi dashboard ini.
- Jika prosesnya berhasil, akan muncul tabel dengan data yang di-_upload_ atau contoh data. Tabel ini _editable_ sehingga bisa menyesuaikan saat proses pengoreksian saat eksplorasi data. Bisa juga diubah nama tabelnya. Pastikan nama kolom berbeda dan nama kolom pertama (tanggal) selalu "DATE".
- Klik "Visualize Data" untuk melihat visualisasi data. Pada tahap ini, Anda bisa kembali ke tabel jika ingin melakukan pengoreksian data. Anda juga bisa melakukan filter pada setiap kolom untuk eksplorasi selanjutnya.` 
- Tabel yang telah diubah, bisa di-_download_ kembali dalam bentuk CSV. 
- Setelah tabel sudah dikoreksi. Bisa dilanjutkan ke tahapan analisis data. Perlu diingat, data yang dianalisis sesuai dengan tampilan/informasi tabel terkini. Jadi, jika masih ada filter, maka analisis hanya dilakukan pada data yang telah terfilter.
- Klik "Analyze Data" untuk melakukan analisis data. Perlu diingat, proses ini akan memakan waktu jika memiliki dataset yang besar. Jadi, sangat disarankan menggunakan mesin lokal untuk proses ini. Karena yang dapat diakses di web hanya berupa demonstrasi saja dan menggunakan layanan gratis sehingga sangat terbatas kemampuannya.
- Analisis data terbagi menjadi tiga periode yaitu 2 periode (biweekly), setiap bulanan (monthly), dan tahunan (yearly). Sebagai catatan, biweekly itu dibagi berdasarkan 16 hari pertama kemudian sisa harinya pada setiap bulan.
- __Baru di `v1.1.0`__: Analisis konsistensi (kurva massa ganda) dan kumulatif hujan tahunan. 
- Analisis data yang dilakukan berupa:
    - `days`: Jumlah hari pada setiap periodenya (16 hari untuk biweekly, 1 bulan untuk monthly, dan 1 tahun untuk yearly).
    - `max`: Nilai maksimum pada setiap periode.
    - `sum`: Total nilai pada setiap periode.
    - `n_rain`: Jumlah hari hujan di setiap periode.
    - `n_dry`: Jumlah hari kering di setiap periode. Catatan: Ini akan menghitung nilai `np.nan` sebagai hari kering.
    - `max_date`: Tanggal kejadian hujan maksimum terjadi pada setiap periode. 
- Tabel analisis tidak dapat diubah dan hanya sebagai penyedia informasi saja.
- Melihat tabel analisis rasanya cukup sulit untuk diceritakan atau diinterpretasikan, oleh karena itu disediakan tombol "Visualize it!" untuk melakuakn visualisasi tabel analisis.
- Selain melakukan visualisasi, tabel analisis juga dapat di-_download_ dengan mengklik tombol "Download Results as CSV". Perlu dicatat, `dataframe` tabel analisis menggunakan `MultiIndex` sehingga pada format CSV akan perlu dilakukan pengolahan lagi. 
- Visualisasi dari tabel analisis berupa:
    - Group Bar Chart untuk setiap periode dengan kolom `max` dan `sum`. Grafik ini bisa melihat secara langsung perbandingan nilai antar stasiun. 
    - Stack Bar Chart untuk setiap periode dengan kolom `n_rain` dan `n_dry`. Grafik ini bisa memberikan gambaran periode yang memiliki frekuensi hujan/kekeringan tinggi/rendah secara sekilas.
    - Bubble Chart (Maximum Rainfall Events) memberikan gambaran besar terkait tanggal kejadian saat hujan maksimum terjadi di setiap stasiun. Ukuran lingkaran menunjukkan seberapa besar hujan maksimum yang terjadi. 
    - __Baru di `v1.1.0`__: Ditambahkan grafik kumulatif hujan tahunan dan konsistensi (kurva massa ganda) untuk setiap stasiun.

Navigasi dengan grafik interaktif plotly:

- Pada setiap grafik plotly, dapat dilakukan interaksi langsung dengan grafik seperti mengatur stasiun/data mana saja yang ditampilkan, pembesaran pada periode tertentu. mengatur ukuran sumbu, dll.
- Sangat dianjurkan untuk mengeksplorasi sendiri mengenai _mode bar_ yang ada di kanan atas setiap grafik plotly. 
- Setiap grafik bisa di-_download_ dalam bentuk `.png` untuk kepentingan menaruh di dokumen atau lainnya. 
