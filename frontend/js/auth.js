
// Password visibility toggle

document.querySelectorAll(".toggle-password").forEach((button) => {
    button.addEventListener("click", () => {
        const inputId = button.dataset.target || "password";
        const passwordInput = document.getElementById(inputId);
        const eyeIcon = button.querySelector("svg");

        if (!passwordInput) return;

        const isPasswordHidden = passwordInput.type === "password";

        passwordInput.type = isPasswordHidden ? "text" : "password";

        if (eyeIcon) {
            eyeIcon.innerHTML = isPasswordHidden
                ? `
                    <path d="M3 3l18 18"/>
                    <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8"/>
                    <path d="M9.9 5.2A11 11 0 0 1 12 5c6.4 0 10 7 10 7s-3.6 7-10 7c-1.1 0-2.1-.2-3-.5"/>
                  `
                : `
                    <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/>
                    <circle cx="12" cy="12" r="3"/>
                  `;
        }

        button.setAttribute(
            "aria-label",
            isPasswordHidden ? "مخفی کردن رمز عبور" : "نمایش رمز عبور"
        );
    });
});

// Login form

const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        const errorMessage = document.getElementById("errorMessage");
        const loginButton = document.getElementById("loginButton");

        errorMessage.hidden = true;
        loginButton.disabled = true;
        loginButton.textContent = "در حال ورود...";

        try {
            const response = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || "ورود ناموفق بود.");
            }

            window.location.href = "welcome.html";

        } catch (error) {
            errorMessage.textContent =
                error.message === "Failed to fetch"
                    ? "ارتباط با سرور برقرار نشد."
                    : error.message;

            errorMessage.hidden = false;
        } finally {
            loginButton.disabled = false;
            loginButton.textContent = "ورود به حساب";
        }
    });
}

// Welcome page: get current user

const welcomeMessage = document.getElementById("welcomeMessage");

if (welcomeMessage) {
    async function loadCurrentUser() {
        try {
            const response = await fetch("http://127.0.0.1:8000/me", {
                method: "GET",
                credentials: "include"
            });

            if (response.status === 401 || response.status === 403) {
                window.location.href = "index.html";
                return;
            }

            if (!response.ok) {
                throw new Error("دریافت اطلاعات حساب ناموفق بود.");
            }

            const user = await response.json();

            welcomeMessage.textContent =
                `خوش اومدی ${user.name}! ایمیل شما: ${user.email}`;

        } catch (error) {
            welcomeMessage.textContent = "ارتباط با سرور برقرار نشد.";
        }
    }

    loadCurrentUser();
}


// Logout

const logoutButton = document.getElementById("logoutButton");

if (logoutButton) {
    logoutButton.addEventListener("click", async () => {
        logoutButton.disabled = true;
        logoutButton.textContent = "در حال خروج...";

        try {
            const response = await fetch("http://127.0.0.1:8000/logout", {
                method: "POST",
                credentials: "include"
            });

            if (!response.ok) {
                throw new Error("خروج از حساب ناموفق بود.");
            }

            window.location.href = "index.html";

        } catch (error) {
            logoutButton.disabled = false;
            logoutButton.textContent = "خروج از حساب کاربری";
            alert("ارتباط با سرور برقرار نشد.");
        }
    });
}

// Signup form

const signupForm = document.getElementById("signupForm");

