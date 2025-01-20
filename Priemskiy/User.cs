using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserSystem
{
    /// <summary>
    /// Пользователь из таблицы БД "users"
    /// </summary>
    public class User
    {
        public required int id { get; set; }
        public required string login { get; set; }
        public string? email { get; set; }
        public required bool is_admin { get; set; }
    }
}
