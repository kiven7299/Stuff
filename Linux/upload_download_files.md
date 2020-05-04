- With `ssh`: `cat $filename | ssh user@host "cd /path/to/upload/files/to; cat - > $filename"`

- With `curl`: 

  - $server: create simple http server with python: `python -m SimpleHttpServer <listened port>`

  - $client: `curl -o <file name> <url to file on server>`


    

- With `netcat`:

  ```sh
  server$ cat test.dat | nc -q 10 -l -p 7878
  client$ nc -w 10 remotehost 7878 > out.da
  nc -w 10 192.168.182.162 7878 > out.exe
  ```

- With `socat`:

  - Server sending file:

    ```sh
    server$ socat -u FILE:test.dat TCP-LISTEN:9876,reuseaddr
    client$ socat -u TCP:127.0.0.1:9876 OPEN:out.dat,creat
    ```

  - Server receiving file:

    ```sh
    server$ socat -u TCP-LISTEN:9876,reuseaddr OPEN:out.txt,creat && cat out.txt
    client$ socat -u FILE:test.txt TCP:127.0.0.1:9876
    ```