if (signupForm) {
    signupForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const signupMessage = document.getElementById("signupMessage");
        const signupButton = document.getElementById("signupButton");

        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        const roles = Array.from(
            document.querySelectorAll('input[name="roles"]:checked')
        ).map((checkbox) => checkbox.value);

        signupMessage.hidden = true;
        signupMessage.className = "message";

        if (password !== confirmPassword) {
            signupMessage.textContent = "رمز عبور و تکرار آن یکسان نیستند.";
            signupMessage.classList.add("error");
            signupMessage.hidden = false;
            return;
        }

        if (roles.length === 0) {
            signupMessage.textContent = "حداقل یک نوع حساب کاربری انتخاب کن.";
            signupMessage.classList.add("error");
            signupMessage.hidden = false;
            return;
        }

        const data = {
            name: document.getElementById("name").value.trim(),
            email: document.getElementById("email").value.trim(),
            phone: document.getElementById("phone").value.trim() || null,
            codemeli: document.getElementById("codemeli").value.trim(),
            address: document.getElementById("address").value.trim(),
            password: password,
            confirm_password: confirmPassword,
            roles: roles
        };

        signupButton.disabled = true;
        signupButton.textContent = "در حال ثبت‌نام...";

        try {
            const response = await fetch("http://127.0.0.1:8000/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                let errorText = "ثبت‌نام ناموفق بود.";

                if (typeof result.detail === "string") {
                    errorText = result.detail;
                } else if (Array.isArray(result.detail)) {
                    errorText = [...new Set(
                        result.detail
                            .map((item) => item.msg?.replace(/^Value error,\s*/, ""))
                            .filter(Boolean)
                    )].join("\n");
                }

                throw new Error(errorText);
            }

            signupMessage.textContent =
                "ثبت‌نام با موفقیت انجام شد. در حال انتقال به صفحه ورود...";

            signupMessage.classList.add("success");
            signupMessage.hidden = false;

            signupForm.reset();

            setTimeout(() => {
                window.location.href = "index.html";
            }, 1500);

        } catch (error) {
            signupMessage.textContent =
                error.message === "Failed to fetch"
                    ? "ارتباط با سرور برقرار نشد."
                    : error.message;

            signupMessage.classList.add("error");
            signupMessage.hidden = false;

        } finally {
            signupButton.disabled = false;
            signupButton.textContent = "ایجاد حساب کاربری";
        }
    });
}

// Forgot password form

const forgotPasswordForm = document.getElementById("forgotPasswordForm");

if (forgotPasswordForm) {
    forgotPasswordForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const forgotMessage = document.getElementById("forgotMessage");
        const forgotButton = document.getElementById("forgotButton");

        forgotMessage.hidden = true;
        forgotButton.disabled = true;
        forgotButton.textContent = "در حال ارسال...";

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/forgot-password",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email: email })
                }
            );

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || "ارسال درخواست ناموفق بود.");
            }

            forgotMessage.textContent =
                "اگر این ایمیل در سایت ثبت شده باشد، لینک بازیابی رمز عبور ایجاد شده است. ترمینال بک‌اند را بررسی کن.";

            forgotMessage.classList.add("success");
            forgotMessage.hidden = false;

        } catch (error) {
            forgotMessage.textContent =
                error.message === "Failed to fetch"
                    ? "ارتباط با سرور برقرار نشد."
                    : error.message;

            forgotMessage.classList.add("error");
            forgotMessage.hidden = false;

        } finally {
            forgotButton.disabled = false;
            forgotButton.textContent = "ارسال لینک بازیابی";
        }
    });
}

// Reset password form

const resetPasswordForm = document.getElementById("resetPasswordForm");

if (resetPasswordForm) {
    const resetMessage = document.getElementById("resetMessage");
    const resetButton = document.getElementById("resetButton");

    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");

    if (!token) {
        resetMessage.textContent = "لینک بازیابی رمز عبور معتبر نیست.";
        resetMessage.classList.add("error");
        resetMessage.hidden = false;
        resetButton.disabled = true;
    }

    resetPasswordForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!token) return;

        const newPassword = document.getElementById("newPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        resetMessage.hidden = true;

        if (newPassword !== confirmPassword) {
            resetMessage.textContent = "رمز عبور و تکرار آن یکسان نیستند.";
            resetMessage.className = "message error";
            resetMessage.hidden = false;
            return;
        }

        resetButton.disabled = true;
        resetButton.textContent = "در حال ذخیره...";

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/reset-password",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        token: token,
                        new_password: newPassword,
                        confirm_password: confirmPassword
                    })
                }
            );

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || "تغییر رمز عبور ناموفق بود.");
            }

            resetMessage.textContent =
                "رمز عبور با موفقیت تغییر کرد. در حال انتقال به صفحه ورود...";

            resetMessage.className = "message success";
            resetMessage.hidden = false;

            resetPasswordForm.reset();

            setTimeout(() => {
                window.location.href = "index.html";
            }, 2000);

        } catch (error) {
            resetMessage.textContent =
                error.message === "Failed to fetch"
                    ? "ارتباط با سرور برقرار نشد."
                    : error.message;

            resetMessage.className = "message error";
            resetMessage.hidden = false;

        } finally {
            resetButton.disabled = false;
            resetButton.textContent = "ذخیره رمز عبور جدید";
        }
    });
}
