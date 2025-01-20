using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserSystem
{
    /// <summary>
    /// Пароль из таблицы БД "passwords"
    /// </summary>
    public class Password
    {
        public required int id { get; set; }
        public required int user_id { get; set; }
        public required string password { get; set; }        
    }
}
