import os
import re

class Symbol:
    def __init__(self, char, prob, low, high) -> None:
        self.char = char
        self.prob = float(prob)
        self.low = float(low)
        self.high = float(high)
        
    def __repr__(self) -> str:
        return f"Char: {self.char}, Prob: {self.prob}, Low: {self.low}, High: {self.high}"

class ArithFloat:
    
    def calcProb(self, input_text):
        probs = {}
        for char in set(input_text):
            count = input_text.count(char)
            probs[char] = count / len(input_text)
        return probs

    def convertToSymbols(self, input_text):

        probs = self.calcProb(input_text)

        cumulative = 0.0
        symbols = []
        for char, prob in sorted(probs.items()):
            symbols.append(Symbol(char, prob, cumulative, cumulative + prob))
            cumulative += prob

        return symbols

    # ==========================[ Compress ]=============================

    def Compress(self, data):
        symbols = self.convertToSymbols(data)
        symbol_map = {s.char: s for s in symbols} # {'a': S(A)}

        lower_bound = 0.0
        upper_bound = 1.0

        for char in data:
            symbol = symbol_map[char]
            range_width = upper_bound - lower_bound

            temp_lower = lower_bound + range_width * symbol.low
            upper_bound = lower_bound + range_width * symbol.high
            lower_bound = temp_lower

        code = (lower_bound + upper_bound) / 2
        return code, symbols

    # ==========================[ Decompress ]=============================
    
    def deCompress(self, code, symbols, length):
      
        decoded = []
        value = float(code)

        for _ in range(length):
            for symbol in symbols:
                if symbol.low <= value <= symbol.high:
                    decoded.append(symbol.char)
                    lower = symbol.low
                    upper = symbol.high
                    range_width = upper - lower
                    value = (value - lower) / range_width
                    break
            else:
                raise ValueError(f"Code Value {value} out of range for all symbols!")

        return ''.join(decoded)

    # ==========================[ Compress to File ]=============================

    def compressToFile(self, input_file, file_path=None):
        try:
            with open(os.path.join('Playground', input_file), 'r') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: {input_file} not found in 'Playground/' directory.")
            return

        if not data.strip():
            raise ValueError("Input file is empty!!")

       
        code, symbols = self.Compress(data)

       
        if not file_path:
            base_name, ext = os.path.splitext(input_file)
            file_path = f"{base_name}.arf"

        
        with open(os.path.join('Playground', file_path), 'w') as f:
            f.write(f"{ext}\n")
            f.write(f"{len(data)}\n")
            f.write(f"{code}\n")
            for symbol in symbols:
                escaped_char = symbol.char.replace('\\', '\\\\').replace(',', '\\,').replace(' ', '\\s')
                f.write(f"{escaped_char},{symbol.prob},{symbol.low},{symbol.high}\n")


        return file_path

    # ==========================[ DeCompress to File ]=============================

    def decompressFromFile(self, compressed_file, output_file=None):
        try:
            with open(os.path.join('Playground', compressed_file), 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: {compressed_file} not found in 'Playground/' directory.")
            return

        try:
            if len(lines) < 3:
                raise ValueError("Compressed file is not in the correct format")

            ext = lines[0]
            length = int(lines[1])
            code = float(lines[2])
        except (ValueError, IndexError) as e:
            print(f"Error parsing header: {e}")
            return

        symbols = []
        for line in lines[3:]:
            try:
                # Split only the first three commas
                char_parts = re.split(r'(?<!\\),', line, maxsplit=3)
                if len(char_parts) == 4:
                    char = char_parts[0].replace('\\\\', '\\').replace('\\,', ',').replace('\\s', ' ')
                    prob = float(char_parts[1])
                    low = float(char_parts[2])
                    high = float(char_parts[3])
                    
                    symbols.append(Symbol(char, prob, low, high))
            except ValueError:
                print(f"Skipping invalid symbol line: {line}")
                continue

        if not output_file:
            base_name = os.path.splitext(compressed_file)[0]
            output_file = f"{base_name}{ext}"

        try:
            decoded_data = self.deCompress(code, symbols, length)
        except ValueError as e:
            print(f"Decompression error: {e}")
            return

        with open(os.path.join('Playground', output_file), 'w') as f:
            f.write(decoded_data)

        return output_file