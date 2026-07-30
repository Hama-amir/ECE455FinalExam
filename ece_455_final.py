import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python ece_455_final.py <input_filename>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    print(f"Processing file: {input_filename}")

if __name__ == "__main__":
    main()
