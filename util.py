# ---------------------------------------------------
#    Name: FATIMA REHMATULLAH
#    ID: 1631703
#    CMPUT 274, Fall  2020
#    Assignment 2: Huffman Coding
# --------------------------------------------------
import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    d = pickle.load(tree_stream)
    return(d) 

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    #isintance checks for the type of the tree, leaf or branch
    if isinstance(tree,huffman.TreeLeaf):
      return tree.getValue()
    #reading one bit at a time 
    bit = bitreader.readbit()
    if bit:
      #recursive function calls to decode_byte
      return decode_byte(tree.getRight(),bitreader)
    return decode_byte(tree.getLeft(),bitreader)
    pass


def decompress(compressed, uncompressed):
    '''First, read a .Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    compressedtree = read_tree(compressed)
    #instantiates objects of the reader and writer
    bitreader = bitio.BitReader(compressed)
    bitwriter = bitio.BitWriter(uncompressed)
    error = False
    try:
      while not error:
        result = decode_byte(compressedtree,bitreader)
        #writes a whole byte at a time
        if result != None:
          bitwriter.writebits(result,8)
        else:
          error = True
      #flushing the bit writer after running
      bitwriter.flush()
    except EOFError:
        pass

def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree,tree_stream)
    pass

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    write_tree(tree,compressed)
    bitwriter = bitio.BitWriter(compressed) #instantiate object of writer
    bitreader = bitio.BitReader(uncompressed) #instantiate object of reader
    encoding_table = huffman.make_encoding_table(tree) #get encoding table

    end_of_file=False
    while not end_of_file:
      try:
        byte = bitreader.readbits(8) #read a byte at a time
        encoding_tuple = encoding_table[byte]
        for bit in encoding_tuple: #replace with the path from the table
          bitwriter.writebit(bit)
      except:
        end_of_file = True
        encoding_tuple = encoding_table[None] #takes care of the none condition 
        for bit in encoding_tuple:
          bitwriter.writebit(bit)
    bitwriter.flush() #flushing the writer after writing