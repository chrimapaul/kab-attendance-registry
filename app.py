def main():
    while True:
        print("\n=== KAB Attendance Registry ===")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
