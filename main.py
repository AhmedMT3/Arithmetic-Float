from ArithFloat import ArithFloat

# ==========[ Main ]===========
def main():
    arithCoder = ArithFloat()
    print("Arithmetic Compression Program")
    print("1. Compress a file")
    print("2. Decompress a file")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == '1':
        input_file = input("Enter the name of the file (located in 'Playground'): ").strip()
        try:
            arithCoder.compressToFile(input_file)
        except Exception as e:
            print(f"Error occurred during compression: {e}")

    elif choice == '2':
        arirh_file = input("Enter the name of the .arf file (located in 'Playground'): ").strip()
        try:
            arithCoder.decompressFromFile(arirh_file)
        except Exception as e:
            print(f"Error occurred during decompression: {e.with_traceback()}")
    
    elif choice == '3':
        data = input("Enter Data: ")
        code, symbols = arithCoder.Compress(data)
        print("Code: ", code)
        for symbol in symbols:
            print(symbol)
        
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
