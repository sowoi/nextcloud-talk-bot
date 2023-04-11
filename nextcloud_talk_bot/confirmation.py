def are_you_sure(object, entity):
    while True:
        user_input = input(f"Are you sure you want to {object} '{entity}'? This process is irrevocable! (yes/no): ")
        if user_input.lower() == 'no':
            return False
        elif user_input.lower() == 'yes':
            return True
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")