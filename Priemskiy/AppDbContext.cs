using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserSystem
{
    /// <summary>
    /// Подключение к базе данных
    /// </summary>
    public class AppDbContext : DbContext
    {
        /// <summary>
        /// Пользователи
        /// </summary>
        public DbSet<User> Users { get; set; }

        /// <summary>
        /// Пароли
        /// </summary>
        public DbSet<Password> Passwords { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            // Строка подключения к БД
            string connectionString = "Host=localhost; Port=5432; Username=postgres; Password=admin; Database=user_system";
            optionsBuilder.UseNpgsql(connectionString);
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<User>().ToTable("users");
            modelBuilder.Entity<Password>().ToTable("passwords");
        }
    }
}
