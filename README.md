# resttest
### Intro
Resttest is aiming to bring automatic test on a Restful api. Resttest is based on [POSTMAN](https://www.getpostman.com) exported files(which using .postman_collection as default suffix at this time) , you can also create your own jsone style file using the same format, but we strongly suggest you use POSTMAN output files, not only its very convenient, but also it agree with a test style we recommanded: developers should test their api first. POSTMAN is also convenient for developers, and then they can export configure file and give it to test team. POSTMAN can also help you manage your work properly, via using collections, etc.

Another function of resttest is monitoring your online service, you can send request to important inferfaces periodically (with crontab or other tools) and see if those serivces are provided correctly.

Then we will start our resttest.

### Requirements
Resttest is written based on python 3.5

but I think it will work fine on all python versions above 3.0

Except python,  some other packages are needed, I put them in file 'requirements', using following command to build your enviroment([pyenv](https://github.com/yyuu/pyenv) and [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv) is recommanded too)
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
|
|-- requirements
```

- resttest.py: this is the top executable python file, using ```python resttest.py``` to start your Resttest
- requirements: this file include all packages you will need to run Resttest properly
- testfiles: this diretory is where you can put your test configure files, Resttest will scan this directory and try to analyse files if it obey the POSTMAN rule, if yes, it will start test automactically. All files not obay the rule will be skipped
- testapp: this diretory contains all models and other codes

### Quickstart

### Output

### Expectations
"Expectations" is the most core conception in resttest.

We using "expectations" to manage whether interfaces response correctly as we want. Now resttest supports four types of expectations: ["status_code", "include_keys", "include_words", "value"].

##### How to implement an expectation
To enable expectation, we need to add an "expectations" key in a request dictionary. Value of this key must be a list, and every expectation as a dictionary in this list.

For example:
<pre>
{
    "id": "abcd-abc-abc-abc-abcdef",
    "name": "example of exceptation",
    "description": "in this example, you can see we implement expectations in every request dictionary",
    "order": [
            "some-request-id-to-run-firstly",
            "some-request-id-to-run-secondly"
    ],
    ......
    requests: [
        {
            "id": "some-request-id-to-run-firstly",
            "name": "some-request-to-run-firstly",
            "method": "GET",
            "url": "some url to request",
            ......<font color="red"><b>
            "expectations": [
                {
                    "type": "status_code",
                    "value": 200
                }
                ... other expectations
            ]</b></font>
        }
        ......
    ]
}
</pre>

1. "status_code"

    This type is used to see if the responsed http status code is correct.

    format for using this type is:
```
    {
        "type": "status_code",
        "value": 200
    }
```
    you can replace 200 with any valid http status code if you want. resttest will return "passed" if response code is the value you set, or "failed" if they are not matching.

2. "include_keys"

    This type is used to check if a key include in specific responsed data.

    format for using this type is:
```
    {
        "type": "include_keys",
        "pos": ".",
        "value": ["key1", "key2", ...]
    }
```
    **here we meets an important concept: "pos"**, you will use "pos" in all exceptation types except "status_code". "pos" indicate which json level we will implement our exceptation. Every "pos" value should start with '.', and this means the root level of the json data.

    "pos" in "include_keys" tell resttest where to find the key we want. Assuming we get following response when request a book's info:
```
    {
        "bookname": "Nineteen Eighty-Four"，
        "market price": 20,
        "language": "English"
        "author": 
        {
            "name": "George Orwell",
            "novels": [
                "Animal Farm",
                "Nineteen Eighty-Four",
                "Coming Up for Air"
            ]
        }
        "editions": [
            {
                "type": "hard cover",
                "price": 20
            }
            {
                "type": "paper back",
                "price": 9
            }
            {
                "type": "kindle edition",
                "price": 3
            }
        ],
        "timestamp": 1450432485
    }
```
    Resttest will return true if you expect "include_keys" "bookname" in pos ".", or "include_keys" "price" in pos ".editions", or "include_keys" "novels" in pos ".author"

    In "value", you can put a list of key you want. Make sense that if you only want to check one key, you need to build a list, too. As `"value": ["key"]`. Resttest will create an exceptation for every key.

    Last thing we will metion is, as the example, "include_keys" will search both dictionay and list type value of a key, if you want it work on a list type, such as the pos ".editions", resttest will return "passed" only if all elements in the list has that key. 

3. "include_words"

    This type is used to check if a string is include in specific responsed data. Usage of this type is similar with "include_keys", see example:
```
    {
        "type": "include_words",
        "pos": ".",
        "value": ["words 1", "words 2", ...]
    }
```
    If we using the sample book-info response in "include_keys" section, resttest will return true if you expect "include_words" "George Orwell" in pos "."/".author" , or "include_words" "kindle edition" in pos "."/".editions"

4. "value"

    This type is used to check if a returned value meets our expectation. Now "value" type supports following camparison: 
    - equal: "="
    - not equal: "!=" 
    - greater than: ">"
    - greater than or equal: ">="
    - less than: "<"
    - less than or equal: "<=" in
    - in: "in"

    see examples, using book-info response in "include_keys" section:
```
    {
        "type": "value",
        "left": ".timestamp",
        "op": ">=",
        "right": 0
    }
    {
        "type": "value",
        "left": ".market price",
        "op": ">=",
        "right": ".editions.price"
    }
    {
        "type": "value",
        "left": ".language",
        "op": "in",
        "right": ["English", "Franch", "Chinese"]
    }
```
    In "value" type, we use 3 new parameters: "left", "right", and "op". "left"/"right" is left/right part of an comparison expression，and "op" stands for operation. "left"/"right" can be a value of specific key in response (same format as "pos" in "include_keys"/"include_words") or a number, make sense that all value of left/right should be number except "in" operator. 

    First expactation indicates timestamp should >0, second indicates market price of the book should greater than or equal all selling editions, third indicates book language should be "English" or "Franch" or "Chinese".

### Context
"Context" is another important concept of resttest. In an intergrated test process, params passed between tests is inevitable. For example, think if we want to get user infomation, the interface always asked for a user token, so we must access a login or regist interface first, get user's access token and than use it to get user information. In resttest, it's "context" help user implement such message dilevery between interface tests. Without "context", you must interrupt test process manually to change access information.

"Context" include two parts: "defination" and "usage". "Defination" is where we assign params to be delivered, and "usage" is where these params are used to request a http interface.

1. defination of context
"Defination" will be put at the top level of your json data, see following example:
<pre>
{
    "id": "id-of-postman-collection",
    "name": "example of context",
    "order": [
        "some-test-id-should-be-firstly-run",
        "some-test-id-should-be-secondly-run"
        ...
    ],<font color="red"><b>
    "context": [
        {
            "name": "mobile",
            "request": [],
            "default": "10955832"
        },
        {
            "name": "token",
            "request": [
                {
                    "id": "some-request-id",
                    "path": ".data.key"
                }
            ],
            "default":  ""
        }
        ...
    ],</b></font>
    "requests": [
        {
            "id": "some-test-id-should-be-firstly-run",
            "name": "1st run test",
            "method": "GET",
            "data": [],
            "url": "https://url-of-test/{token}/",
            "collectionId": "id-of-postman-collection",
            "expectations": []
        }
        ...
    ]
}
</pre>
In this example, we can find every context will include three key-value pair: "name", "request" and "default".

"name" is a global unique key to indicate which context we should define and use. "request" includes a list, which indicate we can get context value in which request(via request id) and then which path in the response. "default" is the default value if we haven't received any response to update this context value, you can also use "default" to set static variables(like "mobile" context in our example, with no request set).

Make sense the value of context will never be set in this config file. Our program will read context info when execute this file and then update the corresponde value in memory.

2. usage

After we defined these contexts, we and use them in anywhere you want in request section. Remember to use "{context_name}" to indicate what you want is a context value, see the url part of above example(in requests section).

Another thing must be mentioned is we using a request list in context defination. This mean every request in the list will update the context value. 


### FAQs













