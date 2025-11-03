from app.tasks import calculate, get_operation_stats

def display_menu():
    print("\n" + "="*50)
    print("CELERY CALCULATOR")
    print("="*50)
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. View Statistics")
    print("6. Exit")
    print("="*50)


def get_numbers():
    while True:
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            return a, b
        except ValueError:
            print("Invalid input! Please enter valid numbers.")


def perform_calculation(operation_name):
    a, b = get_numbers()
    print(f"\nSubmitting task: {operation_name}({a}, {b})")
    
    result = calculate.delay(a, b, operation_name)
    print(f"Task ID: {result.id}")
    print("Waiting for result...")
    
    task_result = result.get(timeout=10)
    
    symbols = {'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/'}
    symbol = symbols.get(operation_name, '?')
    
    print("\n" + "-"*50)
    if task_result['success']:
        print(f"Result: {a} {symbol} {b} = {task_result['result']}")
    else:
        print(f"Error: {task_result['error']}")
    print("-"*50)


def show_statistics():
    print("\nFetching statistics...")
    result = get_operation_stats.delay()
    task_result = result.get(timeout=10)
    
    print("\n" + "="*50)
    print("OPERATION STATISTICS")
    print("="*50)
    
    if task_result['success']:
        stats = task_result['stats']
        total = task_result['total_operations']
        
        if total == 0:
            print("No operations performed yet.")
        else:
            for operation in ['add', 'subtract', 'multiply', 'divide']:
                count = stats.get(operation, 0)
                percentage = (count / total * 100) if total > 0 else 0
                print(f"{operation.capitalize():<12}: {count:>5} ({percentage:>5.1f}%)")
            print("-"*50)
            print(f"{'Total':<12}: {total:>5}")
    else:
        print(f"Error: {task_result['error']}")
    
    print("="*50)


def main():
    operation_map = {
        '1': 'add',
        '2': 'subtract',
        '3': 'multiply',
        '4': 'divide'
    }
    
    print("\nWelcome to Celery Calculator!")
    print("Make sure Redis and Celery worker are running.")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '6':
            print("\nGoodbye!")
            break
        elif choice == '5':
            show_statistics()
        elif choice in operation_map:
            perform_calculation(operation_map[choice])
        else:
            print("\nInvalid choice! Please select 1-6.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication terminated.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure Redis and Celery worker are running!")