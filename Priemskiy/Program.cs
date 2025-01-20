namespace UserSystem
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("User System 1.0.0\n");

            Console.Write("Подключение к базе данных...");

            // Проверка базы данных
            using (var context = new AppDbContext())
            {                
                if (context.Database.CanConnect())
                {
                    Console.WriteLine("OK\n");
                }
                else
                {
                    Console.WriteLine("Не удалось подключиться к базе данных.");
                    return;
                }
            }
            

            // Запуск системы
            System system = new System();
            try
            {
                system.Run();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }
    }
}
