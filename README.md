# simple_text_compression

Creates a compressed file given a .txt file.  
Uses a tree based on frequency of individual characters.  
The .compressed file contains the tree and compressed message.  

.compressed file layout in order:  
byte0: Integer value of tree length  
Tree : List of tuples of the form (character, key).  
-- First byte is character.  
-- Next two bytes are key, starting after first on bit  
Text : Text in compressed form.  
-- Compressed text begins after first on bit  
