![Local Image](diagram.png)

Running the Code

We can run this simple CI system locally, using three different terminal shells for each process. We start the dispatcher first, running on port 8888:
```
$ python dispatcher.py
```
In a new shell, we start the test runner (so it can register itself with the dispatcher):
```
$ python test_runner.py <path/to/test_repo_clone_runner>
```
The test runner will assign itself its own port, in the range 8900-9000. You may run as many test runners as you like.

Lastly, in another new shell, let's start the repo observer:
```
$ python repo_observer.py --dispatcher-server=localhost:8888 <path/to/repo_clone_obs>
```
Now that everything is set up, let's trigger some tests! To do that, we'll need to make a new commit. Go to your master repository and make an arbitrary change:
```
$ cd /path/to/test_repo
$ touch new_file
$ git add new_file
$ git commit -m"new file" new_file
```
Then repo_observer.py will realize that there's a new commit and notify the dispatcher. You can see the output in their respective shells, so you can monitor them. Once the dispatcher receives the test results, it stores them in a test_results/ folder in this code base, using the commit ID as the filename.