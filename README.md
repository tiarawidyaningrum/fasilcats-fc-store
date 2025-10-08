## Jawaban Pertanyaan Tugas 6

### 1. Apa perbedaan antara synchronous request dan asynchronous request?
synchronous request 
-definisi, Permintaan dikirim, dan browser menunggu respons hingga selesai.
-blocking, Memblokir (Blocking). Thread utama diblokir, membuat UI freeze atau hang.
-alur kerja, Permintaan harus dieksekusi secara berurutan.

asynchronous request
-definisi, Permintaan dikirim, dan browser tidak menunggu.
-blocking, Tidak Memblokir (Non-blocking). Thread utama tetap bebas.
-alur kerja, Permintaan dikirim di background, dan hasil ditangani oleh callback function.

### 2. Bagaimana AJAX bekerja di Django (alur request–response)?
AJAX di Django memungkinkan pertukaran data secara parsial antara frontend dan backend tanpa page reload. dengan alur

Client-Side (Frontend)
-action user (misalnya klik tombol "Add Product") memicu event listener JavaScript.
-JavaScript (menggunakan fetch() API atau XMLHttpRequest) membuat permintaan asinkron (misalnya POST/GET) ke URL Django. Data dikirim dalam format ringan, umumnya FormData atau JSON.

Server-Side (Django)
-Django Router (urls.py) mengarahkan permintaan ke View Function yang ditujukan untuk AJAX (misalnya add_product_entry_ajax).
-View Function memproses data, melakukan validasi (menggunakan ProductForm atau AuthenticationForm) dan sanitasi (strip_tags) untuk keamanan.
-Setelah berinteraksi dengan database (CRUD), View tidak me-render template HTML. Sebaliknya, ia mengembalikan respons ringan berupa JsonResponse (berisi data baru atau pesan status) atau HttpResponse(status=xxx).

Client-Side (Frontend)
-JavaScript menerima respons JSON/status.
-JavaScript kemudian memperbarui bagian tertentu dari DOM (Document Object Model) halaman (misalnya, menambahkan card produk baru ke grid atau menampilkan Toast notification) tanpa harus memuat ulang seluruh halaman.

### 3. Apa keuntungan menggunakan AJAX dibandingkan render biasa di Django?
Keuntungan: AJAX;	Render Biasa
Kecepatan & Responsivitas:
	Lebih cepat dan responsif karena hanya data kecil yang ditukar; 
  Lebih lambat karena membutuhkan full page reload untuk setiap interaksi.
Pengalaman Pengguna (UX):
	Mulus (seamless), UI tidak terblokir, dan konteks pengguna (seperti scroll position) tetap terjaga;	
  Terputus-putus (jarring), mengganggu alur pengguna.
Efisiensi Bandwidth	Sangat:
 efisien, hanya mengirim dan menerima data (JSON/XML);
 Membutuhkan bandwidth lebih besar karena harus mengirim HTML, CSS, dan JavaScript secara berulang.
Interaktivitas:
	Tinggi. Memungkinkan live update dan state management yang kompleks di client-side;	
  Rendah. Interaktivitas harus diimplementasikan dengan pengiriman form berulang.

### 4. Bagaimana cara memastikan keamanan saat menggunakan AJAX untuk fitur Login dan Register di Django?
Cross-Site Request Forgery (CSRF) Protection:
-Semua request POST, PUT, dan DELETE ke endpoint AJAX harus menyertakan CSRF Token di dalam request body (FormData) atau header (X-CSRFToken). mencegah request berbahaya dari domain lain.
-Meskipun View Function diberi dekorator @csrf_exempt (jika menggunakan body JSON), metode yang lebih aman adalah menggunakan FormData dengan token terlampir, atau JSON dengan token di header, dan membiarkan Django memverifikasinya.

Menggunakan HTTPS: Menggunakan protokol HTTPS adalah wajib. Ini mengenkripsi semua data sensitif (seperti password dan username) saat transit, mencegah penyadapan (Man-in-the-Middle Attack).

Django Forms & Built-in Validation: Menggunakan UserCreationForm dan AuthenticationForm di backend (di endpoint AJAX) memastikan bahwa validasi standar (keamanan password, ketersediaan username) dilakukan oleh framework Django yang terpercaya.

Backend Rate Limiting: Menerapkan batas percobaan login di backend untuk mencegah serangan brute-force yang mengeksploitasi kecepatan endpoint AJAX.

### 5. Bagaimana AJAX mempengaruhi pengalaman pengguna (User Experience) pada website?
AJAX secara fundamental mengubah dan meningkatkan pengalaman pengguna (UX) dengan menciptakan pengalaman yang lebih modern, cepat, dan interaktif:
-Responsivitas Instan: Menghilangkan jeda yang disebabkan oleh full page reload. Aksi seperti menambahkan produk atau login terasa instan.
-Feedback Asinkron: AJAX memungkinkan penggunaan Loading State, Error State, dan Toast Notification (seperti yang diimplementasikan di Tugas 6). Pengguna mendapatkan umpan balik langsung (misalnya, spinner saat data dimuat, atau toast "Product Added!") tanpa harus menunggu redirect halaman, sehingga mengurangi frustrasi.
-Pengurangan "Blank Page": Pengguna tidak akan melihat halaman putih kosong selama loading, karena hanya bagian tertentu dari konten yang diperbarui.
-Pengelolaan Konteks: Pengguna dapat memfilter produk, mengedit form di modal, atau menghapus item tanpa kehilangan scroll position atau state aplikasi mereka.