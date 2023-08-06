sqlwitch is a Python 2.5+ library that offers idiomatic SQL generation on top 
of MySQLdb[1]. Like xmlwitch[2] and html5witch[3], it aims to provide a 
natural, Pythonic syntax that benefits from context managers. 

To install, just run "pip install sqlwitch", "easy_install sqlwitch" or copy 
**sqlwitch.py** to your appropriate project's directory. It's just one file.
 
    with db.insert(into='foobars') as obj:
        obj.foo = 1
    
    with db.select('foo, bar', from_='foobars'):
        db.where('foo = 1')
    
    with db.update('foobars') as changeset:
        changeset.foo = 2
        db.where('foo = 1')
    
    with db.delete(from_='foobars'):
        db.where('foo = 2')
   
Please refer to 

  http://jonasgalvez.com.br/Software/SQLWitch.html 
  
for further info.

Pull requests are welcome.

[1] http://sourceforge.net/projects/mysql-python/
[2] http://jonasgalvez.com.br/Software/XMLWitch.html
[3] http://jonasgalvez.com.br/Software/HTML5Witch.html