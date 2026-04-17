import os
import re
import database
from game import Game

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_nickname():
    while True:
        nick = input("Введите ваш ник (только латиница, до 15 символов): ").strip()
        if re.match(r'^[A-Za-z]{1,15}$', nick):
            return nick
        print("Ошибка: Ник должен содержать только латинские буквы и быть не длиннее 15 символов.\n")

def show_leaderboard():
    clear_screen()
    print("=== ТАБЛИЦА РЕЙТИНГА (ТОП 10) ===")
    top_players = database.get_top_10()
    
    if not top_players:
        print("Пока нет записей. Станьте первым!")
    else:
        for i, (nick, score) in enumerate(top_players, 1):
            print(f"{i}. {nick} - {score} очков")
    
    print("\n")
    input("Нажмите Enter для возврата в меню...")

def main_menu():
    database.init_db()

    while True:
        clear_screen()
        print("=== ИГРА ЗМЕЙКА ===")
        print("Выберите опцию:")
        print("1 - Легкая (медленная)")
        print("2 - Средняя (стандартная)")
        print("3 - Сложная (быстрая)")
        print("4 - РЕЙТИНГ (Сложная + запись в БД)")
        print("5 - Таблица рейтинга")
        print("0 - Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        speed = 0.15
        rating_mode = False
        nickname = ""

        if choice == '1':
            speed = 0.3
        elif choice == '2':
            speed = 0.15
        elif choice == '3':
            speed = 0.08
        elif choice == '4':
            speed = 0.08
            rating_mode = True
            print("\n--- Режим Рейтинга ---")
            nickname = validate_nickname()
            best_score = database.get_best_score(nickname)
            
            clear_screen()
            print(f"Игрок: {nickname}")
            print(f"Лучший результат: {best_score}")
            input("Нажмите Enter, чтобы начать игру...")
        elif choice == '5':
            show_leaderboard()
            continue
        elif choice == '0':
            print("До встречи!")
            break
        else:
            input("Неверный ввод. Нажмите Enter и попробуйте снова...")
            continue

        game = Game(height=10, width=20, speed=speed)
        final_score = game.play()
        
        print(f"\nВаш итоговый счет: {final_score}")
        
        if rating_mode:
            database.save_score(nickname, final_score)
            print("Результат сохранен в таблицу рейтинга!")
            
        input("\nНажмите Enter для возврата в главное меню...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nИгра экстренно завершена.")