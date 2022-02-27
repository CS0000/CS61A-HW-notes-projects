# CS61A-HW-notes-projects
#### python interactive mode    
`$ python3 -i XXX.py`    
> -i:    
> inspect interactively after running script; forces a prompt even if stdin does not appear to be a terminal;
          
#### test domo               
`$ python3 -m doctest -v XXX.py`
> -m doctest -v
> simulate session, demo the example in function's doc. Invoke the doc test module on a particular `.py` file.       

#### local variable 'x' referenced before assignment      
you can't have the same local and a global name at the same time, in a function


