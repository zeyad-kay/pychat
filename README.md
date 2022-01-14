# PyChat

Healthcare Chatbot that advices patients for visiting clinics depending on patients complaints.
# Setup

1. From the command line create a virtual environment and activate.
```sh
# Windows
> python -m venv .venv
> .venv\Scripts\activate

# Linux
> python3 -m venv .venv
> source .venv/bin/activate
```

2. Install server dependencies.
```sh
> pip install -r server/requirements.txt
```

3. Create an environment variables file and enter the database and email credentials for the server to use for tokens e.g.:
```sh
MONGO_URI=<mongodb connection>
EMAIL_HOST=<mail host>
SENDER_EMAIL=<sender email>
SENDER_PASSWORD=<sender password>
```
Instead of using your personal email, visit [Ethereal](https://ethereal.email/). It creates a dummy account that simulates sending and recieving email. When running the client use the generated email to be able to view the token. Sometimes it doesn't catch emails or takes too long, in that case, just restart the server.

If you don't have a local MongoDB set up, you can create one for free on [MongoDB](https://www.mongodb.com/).

4. Run the server.
```sh
> python server/server.py <env-vars-file-path>
```

5. Run the client.
```sh
> python client/cli.py
```
