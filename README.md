# simple_text_compression

Creates a compressed file given a .txt file.  
Uses a tree based on frequency of individual characters.  
The .compressed file contains the tree and compressed message.  

.compressed file layout in order:  
byte0-1: Integer value of compressed tree length in bytes  
Tree: List of tuples of the form (character, key).  
-- First byte is character.  
-- Next bit if 0, next 15 bits are char key, if 1, next 31 bits are char key  
Text: Text in compressed form.  
-- Compressed text begins after first on bit  
