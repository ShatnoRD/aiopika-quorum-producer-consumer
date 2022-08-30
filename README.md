## Installation

In your current project Directory

```bash
pip install -r requirements.txt
```

## Quick-start guide

Host a rabbitMQ server, or use a cloud based solution like [cloudAMQP](https://cloudamqp.com/), and set up an instance to gain a valid AMQP host URL.

Create a ".env" file based on the [Sample](sample.env) for storing the said host URL as AMQP_ADDRESS. Also declare an EXCHANGE_NAME, and two different BINDING_KEY-s, based on the topic exchanged will be routing the messages.
The QUEUE_NAME-s should be unique for each Consumer, but for the sake of the example, I just set a constant string value from them.

You're all set! Simply run [Consumer A](consumer_a.py), [Consumer B](consumer_b.py) scripts in different terminals, keeping it in mind that the [Producer](producer.py) MUST be started after the clients on the first time, otherwise the queues won't be declared server-side, and the exchange, the producer is emitting the messages to, won't be able to route them.

```bash
python .\script.py
```

The [Producer](producer.py) will send a random amount of messages to the declared topic exchange, that will forward them to the correct queues. It can be observed that [Consumer A](consumer_a.py) receives messages sent for both topics, while [Consumer B](consumer_b.py) isn't, since it's listening to a queue bound by only one of the routing keys.

## Output example

```output
python .\consumer_a.py
Message body is:"1# payload sent with topic[binding_key_1]"
Message body is:"2# payload sent with topic[binding_key_1]"
Message body is:"3# payload sent with topic[binding_key_1]"
Message body is:"4# payload sent with topic[binding_key_1]"
Message body is:"1# payload sent with topic[binding_key_2]"
Message body is:"2# payload sent with topic[binding_key_2]"
Message body is:"3# payload sent with topic[binding_key_2]"
```

```output
python .\consumer_b.py
Message body is:"1# payload sent with topic[binding_key_2]"
Message body is:"2# payload sent with topic[binding_key_2]"
Message body is:"3# payload sent with topic[binding_key_2]"

```
