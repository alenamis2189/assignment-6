from __future__ import annotations  # for cool type hinting
from pympler import asizeof

class Node:
    """A simple binary tree node for a basic Huffman encoder."""

    def __init__(self,  symbol: str | None, frequency: int):
        """Object constructor.

        Inputs
        ------
        frequency : int
          The frequency represented by this node. If the node has also a symbol,
          this is the frequency of the symbol. If no symbol is present, this is
          the sum of frequencies of the node's subtrees.
        symbol : char
          The symbol whose frequency we capture. If symbol is None, the node
          captures frequencies for subtrees under the node.

        Returns
        -------
        Instance of Node object with fields:
          frequency : as described above
          symbol : as described above
          left : pointer to left node child (default none)
          right : pointer to right node child (default none)
        """
        self.__frequency: int = frequency
        self.__symbol: str | None = symbol
        self.__left: None | Node = None
        self.__right: None | Node = None

    def __lt__(self, other: Node):
        """Redefine < for node to be based on frequency value"""
        return self.__frequency < other.get_frequency()
    def set_left(self, left: Node | None):
        """Setter for left child."""
        self.__left = left

    def set_right(self, right: Node | None):
        """Setter for right child."""
        self.__right = right

    def has_left(self):
        """Predicate accessor for left child"""
        return self.__left is not None

    def has_right(self):
        """Predicate accessor for right child"""
        return self.__right is not None

    def get_left(self):
        """Accessor for left child"""
        return self.__left

    def get_right(self):
        """Accessor for right child."""
        return self.__right

    def get_symbol(self) -> str:
        """Accessor for the symbol in a leaf node"""
        return self.__symbol
    def get_frequency(self):
        """Accessor for frequency."""
        return self.__frequency

    def is_leaf(self) -> bool:
        """Determines if node is leaf node, indicated by the
        absence of both child pointers."""
        return self.__left is None and self.__right is None

    def __str__(self):
        """String representation of object."""
        return f"[ {self.__symbol}: {self.__frequency} ]"

# Count the frequency of each letter in the message
def count_frequencies(message):
    frequencies = {}
    for char in message:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies

# Convert the data into leaf nodes
def create_a_forest(frequencies):
    forest = []
    for symbol, frequency in frequencies.items():
        node = Node(symbol, frequency)
        forest.append(node)
    return forest

# Build a Huffman tree from the forest
def huffman_algorithm(forest):
  
    while len(forest) > 1:
        n1 = min(forest)
        forest.remove(n1)
      
        n2 = min(forest)
        forest.remove(n2)

        parent = Node(None, n1.get_frequency() + n2.get_frequency())
        parent.set_left(n1)
        parent.set_right(n2)

        forest.append(parent)
    return forest[0]

# Encode the tree
def huffman_tree(root):
    c = {}

    def tree(node, code):
        if node is None:
            return
        if node.is_leaf():
            c[node.get_symbol()] = code
            return

        tree(node.get_left(), code + "0")
        tree(node.get_right(), code + "1")
    tree(root, "")
    return c

# Put together the encoded message
def encode_message(message, code):
    encoded = ""
    for c in message:
        encoded += code[c]
    return encoded

# Decode the encoded bits back to letters
def decode_message(message, root):
    n = root
    decoded = ""
    for c in message:
        if c == "0":
            n = n.get_left()
        else:
            n = n.get_right()
        if n.is_leaf():
            decoded += n.get_symbol()
            n = root
    return decoded

# Calculate the bit sizes
def ascii_size(message):
    return len(message) * 8

def huffman_size(encoded):
    return len(encoded)

# Main
def main():
    # Message test
    print("\nMessage test")
    message = "HELLO WORLD"
    print("Message", message)

    frequencies = count_frequencies(message)
    print("Frequencies:", frequencies)

    forest = create_a_forest(frequencies)
    root = huffman_algorithm(forest)

    code = huffman_tree(root)
    print("Codes:", code)

    encoded = encode_message(message, code)
    print("Encoded message:", encoded)

    decoded = decode_message(encoded, root)
    print("Decoded message:", decoded)

    ascii_bits = ascii_size(message)
    huffman_bits = huffman_size(encoded)
    print("Ascii bits:", ascii_bits)
    print("Huffman bits:", huffman_bits)
    print("Bits saved:", ascii_bits - huffman_bits)

    memory_required = asizeof.asizeof(root)
    print("Tree memory required (ascii):", memory_required * 8)
    print("Tree memory required (huffman):", memory_required)

    # Book test
    print("\nBook test")
    with open("Frankenstein.txt", "r", encoding="utf-8") as f:
        message = f.read()

    frequencies = count_frequencies(message)
    forest = create_a_forest(frequencies)
    root = huffman_algorithm(forest)
    code = huffman_tree(root)
    encoded = encode_message(message, code)

    ascii_bits = ascii_size(message)
    huffman_bits = huffman_size(encoded)
    print("Ascii bits:", ascii_bits)
    print("Huffman bits:", huffman_bits)
    print("Bits saved:", ascii_bits - huffman_bits)

    memory_required = asizeof.asizeof(root)
    print("Tree memory required (ascii):", memory_required * 8)
    print("Tree memory required (huffman):", memory_required)

if __name__ == "__main__":
    main()
