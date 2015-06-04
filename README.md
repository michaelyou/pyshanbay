PyShanb：命令行下的扇贝词典
===========================


fork自[mozillazg](https://github.com/mozillazg/PyShanb)


原来的代码使用的一些扇贝网的API有一些已经不支持了，将其全部换成了新的API，API可以参考[这里](http://www.shanbay.com/developer/wiki/api_v1/)

原来代码中取pyshabay.conf文件路径依赖于环境变量HOME，这样不好，做了修改

把发布工具，生成doc，爱词霸，有道等这些都去掉了，只剩下了代码。

我没有windows的系统，所以把windows相关的也删掉了

##使用

在根目录下

    python shanbay.py -u uername -p password
或者在根目录下

    python -m pyshanb -u username -p password

或者在pyshanb目录下

    python main.py -u username -p password

**Note1** 不想每次都输入用户名密码的话，修改pyshanb.conf文件，将用户名，密码写入其中即可

**Note2** 在shell中键入`q`退出pyshanb

##功能


-  自动登录扇贝网（需要配置用户名及密码）;
-  显示单词中文释义;
-  显示单词英文释义（可选，默认禁用）;
-  自动添加单词到扇贝网词库（当天待背单词列表）（可选，默认禁用）;
-  询问是否添加单词到扇贝网词库（可选，默认启用）;
-  显示例句（显示用户在扇贝网添加的例句）（可选，默认禁用）;
-  配置文件（配置用户名、密码及其他功能项）;
-  通过命令行参数指定配置文件、用户名及密码等;
-  登录后显示用户昵称;
-  添加单词例句（可选，默认启用）;
-  高亮单词及错误信息。





##命令行参数



    >shanbay --hlep
    usage: shanbay.py [-h] [-V] [-s SETTINGS] [-u USERNAME] [-p PASSWORD]
                  [-e | -E]
                  [--color {black,white,red,green,yellow,blue,magenta,cyan,gray}]
                  [--example | --disable-example]
                  [--english | --disable-english]

    An command line tool for shanbay.com.

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -s SETTINGS, --settings SETTINGS
                            the settings file of the application
      -u USERNAME, --username USERNAME
                            the account username of shanbay.com
      -p PASSWORD, --password PASSWORD
                            the account password of shanbay.com
      -e, --add-example     enable "Add example" feature
      -E, --disable-add-example
                            disable "Add example" feature
      --color {black,white,red,green,yellow,blue,magenta,cyan,gray}
                            colorize keyword (default: green)
      --example, --enable-example
                            enable examples
      --disable-example     disable examples
      --english             enable english definition
      --disable-english     disable english definition


