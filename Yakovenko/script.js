// Получение элементов
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const formContainer = document.getElementById('formContainer');
const mainContainer = document.querySelector('.main-container');

// HTML-код формы входа
const loginForm = `
    <form id="loginForm">
        <label for="username">Имя пользователя</label>
        <input type="text" id="username" name="username" required>
        <label for="password">Пароль</label>
        <input type="password" id="password" name="password" required>
        <div id="loginError" class="error"></div>
        <button type="submit">Войти</button>
    </form>
`;

// HTML-код формы регистрации
const registerForm = `
    <form id="registrationForm">
        <label for="username">Имя пользователя</label>
        <input type="text" id="username" name="username" required>
        <label for="password">Пароль</label>
        <input type="password" id="password" name="password" required>
        <div id="passwordError" class="error"></div>
        <label for="confirmPassword">Подтверждение пароля</label>
        <input type="password" id="confirmPassword" name="confirmPassword" required>
        <div id="confirmPasswordError" class="error"></div>
        <button type="submit">Зарегистрироваться</button>
    </form>
`;

const changePassForm = `
    <form id="changePassForm">
        <label for="password">Пароль</label>
        <input type="password" id="password" name="password" required>
        <div id="passwordError" class="error"></div>
        <label for="confirmPassword">Подтверждение пароля</label>
        <input type="password" id="confirmPassword" name="confirmPassword" required>
        <div id="confirmPasswordError" class="error"></div>
        <button type="submit">Изменить пароль</button>
    </form>
`;

// Отображение формы входа
loginBtn.addEventListener('click', () => {
  formContainer.innerHTML = loginForm;

  // Добавляем обработчик отправки формы входа
  const loginFormElement = document.getElementById('loginForm');
  const loginErrorElement = document.getElementById('loginError');

  loginFormElement.addEventListener('submit', function (e) {
    e.preventDefault(); // Отменяем стандартное поведение формы

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    var params = new FormData();
    params.append('username', username);
    params.append('password', password);

    // Отправка данных на сервер
    fetch('https://yakovenko-aleksandr.ru/zadanie/checkUser.php', {
      method: 'POST',
      body: params,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.result.admin == '1') {
          adminUsers(data.result.userName);
        } else {
          formLogin(data.result);
        }
      })
      .catch((error) => {
        console.error('Ошибка:', error);
        loginErrorElement.textContent = 'Произошла ошибка при попытке входа.';
      });
  });
});

function formLogin(res) {
  if (res) {
    let div = `<h1>Добро пожаловать, ${res.userName}</h1>
        <div class="button-container">
            <button id="changePass">Сменить пароль</button>
            <button id="out">Выйти</button>
        </div>
        <div id="formContainer"></div>
        `;
    mainContainer.innerHTML = div;
    document.getElementById('out').addEventListener('click', () => {
      location.reload();
    });

    changePass(res.userName);
  } else {
    alert('неверный пароль');
    location.reload();
  }
}

function formLoginNewUser(userName) {
  let div = `<h1>Добро пожаловать, ${userName}</h1>
        <div class="button-container">
            <button id="changePass">Сменить пароль</button>
            <button id="out">Выйти</button>
        </div>`;
  mainContainer.innerHTML = div;
  document.getElementById('out').addEventListener('click', () => {
    location.reload();
  });

  changePass(userName);
}

// Отображение формы регистрации
registerBtn.addEventListener('click', () => {
  formContainer.innerHTML = registerForm;

  // Подключение проверки для формы регистрации
  const form = document.getElementById('registrationForm');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirmPassword');
  const passwordError = document.getElementById('passwordError');
  const confirmPasswordError = document.getElementById('confirmPasswordError');

  function validatePassword(password) {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    return regex.test(password);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    let valid = true;

    // Очистить предыдущие ошибки
    passwordError.textContent = '';
    confirmPasswordError.textContent = '';

    // Проверка пароля
    if (!validatePassword(passwordInput.value)) {
      valid = false;
      passwordError.textContent =
        'Пароль должен содержать не менее 8 символов, включать буквы верхнего и нижнего регистра, цифры и специальные символы.';
    }

    // Проверка подтверждения пароля
    if (passwordInput.value !== confirmPasswordInput.value) {
      valid = false;
      confirmPasswordError.textContent = 'Пароли не совпадают.';
    }

    if (!valid) {
      return;
    }

    var params = new FormData();
    params.append('username', username);
    params.append('password', passwordInput.value);

    // Отправка данных на сервер
    fetch('https://yakovenko-aleksandr.ru/zadanie/loginUser.php', {
      method: 'POST',
      body: params,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.success) {
          formLoginNewUser(username);
        }
      })
      .catch((error) => {
        console.error('Ошибка:', error);
        loginErrorElement.textContent = 'Произошла ошибка при попытке входа.';
      });
  });
});

