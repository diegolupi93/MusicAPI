# MusicApi

### Run the code
To run the code you must have installed docker and docker-compose. Run 
into the terminal following command is to run the code:

> $ docker-compose build --no-cache && docker-compose up

### Test Manually
To Test the app Run the code after that go to **localhost:5000** and try, for example:

[http://localhost:5000/artist?name=coldplay](http://localhost:5000/artist?name=coldplay)

### Run the test
To run the code you must have installed virtualenv. Run 
into the terminal following command is to run the test:

> $ python3 -m venv venv

> $ source venv/bin/activate

> $ pip install -r requirements.txt

> $ pytest test.py
