# Blue Apron Cronometer Import Tool
I have recently been using the website Cronometer to track meals and nutrition
information, but I found an issue with the Blue Apron meal delivery service
not being able to be imported into Cronometer. While I could manually enter
the data every week, what fun is that when I'm a programmer?

So, this utility is intended to run as a very simple web server that will
take a Blue Apron URL, parse out the recipe ingredients, and generate a
format that can be imported into Cronometer.

This is done by using Selenium, as a simple curl/requests to Blue Apron does
not appear to actually give the recipe.

## Usage
My usage is as follows:

### Build the Docker image
Use the following command to build a Docker image
```
docker build -t ba .
```

### Run the Docker image
```
docker run -p 8080:10000 ba
```