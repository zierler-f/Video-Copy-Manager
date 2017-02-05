# Video Copy Manager
The Video Copy Manager is a tool which helps the user manage videos in different directories. It searches a source directory, and a target directory for video files recursively can do multiple things with videos missing in target:

* print out filenames of videos only present in source
* copy missing videos from source to target

## Prerequisites

In order to be able to download & run Video Copy Manager, the following tools/programs need to me installed on your machine:

* Git
* Python3

## Download

To download Video Copy Manager run the following command in a shell of your choice:

```sh
$ git clone https://github.com/zierler-f/Video-Copy-Manager.git
```

## Run

After downloading, Video Copy Manager is ready to run. To do so go to the root directory of the project, open a  shell and type:

```sh
$ python3 videocopymanager.py <run-type> <source> <target> [<cp-target> <ignore-file>]
```

And replace the placeholders as follows:

* Only <run-type>, <source> and <target> have to be provided, <cp-target> and <ignore-file> are optional, and therefore can be left out completely.
* Replace <run-type> with either "show", "cp" or "ln". If the first argument is anything different, it won't work.
* Replace <source> with the path to a directory containing the video files, the users wants copied.
* Replace <target> with the path to a directory where you want all video files from source copied to.
* Optionally replace <cp-target> with the path to a directory within <target> if you don't want all videos files which will be copied in the root of <target>, but rather somewhere else.
* Optionally replace <ignore-file> with the path to a file containing filenames of all video files the user does not want to be copied, although the are missing.

Examples:

```sh
$ python3 videocopymanager.py show /home/user/Downloads /home/user/Videos
```

will print out all filenames of video files, which are present in /home/user/Downloads, but are not present in /home/user/Videos.

```sh
$ python3 videocopymanager.py cp /home/user/Downloads /home/user/Videos /home/user/Videos/New /home/user/Videos/.vcmignore
```

will first find all video files from /home/user/Downloads, which are missing in /home/user/Videos. Then it will compare the list of missing files with all lines from /home/user/Videos/.vcmignore and if a line matches a filename, the file will be dropped from the missing files list. The remaining files will then be copied to the /home/user/Videos/New directory.

### Run Types

Video Copy Manager has 3 modes:

* show
    * Just prints out names of missing video files
* cp
    * Copies missing video files from source to target
* ln
    * Creates a hard link from the missing video files from source, in target