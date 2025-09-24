## Jawaban Pertanyaan Tugas 4

### 1. Apa itu Django AuthenticationForm? Jelaskan juga kelebihan dan kekurangannya.

AuthenticationForm adalah form bawaan Django yang digunakan untuk proses login/autentikasi pengguna. Form ini menerima input username dan password, kemudian memvalidasi kredensial tersebut terhadap database pengguna.

Kelebihan:
-Sudah siap pakai tanpa perlu membuat form dari nol
-Validasi built-in untuk memverifikasi username dan password
-Keamanan terintegrasi dengan sistem autentikasi Django

Kekurangan:
-Fungsionalitas terbatas hanya untuk username/password (tidak support email login secara default)
-Tidak fleksibel untuk kebutuhan autentikasi yang kompleks (misalnya multi-factor authentication)

### 2. Apa perbedaan antara autentikasi dan otorisasi? Bagaiamana Django mengimplementasikan kedua konsep tersebut?

Autentikasi, proses memverifikasi identitas pengguna. Contoh: Login dengan username dan password. 
Django:
-AuthenticationForm untuk form login
-authenticate() dan login() functions untuk memverifikasi dan membuat session
-@login_required decorator untuk memaksa login

Otorisasi, proses menentukan akses dan hak yang dimiliki pengguna yang sudah terautentikasi. Contoh: User biasa tidak bisa mengakses halaman admin
Django:
-Permissions: Izin spesifik (add, change, delete, view)
-Superuser: Akses penuh ke seluruh aplikasi
-Template tags: {% if perms.app.permission %}

### 3. Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?

Session
Kelebihan, keamanan tinggi karena data disimpan di server, kapasitas besar, tidak mudah dimanipulasi oleh client, expire saat browser ditutup.
Kekurangan, beban server karena data disimpan di server, memory usage bertambah seiring jumlah user, scaling issues pada aplikasi dengan multiple server, hilang saat server restart (jika menggunakan memory storage).

Cookies
Kelebihan, ringan untuk server karena data disimpan di client, persistent dapat bertahan meskipun browser ditutup, mudah digunakan untuk data sederhana, scalable tidak mempengaruhi performa server.
Kekurangan, keamanan rendah karena dapat dimodifikasi client, kapasitas terbatas, bisa diblokir oleh browser user, tidak cocok untuk data sensitif.

### 4. Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai? Bagaimana Django menangani hal tersebut?

Risiko Potensial Cookies
-Session Hijacking: Cookie session dapat dicuri dan digunakan orang lain
-Cross-Site Scripting (XSS): JavaScript jahat dapat mengakses cookies
-Cross-Site Request Forgery (CSRF): Request palsu menggunakan cookies user
-Man-in-the-Middle: Cookies dapat disadap di koneksi tidak aman

Penanganan Django
-CSRF Protection
-Secure Cookies
-SameSite Attribute
-Cookie Age

### 5. elaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

Menambah fungsi register, login, dan logout

Tambah import di views.py:

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

Buat fungsi register:
(sesuai dengan tutorial)

Buat template html dengan styling yang sesuai desain

Tambah URL routing:

path('register/', register, name='register'),
path('login/', login_user, name='login'),
path('logout/', logout_user, name='logout'),

Merestriksi Akses Halaman

Tambah import decorator:

from django.contrib.auth.decorators import login_required

Tambah decorator pada fungsi views:

@login_required(login_url='/login')
def show_main(request):
   
@login_required(login_url='/login')
def create_product(request):

Implementasi Cookies

Set cookie saat login:

response.set_cookie('last_login', str(datetime.datetime.now()))

Tampilkan last_login di context:

context = {
    'last_login': request.COOKIES.get('last_login', 'Never')
   }

Menghubungkan Model dengan User

Modifikasi models.py:

from django.contrib.auth.models import User
   
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

Filter produk berdasarkan user

   def show_main(request):
       filter_type = request.GET.get("filter", "my")
       if filter_type == "all":
           products = Product.objects.all()
       else:
           products = Product.objects.filter(user=request.user)

Jalankan migrasi

Membuat Dummy Data