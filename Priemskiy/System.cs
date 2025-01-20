using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserSystem
{
    /// <summary>
    /// Основной класс приложения.
    /// </summary>
    public class System
    {
        /// <summary>
        /// Текущий пользователь
        /// </summary>
        private User? currentUser = null;

        /// <summary>
        /// Основной цикл приложения.
        /// Начинается с процедуры входа,
        /// затем идет обработка пользовательских команд,
        /// пока не поступит команда "logout", после
        /// чего все повторяется заново.
        /// Выйти из приложения можно нажав комбинацию Ctrl-C.
        /// </summary>
        public void Run()
        {
            while (true)
            {
                if (Login())
                {
                    if (!ProcessCommands())
                        return;
                }
            }
        }

        /// <summary>
        /// Обработка команд.
        /// Вход пользователя уже произошел.
        /// </summary>
        /// <returns></returns>
        public bool ProcessCommands()
        {
            while (true)
            {
                string? command = ReadCommand();

                if (command == null) 
                {
                    return false;
                }

                if (command == "logout")
                {
                    Logout();
                    return true;
                }

                if (command == "mod pass")
                {
                    ModPass();
                    continue;
                }

                if (command == "add user")
                {
                    AddUser();
                    continue;
                }

                if (command == "del user")
                {
                    DelUser();
                    continue;
                }

                if (command == "mod user")
                {
                    ModUser();
                    continue;
                }

                if (command == "user info")
                {
                    UserInfo();
                    continue;
                }

                if (command == "list users")
                {
                    ListUsers();
                    continue;
                }

                if (command == "date")
                {
                    Date();
                    continue;
                }

                if (command == "time")
                {
                    Time();
                    continue;
                }

                if (command == "help")
                {
                    Help();
                    continue;
                }

                Error("Неизвестная комманда.");
            }
        }        

        /// <summary>
        /// Процедура входа в аккаунт.
        /// </summary>
        /// <returns></returns>
        public bool Login() 
        {
            Console.Write("Логин: ");
            string? login = Console.ReadLine();
            if (login != null)
            {
                using var context = new AppDbContext();
                // Проверка логина
                var user = context.Users.Where(u => u.login == login).FirstOrDefault();
                if (user != null)
                {                    
                    string? password = ReadPassword("Пароль: ");                   
                    if (password != null)
                    {
                        // Проверка пароля
                        var pwd = context.Passwords.Where(p => p.user_id == user.id && p.password == password).FirstOrDefault();                        
                        if (pwd != null)
                        {
                            currentUser = user;
                            Console.WriteLine("Добро пожаловать, " + login + "!");

                            if (!user.is_admin)
                            {
                                // После удачной регистрации использованный пароль удаляется из списка. 
                                context.Passwords.Remove(pwd);
                                context.SaveChanges();
                                // Показать кол-во оставшихся паролей
                                int remains = context.Passwords.Where(p => p.user_id == user.id).Count();
                                Console.WriteLine("{0} паролей осталось.", remains);
                            }
                            Console.WriteLine();

                            return true;
                        }
                    }
                    Error("Некорректный пароль.");
                }
                else
                {
                    Error("Некорректный логин.");
                }
            }
            return false;
        }

        /// <summary>
        /// Выход из аккаунта
        /// </summary>
        public void Logout() 
        {            
            Console.WriteLine("До свидания, " + currentUser.login + "!\n");
            currentUser = null;
        }        

        /// <summary>
        /// Изменение пароля текущего пользователя
        /// </summary>
        public void ModPass()
        {
            ModPass(currentUser);    
        }

        /// <summary>
        /// Добавление нового пользователя
        /// </summary>
        public void AddUser()
        {
            // Только Администротор
            if (CanPerformCommand())
            {
                // Ввод и проверка логина
                Console.Write("Логин (не более 32 символов): ");
                string? login = Console.ReadLine();
                if (login == null || login.Length == 0)
                {
                    Error("Логин не должен быть пустым.");
                    return;
                }
                if (login.Length > 32)
                {
                    Error("Логин не должен быть длинее 32 символов.");
                    return;
                }

                // Ввод и проверка почты
                Console.Write("Эл. почта (не более 64 символов, опционально): ");
                string? email = Console.ReadLine();
                if (email != null && email.Length > 64)
                {
                    Error("Эл. почта не должна быть длинее 64 символов.");
                    return;
                }

                // Запрос роли пользователя (Администратор или Пользователь)
                bool is_admin = false;
                Console.Write("Администратор? (0 - Нет, 1 - да): ");
                string? answer = Console.ReadLine();
                if (answer != null && answer == "1")
                {
                    is_admin = true;
                }

                // Создание нового пользователя
                User user = new User() { id=0, login=login, email=email, is_admin= is_admin };
                using (var context = new AppDbContext())
                {
                    context.Users.Add(user);
                    try
                    {
                        context.SaveChanges();
                    }
                    catch (Microsoft.EntityFrameworkCore.DbUpdateException)
                    {
                        // Проверка уникальности осуществляется на уровне базы данных
                        Error("Пользователь с данным логином уже существует.");
                        return;
                    }
                }                

                if (is_admin)
                {
                    // Для Администратора создается один и только один пароль
                    AddPassword(user);
                }
                else
                {
                    // Для Пользователя может быть задано от 0 до любого кол-ва паролей
                    AddPasswords(user);
                }                
            }
        }

        /// <summary>
        /// Удаление пользователя
        /// </summary>
        public void DelUser()
        {
            // Только Администротор
            if (CanPerformCommand())
            {
                // Ввод логина пользователя
                Console.Write("Логин: ");
                string? login = Console.ReadLine();
                if (login != null)
                {
                    using var context = new AppDbContext();
                    // Проверка что пользователь существует
                    var user = context.Users.Where(u => u.login == login).FirstOrDefault();
                    if (user != null)
                    {
                        // Проверка на самоудаление
                        if (user.id == currentUser.id)
                        {
                            Error("Нельзя удалить самомго себя.");
                        }
                        else
                        {
                            // Сначала удалим связанные пароли
                            var pwds = context.Passwords.Where(p => p.user_id == user.id).ToArray();
                            context.Passwords.RemoveRange(pwds);
                            context.SaveChanges();

                            // Затем сам аккаунт
                            context.Users.Remove(user);
                            context.SaveChanges();
                        }
                    }
                    else
                    {
                        Error("Пользователь не найден.");
                    }
                }
            }            
        }

        /// <summary>
        /// Изменение учетных данных пользователя
        /// </summary>
        public void ModUser()
        {
            // Только Администротор
            if (CanPerformCommand())
            {
                // Ввод логина пользователя
                Console.Write("Логин: ");
                string? login = Console.ReadLine();
                if (login != null)
                {
                    using var context = new AppDbContext();
                    // Проверка что пользователь существует
                    var user = context.Users.Where(u => u.login == login).FirstOrDefault();
                    if (user != null)
                    {
                        // Выбор действия с аккаунтом
                        while (true)
                        {
                            Console.WriteLine("Выберите действие:");
                            Console.WriteLine("0) Закончить");
                            Console.WriteLine("1) Изменить логин");
                            Console.WriteLine("2) Изменить эл. почту");
                            Console.WriteLine("3) Изменить пароль");
                            if (!user.is_admin)
                            {
                                Console.WriteLine("4) Добавить пароли");
                            }
                            Console.Write("? ");
                            string? cmd = Console.ReadLine();
                            if (cmd == null || cmd == "0")
                            { 
                                break; 
                            }
                            else if (cmd == "1")
                            {
                                ModLogin(user);
                            }
                            else  if (cmd == "2")
                            {
                                ModEmail(user);
                            }
                            else if(cmd == "3")
                            {
                                ModPass(user);
                            }
                            else if(!user.is_admin && cmd == "4")
                            {
                                AddPasswords(user);
                            }
                            else
                            {
                                break;
                            }

                        }                        
                    }
                    else
                    {
                        Error("Пользователь не найден.");
                    }
                }
            }
        }

        /// <summary>
        /// Вывод информации о текущем пользователе
        /// </summary>
        public void UserInfo()
        {
            Console.WriteLine("Логин: " + currentUser.login);
            Console.WriteLine("Эл. почта: " + currentUser.email);
            if (!currentUser.is_admin)
            {
                // Показать кол-во оставшихся паролей
                using var context = new AppDbContext();
                int remains = context.Passwords.Where(p => p.user_id == currentUser.id).Count();
                Console.WriteLine("{0} паролей осталось.", remains);
            }
        }

        /// <summary>
        /// Вывод списка всех пользователей в табличном вормате
        /// </summary>
        public void ListUsers()
        {
            using var context = new AppDbContext();
            var users = context.Users.ToList();
            Console.WriteLine("---------------------------------------------------------------------------------------------------------------");
            Console.WriteLine("{0,-32} {1,-64} {2}", "Логин", "Эл. почта", "Роль");
            Console.WriteLine("---------------------------------------------------------------------------------------------------------------");
            foreach (var user in users)
            {
                string role = user.is_admin ? "Администратор" : "Пользователь";
                
                Console.WriteLine("{0,-32} {1,-64} {2}", user.login, user.email, role);
            }
            Console.WriteLine("---------------------------------------------------------------------------------------------------------------");
        }

        /// <summary>
        /// Вывод текущей даты
        /// </summary>
        public void Date()
        {
            var now = DateTime.Now;
            Console.WriteLine(now.ToString("dd MMMM yyyy, dddd", CultureInfo.CreateSpecificCulture("ru-RU")));
        }

        /// <summary>
        /// Вывод текущего времени
        /// </summary>
        public void Time()
        {
            var now = DateTime.Now;
            Console.WriteLine(now.ToString("HH:mm:ss%K"));
        }

        /// <summary>
        /// Вывод списка доступных команд
        /// </summary>
        public void Help()
        {
            Console.Write("logout");
            Console.WriteLine("\t\tВыход из аккаунта");

            Console.Write("mod pass");
            Console.WriteLine("\tИзменение своего пароля");

            Console.Write("add user");
            Console.WriteLine("\tДобавление нового пользователя");

            Console.Write("del user");
            Console.WriteLine("\tУдаление существующего пользователя");

            Console.Write("mod user");
            Console.WriteLine("\tИзменение учетных данных пользователя");

            Console.Write("user info");
            Console.WriteLine("\tИнформация о текущем пользователе");

            Console.Write("list users");
            Console.WriteLine("\tСписок всех пользователей системы");

            Console.Write("date");
            Console.WriteLine("\t\tТекущая дата");

            Console.Write("time");
            Console.WriteLine("\t\tТекущее время");

            Console.Write("help");
            Console.WriteLine("\t\tСписок доступных команд");
        }

        /// <summary>
        /// Ввод команды
        /// </summary>
        /// <returns></returns>
        private string? ReadCommand()
        {
            Console.Write("$ ");
            string? command = Console.ReadLine();
            return command;
        }

        /// <summary>
        /// Ввод пароля.
        /// Пароль скрывается за счет изменения цвета шрифта консоли.
        /// После ввода цвет возвращается в изначальное состояние.
        /// </summary>
        /// <param name="message"></param>
        /// <returns></returns>
        private string? ReadPassword(string message)
        {
            Console.Write(message);
            Console.ForegroundColor = Console.BackgroundColor;
            Console.CursorVisible = false;
            string? password = Console.ReadLine();
            Console.ResetColor();
            Console.CursorVisible = true;
            return password;
        }

        /// <summary>
        /// Вывод сообщения об ошибке красным цветом.
        /// </summary>
        /// <param name="message"></param>
        private void Error(string message)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine(message);
            Console.ResetColor();
        }

        /// <summary>
        /// Проверка, что текущий пользователь является Администратором.
        /// </summary>
        /// <returns></returns>
        private bool CanPerformCommand()
        {
            if (currentUser.is_admin)
            {
                return true;
            }
            Error("Доступ запрещен.");
            return false;
        }        

        /// <summary>
        /// Изменение логина пользователя
        /// </summary>
        /// <param name="user"></param>
        private void ModLogin(User user)
        {
            // Ввод и проверка нового логина
            Console.Write("Логин (не более 32 символов): ");
            string? login = Console.ReadLine();
            if (login == null || login.Length == 0)
            {
                Error("Логин не должен быть пустым.");
                return;
            }
            if (login.Length > 32)
            {
                Error("Логин не должен быть длинее 32 символов.");
                return;
            }

            // Сохранение в БД
            user.login = login;
            using var context = new AppDbContext();
            context.Users.Update(user);
            context.SaveChanges();
        }

        /// <summary>
        /// Изменение эл. почты пользователя
        /// </summary>
        /// <param name="user"></param>
        private void ModEmail(User user)
        {
            // Ввод и проверка новой почты
            Console.Write("Эл. почта (не более 64 символов, опционально): ");
            string? email = Console.ReadLine();
            if (email != null && email.Length > 64)
            {
                Error("Эл. почта не должна быть длинее 64 символов.");
                return;
            }
            // Сохранение в БД
            user.email = email;
            using var context = new AppDbContext();
            context.Users.Update(user);
            context.SaveChanges();
        }

        /// <summary>
        /// Изменение пароля пользователя
        /// </summary>
        /// <param name="user"></param>
        private void ModPass(User user)
        {
            // Ввод старого пароля
            string? oldPass = ReadPassword("Введите старый пароль: ");
            if (oldPass != null)
            {
                using var context = new AppDbContext();
                // Проверка старого пароля
                var pwd = context.Passwords.Where(p => p.user_id == user.id && p.password == oldPass).FirstOrDefault();
                if (pwd != null)
                {
                    // Ввод и проверка нового пароля
                    string? newPass = ReadPassword("Введите новый пароль: ");
                    if (newPass == null || newPass.Length == 0)
                    {
                        Error("Пароль не должен быть пустым.");
                    }
                    else if (newPass.Length > 32)
                    {
                        Error("Пароль не должен быть длинее 32 символов.");
                    }
                    else
                    {
                        // Повторный ввод нового пароля
                        string? newPassConfirm = ReadPassword("Повторите новый пароль: ");
                        if (newPass == newPassConfirm)
                        {
                            pwd.password = newPass;
                            context.SaveChanges();
                        }
                        else
                        {
                            Error("Пароли не совпадают.");
                        }
                    }
                }
                else
                {
                    Error("Некорректный пароль.");
                }
            }
        }

        /// <summary>
        /// Создание одного единственного пароля для Администратора
        /// </summary>
        /// <param name="user"></param>
        private void AddPassword(User user)
        {            
            while (true)
            {
                // Ввод и проверка нового пароля
                string? password = ReadPassword("Пароль (не более 32 символов): ");
                if (password == null || password.Length == 0)
                {
                    Error("Пароль не должен быть пустым.");
                    continue;
                }
                if (password.Length > 32)
                {
                    Error("Пароль не должен быть длинее 32 символов.");
                    continue;
                }

                // Повторный ввод нового пароля
                string? confirmPassword = ReadPassword("Повторите пароль: ");
                if (password == confirmPassword)
                {
                    // Сохранение пароля в БД
                    using var context = new AppDbContext();
                    Password pwd = new Password() { id = 0, user_id = user.id, password = password };
                    context.Passwords.Add(pwd);                
                    context.SaveChanges();
                    break;
                }
                else
                {
                    Error("Пароли не совпадают.");
                }
            }            
        }

        /// <summary>
        /// Создание списка паролей для Пользователя
        /// </summary>
        /// <param name="user"></param>
        private void AddPasswords(User user)
        {
            int i = 1;
            List<string> passwordList = new List<string>();
            while (true)
            {
                // Ввод и проверка нового пароля
                string message = string.Format("Пароль №{0} (не более 32 символов, пустая строка чтобы закончить): ", i);
                string? password = ReadPassword(message);
                if (password == null || password.Length == 0)
                {
                    break;
                }
                if (password.Length > 32)
                {
                    Error("Пароль не должен быть длинее 32 символов.");
                    continue;
                }

                // Повторный ввод нового пароля
                string? confirmPassword = ReadPassword("Повторите пароль: ");
                if (password == confirmPassword)
                {
                    // Добавить в список
                    passwordList.Add(password);
                    ++i;
                }
                else
                {
                    Error("Пароли не совпадают.");
                }
            }

            // Сохранение списка паролей в БД
            using var context = new AppDbContext();
            foreach (string password in passwordList)
            {
                Password pwd = new Password() { id = 0, user_id = user.id, password = password };
                context.Passwords.Add(pwd);
            }
            context.SaveChanges();
        }
    }
}
