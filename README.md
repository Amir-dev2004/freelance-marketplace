# پلتفرم فریلنسری (Freelance Marketplace)

## ۱. معرفی پروژه

این پروژه با هدف طراحی و پیاده‌سازی یک پلتفرم فریلنسری مشابه پونیشا و Upwork توسعه داده شده است. در این سامانه، کارفرمایان می‌توانند پروژه‌های خود را ثبت کنند و فریلنسرها برای انجام آن‌ها پیشنهاد همکاری ارسال کنند.

## ۲. اعضای تیم

- امیرحسین عامری
- علی مانده زاده
- علی صحاف پور

## ۳. نقش‌های اصلی سیستم

- **کارفرما (Client):** ثبت پروژه، بررسی پیشنهادها و انتخاب فریلنسر.
- **فریلنسر (Freelancer):** مشاهده پروژه‌ها و ارسال پیشنهاد همکاری.
- **مدیر سیستم (Admin):** مدیریت کاربران و نظارت بر سیستم.

## ۴. تکنولوژی‌های استفاده‌شده

| بخش | تکنولوژی |
|---|---|
| Backend | Python, FastAPI |
| ORM | SQLAlchemy |
| Database | Microsoft SQL Server |
| Database Management | SQL Server Management Studio (SSMS) |
| Frontend | HTML, CSS, JavaScript |
| Password Hashing | Argon2 |
| Session Management | FastAPI, ItsDangerous |

## ۵. ساختار پوشه‌های پروژه

```text
freelance-marketplace/
│
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   │
│   └── .env
│
├── database/
│   ├── freelancer_database.sql
│   ├── Freelancer_ERD1.png
│   ├── Freelancer_ERD2.png
│   ├── Freelancer_ERD3.png
│   └── README.md
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── auth.js
│   ├── index.html
│   ├── signup.html
│   ├── forgot-password.html
│   ├── reset-password.html
│   └── welcome.html
│
├── freelancer-erd.png
├── requirements.md
└── README.md
```

## ۶. قابلیت‌های پیاده‌سازی‌شده

### احراز هویت کاربران

- ثبت‌نام کاربران جدید
- اعتبارسنجی اطلاعات هنگام ثبت‌نام
- ورود کاربران با ایمیل و رمز عبور
- ایجاد و مدیریت نشست کاربر (Session)
- خروج از حساب کاربری
- نمایش صفحه خوش‌آمدگویی پس از ورود موفق
- بازیابی رمز عبور از طریق لینک اختصاصی
- امکان استفاده یک‌باره از لینک بازیابی رمز عبور
- اعتبار ۱۵ دقیقه‌ای برای لینک بازیابی رمز عبور
- هش امن رمزهای عبور با استفاده از Argon2

### پایگاه داده

- طراحی و پیاده‌سازی جداول کاربران، پروژه‌ها، پیشنهادها و اطلاعات تکمیلی
- تعریف روابط و محدودیت‌های پایگاه داده
- استفاده از کلیدهای اصلی و خارجی
- ثبت داده‌های آزمایشی و اجرای آزمون‌های اعتبارسنجی

جزئیات ساختار دیتابیس و نحوه اجرای آن در فایل `database/README.md` قرار دارد.

## ۷. پیش‌نیازها

برای اجرای پروژه به موارد زیر نیاز دارید:

- Python 3.10 یا بالاتر
- Microsoft SQL Server
- SQL Server Management Studio (SSMS)
- ODBC Driver سازگار با SQL Server
- مرورگر وب
- Visual Studio Code یا ویرایشگر مشابه

## ۸. راه‌اندازی پایگاه داده

۱. نرم‌افزار SSMS را اجرا کنید.

۲. به SQL Server متصل شوید.

۳. فایل `database/freelancer_database.sql` را باز و اجرا کنید.

۴. مطمئن شوید پایگاه داده با موفقیت ایجاد شده است.

## ۹. راه‌اندازی Backend

ابتدا وارد پوشه Backend شوید:

```powershell
cd backend
```

محیط مجازی را فعال کنید:

```powershell
.\.venv\Scripts\Activate.ps1
```

در صورت نیاز، وابستگی‌ها را نصب کنید:

```powershell
pip install -r requirements.txt
```

یک محیط مجازی ایجاد کنید:
python -m venv .venv


محیط مجازی را فعال کنید:
.\.venv\Scripts\Activate.ps1


وابستگی‌های پروژه را نصب کنید:
pip install -r requirements.txt

فایل `.env` را در پوشه `backend` ایجاد و تنظیمات اتصال به دیتابیس و کلید امنیتی را در آن وارد کنید.

سپس سرور را اجرا کنید:

```powershell
uvicorn app.main:app --reload
```

آدرس مستندات API:

http://127.0.0.1:8000/docs

## ۱۰. اجرای Frontend

پس از اجرای Backend، پوشه اصلی پروژه را در Visual Studio Code باز کنید و با افزونه Live Server فایل زیر را اجرا کنید:

```text
frontend/index.html
```

صفحات اصلی Frontend:

- صفحه ورود
- صفحه ثبت‌نام
- صفحه فراموشی رمز عبور
- صفحه تغییر رمز عبور
- صفحه خوش‌آمدگویی

## ۱۱. لینک‌های پروژه

**GitHub Repository:**

https://github.com/Amir-dev2004/freelance-marketplace

**Pull Request:**

https://github.com/Amir-dev2004/freelance-marketplace/pull/1

**Jira Board:**

https://devfrontiers.atlassian.net/jira/software/projects/KAN/boards/2?filter=&groupBy=none
