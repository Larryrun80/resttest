# resttest
### Intro
Resttest is aiming to bring automatic test on a Restful api. Resttest is based on [POSTMAN](https://www.getpostman.com) exported files(which using .postman_collection as suffix at this time) , you can also create your own jsone style file using the same format, but we strongly suggest you use POSTMAN output files, not only its very convenient, but also it agree with a test style we recommanded: developers should test their api first. POSTMAN is also convenient for developers, and then they can export configure file and give it to test team. POSTMAN can also help you manage your work properly, via using collecting, etc.
Then we will start our resttest.

### Requirements
Resttest is written based on python 3.5
but I think it will work fine on all python versions above 3.0
Except python,  some other package is needed, I put them in file 'requirements', its a pure requirements and use following command to build your enviroment([pyenv](https://github.com/yyuu/pyenv) and [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv) is recommanded too)
```bash
pip install  -r PATH_TO_REQIREMENTS_FILE
```

### Installation
find a suitable directory in your computer, and then execute this in your terminal:
```
git clone https://github.com/Larryrun80/resttest.git
```

### Structure
In your resttest directory, you will find files and packages as following:
```
resttest\
|
|-- testapp\
|         |
|         |-- models\
|         |
|         |-- utils\
|
|-- testfiles\
|
|-- resttest.py
```

- resttest.py: this is the top executable python file, using ```python resttest.py``` to start your Resttest
- testfiles: this diretory is where you can put your test configure files, Resttest will scan this file and try to analyse if the file obey the POSTMAN rule, and start test automactically if yes. All files not obay the rule will be skipped
- testapp: this diretory contains all models and other codes.

### Quickstart

### Output

### Expectations

### Context

### FAQs