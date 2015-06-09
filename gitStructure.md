###Server:
1. git-server</br>
Directory: `/home/lxw/gitLib/monitorURL`</br>
Command:</br>
`git init --bare`</br>
&</br>
_execute on the client side_
```
git remote add origin lxw@218.241.xyz.ab:/home/lxw/gitLib/monitorURL
git push origin master
```

2. git-client</br>
Directory: `/home/lxw/monitorURL`</br>
Command: `git pull /home/lxw/gitLib/monitorURL`</br>

###Local:
1. git-client</br>
Directory: `/home/lxw/monitorURL`</br>
Command: `git pull lxw@218.241.xyz.ab:/home/lxw/gitLib/monitorURL`</br>
