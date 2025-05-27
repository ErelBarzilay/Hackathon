import threading
from get_gov_data import get_gov_data
from get_btl_data import get_btl_data

def main():
    gov_thread = threading.Thread(target=get_gov_data)
    btl_thread = threading.Thread(target=get_btl_data)

    # Start threads
    gov_thread.start()
    btl_thread.start()

    # Wait for both threads to finish
    gov_thread.join()
    btl_thread.join()

if __name__ == "__main__":
    main()