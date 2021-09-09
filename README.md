# tssh
clusterssh like behaviour for tmux

## Usage
Clone this repo and load the wrapper in your `bashrc`
```
cd /some/dir/to/clone
git clone https://github.com/rohm1/tssh
echo "source $(pwd)/tssh.sh\n" >> ~/.bashrc
```

Create a `~/.clusterssh/clusters` file. This is a whitespace separated file, one cluster per line. First item is the name of your cluster, following items are the names of the servers in the cluster. The name of the servers must be known to ssh (typically through `~/.ssh/config`).

Example:
```
mycluster server1 server2 server3
```
```shell
tssh mycluster
```

The shell wrapper supports autocompletion for the clusters. In case you do not want to use `~/.clusterssh/clusters`, you can define a config in the optional file `~/.tssh.json`:
```json
{
    "cssh_file_path": "~/.clusterssh/clusters"
}
```
