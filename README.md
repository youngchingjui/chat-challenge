# Chat Challenge

The "chat challenge" is to create a basic terminal-based chatbot by integrating with some simple services (included in this repo).

## What to build

A solution to perform basic customer support needs.

A user should be able to run the program via main.py and interact with it in the command line with something like `$ python3 main.py`. Input from the user should be typed there and submitted to the program when they press enter. 

Users should be able to get 3 main kinds of help from the program:

1. Get product information
2. Technical support for a problem on the product they bought
3. Speak with a real person

For two of the services results are streamed back to the client. In these cases data should be printed as it is streamed, but only in usable chunks, which are defined as being wrapped in html p tags.

## Example interactions

Product questions: If the user text has the words "product question" in it, you should take that to mean it is a request for product information. See which known-product they are asking about and give the response. Here's how that interaction should look: 

```shell
> I have a product question about Antigravity Socks

<p>Self-levitating socks that float gently in your drawer.</p>
<p>Never lose a sock again - they actively seek their matching pair!</p>
<p>WARNING: Do not wear during thunderstorms or solar flares.</p>
```


Technical support: If the user text has the words "help" in it, you should take that to mean it is a request for technical support. See which known-issue they are asking about and give the response. Here's how that interaction should look: 

```shell
> I need help with my product. It has a flashing red light. What should I do?

<p>If you notice a flashing red light on your device, it is important to take immediate action to address the issue.</p>
<p>This flashing light often indicates that there is a problem that needs to be resolved, and ignoring it could lead to further complications.</p>
<p>To begin troubleshooting, unplug the device from the power source, wait for at least 30 seconds, and then plug it back in to see if the issue persists.</p>
<p>After reconnecting the device, observe whether the red light continues to flash or if it returns to a normal state.</p>
<p>If the light remains flashing, it may be necessary to consult the user manual or contact customer support for further assistance.</p>
<p>In some cases, a flashing red light can signify a hardware failure, so it is crucial to address the situation promptly.</p>
```


Real agent: If the user text has the words "real person" in it, you should take that to mean they want to be transferred to a real person. Here's how that interaction should look: 
```shell
> I would like to speak with a real person please.

Excellence in service creates loyal customers.
```

Notice that all the services have extremely simple single-phrase interactions. This is meant to keep things small for the challenge.

## Streaming, service differences, and a buggy third-party service

The services can be (intentionally for the challenge) slow at processing. To give users faster results, responses are streamed for two of the services. It is important to start giving them that data as soon as possible, but only print complete chunks/paragraphs.

## Some technical details to help

The three big functions for the program are done using simulated services. These can be found in `cheap_gpt.py`, `product_info_bot.py`, and `real_agent.py`. Each of those files are extremely basic programs meant to simulate services to carry out the different types of interactions. Treat these programs/services as if they were third-party external services. The code is only here to make challenge setup easier to see as a whole. No changes should be made to these. Each service can be run like this:

```
python3 cheap_gpt.py # Runs on port 8081 and url of http://localhost:8081/
python3 product_info_bot.py # Runs on port 8082 and url of http://localhost:8082/
python3 real_agent.py # Runs on port 8083 and url of http://localhost:8083/
```

## Important concepts

- As with all code, it is expected that a team can work on it and extend it over time
  - Unit testing is important
  - The design of the code should bring simplicity to the problem
- Idiomatic language usage is ideal. If you are new to Python, work with what you know and we'll talk about the difference when we meet.
- Code this as you would if it were real code you expected to put into production