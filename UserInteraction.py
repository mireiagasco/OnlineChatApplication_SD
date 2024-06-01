from colorama import Fore


def get_chat_options():
    options = {
        "1": True,
        "2": False
    }

    print("\n" + Fore.CYAN + "Options:" + Fore.RESET)
    print("1. " + Fore.MAGENTA + "Subscribe to group chat (receive)" + Fore.RESET)
    print("2. " + Fore.MAGENTA + "Connect to group chat (receive + send)" + Fore.RESET)
    spectator = options.get(input(Fore.YELLOW + "Enter your choice: " + Fore.RESET), False)

    print("\n" + Fore.CYAN + "Type of chat:" + Fore.RESET)
    print("1. " + Fore.MAGENTA + "Transient" + Fore.RESET)
    print("2. " + Fore.MAGENTA + "Persistent" + Fore.RESET)
    persistent = not options.get(input(Fore.YELLOW + "Enter your choice: " + Fore.RESET), False)

    return spectator, persistent


def get_discovery_option():
    print("\n" + Fore.CYAN + "Discovery Options:" + Fore.RESET)
    print("1. " + Fore.MAGENTA + "Discover chats via Redis" + Fore.RESET)
    print("2. " + Fore.MAGENTA + "Discover chats via RabbitMQ" + Fore.RESET)
    print("3. " + Fore.RED + "Back" + Fore.RESET)

    return input(Fore.YELLOW + "Enter your choice: " + Fore.RESET)


def get_main_choice():
    print("\n" + Fore.CYAN + "Options:" + Fore.RESET)
    print("1. " + Fore.MAGENTA + "Connect to chat" + Fore.RESET)
    print("2. " + Fore.MAGENTA + "Subscribe to group chat" + Fore.RESET)
    print("3. " + Fore.MAGENTA + "Discover chats" + Fore.RESET)
    print("4. " + Fore.MAGENTA + "Access insult channel" + Fore.RESET)
    print("5. " + Fore.RED + "Exit" + Fore.RESET)

    return input(Fore.YELLOW + "Enter your choice: " + Fore.RESET)
