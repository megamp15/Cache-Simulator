# Cache-Simulator
### Computer Organization Project: Simulating a Cache using a high-level language. 


### Instructions:

Run the program by entering python3 runner, cachesimulator.py, and input file.

```console 
python cachesimulator.py input.txt
```
The main function shall proceed to call the other functions.

After intialization of RAM from the input file, user will be prompted to configure the cache.

Ranges for input:

    Cache size: 8 bytes to 256 bytes
    Associativity: 1, 2, or 4 (way set associative cache)
    Replacement Policy: -> evicts non-valid lines before valid lines
        1 == Random Replacement -> the non-valid lines are chosen at random instead of linearly until all lines are valid. 
                                   Once all lines are valid then any line can be chosen to be evicted.
        2 == Least Recently Used
        3 == Least Frequently Used
    Write Hit Policy: 
        1 == Write-through -> write the data in both the block in cache and the block in RAM
        2 == Write-back    -> write the data only in the block in cache
    Write Miss Policy:
        1 == Write-allocate      -> load the block from RAM and write in in the cache
        2 == No Write-allocate   -> write the block in RAM and do not load it in the cache

After successfully configuring the cache, the user will be prompted with a MENU of commands that repeats until the quit command is entered:
    
    '''*** Cache simulator menu ***
    type one command:
    1. cache-read
    2. cache-write
    3. cache-flush
    4. cache-view
    5. memory-view
    6. cache-dump
    7. memory-dump
    8. quit
    ****************************'''
    Please type the name of the command only such as cache-flush and any arguments that may be required as outlined below:
    Argumemt commands:
        1. cache-read  -> takes a single argument for the address of the data to be read from cache or RAM if it is a miss. Ex) cache-read 0x00
        2. cache-write -> takes two additional arguments the address and the data to be written into the Cache or RAM. EX) cache-write 0x10 0xAB
    No arguments for the below commands:
        3. cache-flush  -> clears the cache
        4. cache-view   -> display cache content and status
        5. memory-view  -> display RAM content and status
        6. cache-dump   -> dump the current bytes of data in the cache into cache.txt file. Will be created if it does not exist.
        7. memory-dump  -> dump the RAM data contents in a ram.txt file similar to input file. Will be created if it does not exist.
        8. quit         -> command to exit the program.
