#Bigaray

In windows (Xampp):

httpd.conf
```
LoadFile "C:\Python37\python37.dll"
LoadModule wsgi_module "F:\Martin\bigaray\venv\Lib\site-packages\mod_wsgi\server\mod_wsgi.cp37-win_amd64.pyd"
WSGIPythonHome "C:\Python37"
```
httpd-vhosts.conf
```
<VirtualHost *:80>
    
    WSGIPassAuthorization On
    ErrorLog "logs/bigaray.error.log"
    CustomLog "logs/bigaray.access.log" combined
    WSGIScriptAlias /  "F:\Martin\bigaray\bigaray\wsgi_windows.py"
    <Directory "F:\Martin\bigaray\bigaray">
        <Files wsgi_windows.py>
            Require all granted
        </Files>
    </Directory>

    Alias /backend-static "F:\Martin\bigaray\backend-static"
    <Directory "F:\Martin\bigaray\backend-static">
        Require all granted
    </Directory>

    Alias /images "F:\home\deploy\images"
    <Directory "F:\home\deploy\images">
        Require all granted
    </Directory>

</VirtualHost>
```

copy activate_this.py to venv/Scripts.
