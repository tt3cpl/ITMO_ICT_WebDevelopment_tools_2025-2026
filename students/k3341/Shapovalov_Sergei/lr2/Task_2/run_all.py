import subprocess
import sys
from pathlib import Path

task_dir = Path(__file__).parent

def run_program(program_name: str):
    print(f"\n{'=' * 70}")
    print(f"🚀 Запускаем {program_name}...")
    print(f"{'=' * 70}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, task_dir / program_name],
            cwd=str(task_dir),
            capture_output=False,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"❌ Ошибка при выполнении {program_name}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout при выполнении {program_name}")
        return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def main():
    """Главная функция"""
    print("\n" + "=" * 70)
    print("🔬 СРАВНЕНИЕ ТРЁХ ПОДХОДОВ ПАРАЛЛЕЛЬНОГО ПАРСИНГА")
    print("=" * 70)
    
    programs = [
        "ex_threading.py",
        "ex_multiprocessing.py",
        "ex_async.py"
    ]
    
    results = {}
    
    for program in programs:
        try:
            run_program(program)
            results[program] = True
        except Exception as e:
            print(f"❌ Ошибка при запуске {program}: {e}")
            results[program] = False
    
    # Выводим итоговый отчёт
    print("\n" + "=" * 70)
    print("📊 ИТОГОВЫЙ ОТЧЁТ")
    print("=" * 70)
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n✅ Успешно выполнено: {successful}/{total} программ")
    print(f"\nДетали:")
    for program, success in results.items():
        status = "✅ OK" if success else "❌ FAILED"
        print(f"  {program}: {status}")
    
    print("\n" + "=" * 70)
    print("📝 Примечание: Результаты сохранены в БД (таблица 'quote')")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