function changePass(username) {
  document.getElementById('changePass').addEventListener('click', () => {
    const formContainer = document.getElementById('formContainer');
    formContainer.innerHTML = changePassForm;
    // Подключение проверки для формы регистрации
    const form = document.getElementById('changePassForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const passwordError = document.getElementById('passwordError');
    const confirmPasswordError = document.getElementById(
      'confirmPasswordError'
    );

    function validatePassword(password) {
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
      return regex.test(password);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      let valid = true;

      // Очистить предыдущие ошибки
      passwordError.textContent = '';
      confirmPasswordError.textContent = '';

      // Проверка пароля
      if (!validatePassword(passwordInput.value)) {
        valid = false;
        passwordError.textContent =
          'Пароль должен содержать не менее 8 символов, включать буквы верхнего и нижнего регистра, цифры и специальные символы.';
      }

      // Проверка подтверждения пароля
      if (passwordInput.value !== confirmPasswordInput.value) {
        valid = false;
        confirmPasswordError.textContent = 'Пароли не совпадают.';
      }

      if (!valid) {
        return;
      }

      var params = new FormData();
      params.append('username', username);
      params.append('password', passwordInput.value);

      // Отправка данных на сервер
      fetch('https://yakovenko-aleksandr.ru/zadanie/changePass.php', {
        method: 'POST',
        body: params,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert('Пароль успешно изменен. Войдите в систему с новым паролем!');
            location.reload();
          }
        })
        .catch((error) => {
          console.error('Ошибка:', error);
          loginErrorElement.textContent = 'Произошла ошибка при попытке входа.';
        });
    });
  });
}

function adminUsers(userName) {
  let users = [];
  let div = `<h1>Добро пожаловать, ${userName}</h1>
        <button id="outAdmin">Выйти</button>
        <ul class="users"></ul>
        <div id="formContainer"></div>`;
  mainContainer.innerHTML = div;

  document.getElementById('outAdmin').addEventListener('click', () => {
    location.reload();
  });

  fetch('https://yakovenko-aleksandr.ru/zadanie/allUsers.php', {
    method: 'POST',
  })
    .then((response) => response.json())
    .then((data) => {
      users = data.data;
      users.forEach((user) => {
        let li = document.createElement('li');
        li.classList.add('user');

        li.innerHTML = `<span>${user.userName}</span>
          <button class="change" username  = '${user.userName}'>сменить пароль</button>
          <button class="del" username  = '${user.userName}'>удалить</button>`;

        document.querySelector('.users').appendChild(li);
      });

      delUser();
      passwordChangeByAdministrator();
    })
    .catch((error) => {
      console.error('Ошибка:', error);
      loginErrorElement.textContent = 'Произошла ошибка при попытке входа.';
    });
}

function delUser() {
  const users = document.querySelectorAll('.del');

  users.forEach((user) => {
    user.addEventListener('click', (e) => {
      let username = e.target.getAttribute('username');
      var params = new FormData();
      params.append('username', username);

      // Отправка данных на сервер
      fetch('https://yakovenko-aleksandr.ru/zadanie/delUser.php', {
        method: 'POST',
        body: params,
      })
        .then((response) => response.json())
        .then((data) => {
          alert('Пользователь ' + username + ' успешно удален!');
          adminUsers('admin');
        })
        .catch((error) => {
          console.error('Ошибка:', error);
          loginErrorElement.textContent = 'Произошла ошибка при попытке входа.';
        });
    });
  });
}

function passwordChangeByAdministrator() {
  const users = document.querySelectorAll('.change');

  users.forEach((user) => {
    user.addEventListener('click', (e) => {
      const formContainer = document.getElementById('formContainer');
      formContainer.innerHTML = changePassForm;
      // Подключение проверки для формы регистрации
      const form = document.getElementById('changePassForm');
      const passwordInput = document.getElementById('password');
      const confirmPasswordInput = document.getElementById('confirmPassword');
      const passwordError = document.getElementById('passwordError');
      const confirmPasswordError = document.getElementById(
        'confirmPasswordError'
      );
      let username = e.target.getAttribute('username');

      function validatePassword(password) {
        const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
        return regex.test(password);
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        let valid = true;

        // Очистить предыдущие ошибки
        passwordError.textContent = '';
        confirmPasswordError.textContent = '';

        // Проверка пароля
        if (!validatePassword(passwordInput.value)) {
          valid = false;
          passwordError.textContent =
            'Пароль должен содержать не менее 8 символов, включать буквы верхнего и нижнего регистра, цифры и специальные символы.';
        }

        // Проверка подтверждения пароля
        if (passwordInput.value !== confirmPasswordInput.value) {
          valid = false;
          confirmPasswordError.textContent = 'Пароли не совпадают.';
        }

        if (!valid) {
          return;
        }

        var params = new FormData();
        params.append('username', username);
        params.append('password', passwordInput.value);

        // Отправка данных на сервер
        fetch('https://yakovenko-aleksandr.ru/zadanie/changePass.php', {
          method: 'POST',
          body: params,
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert('Пароль пользователя ' + username + ' успшно изменен!');
              adminUsers('admin');
            }
          })
          .catch((error) => {
            console.error('Ошибка:', error);
            loginErrorElement.textContent =
              'Произошла ошибка при попытке входа.';
          });
      });
    });
  });
}
