Citadel-Python-Client.

This is a library to access Citadel servers from Python using the Citadel Protocol.


          Python : http://www.python.org
         Citadel : http://www.citadel.org
Citadel Protocol : http://www.citadel.org/doku.php/documentation:applicationprotocol

 - tcp.py defines a fairly generic TCP client in the Client class.
 - api.py implements the Citadel Protocol on top of tcp.Client.
 - citadel.py is the high level Citadel interface.
 - tpl.py contains templates needed by the Citadel client.

 You shouldn't have to worry about tcp.py, api.Protocol is the class where you would implement missing parts of the low level Citadel Protocol and citadel.py should be the only module you need to import and adapt to your needs.

 When you instenciate the Citadel class, you may pass it a config object (typically a module).
 The config object may have the following attributes:
  . server_adr  : the Citadel server adr
  . server_prt  : the Citadel server port
  . admin_login : admin login           
  . admin_psw   : admin password       
  . log         : log file            
If server_adr is omitted localhost will be used, server_prt defaults to 504.
If admin login or password are not specified, you will be asked for them as needed.
If log is not specified (or evaluate to False) nothing will be logged.
