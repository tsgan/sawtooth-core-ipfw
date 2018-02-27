# sawtooth-core-ipfw

These are some sample PoC codes to distribue FreeBSD ipfw rules on blockchain network using Hyperledger Sawtooth platform.

For installing Hyperledger Sawtooth on FreeBSD:

https://wiki.freebsd.org/HyperledgerSawtooth

Usage samples:

```
root@beast:/home/tsgan/sawtooth-core # bin/ipfw list
RULE NO  ACTION   RULE
root@beast:/home/tsgan/sawtooth-core # bin/ipfw add 65510 pass 'all from 192.168.0.1 to 192.168.0.251'
auth user: None
Response: {
  "link": "http://127.0.0.1:8008/batch_statuses?id=fc794c78854e4bb247fdfef5b0ba3535629bc764443aada640df3bfb872a94c67a5fbd822710afdf0b7803338bb1b27c1c90017dead79814e67526de44459337"
}
root@beast:/home/tsgan/sawtooth-core # bin/ipfw add 65511 drop 'all from 192.168.0.1 to 192.168.0.252'
auth user: None
Response: {
  "link": "http://127.0.0.1:8008/batch_statuses?id=a84639db8c820b028a24ab65a869807bf013ab1a7fe70920b9680e666fcb4d3414037867b6d6027765294da294fdb99ff99fe4a4c4242b75a1c69fdef724e0df"
}
root@beast:/home/tsgan/sawtooth-core # bin/ipfw list
RULE NO  ACTION   RULE
65510    pass     all from 192.168.0.1 to 192.168.0.251
65511    drop     all from 192.168.0.1 to 192.168.0.252
root@beast:/home/tsgan/sawtooth-core # ipfw list | grep 6551
65510 allow ip from 192.168.0.1 to 192.168.0.251
65511 deny ip from 192.168.0.1 to 192.168.0.252
root@beast:/home/tsgan/sawtooth-core # bin/ipfw delete 65510
Response: {
  "link": "http://127.0.0.1:8008/batch_statuses?id=cfabf3a631b950bf8c9e7d21be85599e9dd05f610004de2d4343d959fbb8a31437aa53b12ff59972c996e5e8cb41b6edb733e320b3b2e802936036b17dd49082"
}
root@beast:/home/tsgan/sawtooth-core # bin/ipfw delete 65511
Response: {
  "link": "http://127.0.0.1:8008/batch_statuses?id=f26e7f243de496a47e6661f3177638c8481bb3e83d2763d77597ed976065e1097b5cb1e568525739595ee93cdccbccfbac3d3ccb8a96a7418ca3e69a0e4f92b6"
}
root@beast:/home/tsgan/sawtooth-core # bin/ipfw list
RULE NO  ACTION   RULE
root@beast:/home/tsgan/sawtooth-core # ipfw list | grep 6551
root@beast:/home/tsgan/sawtooth-core #
```

Logs on transaction processor side:

```
[2018-02-27 14:00:10.461 DEBUG    handler] +------------------+
[2018-02-27 14:00:10.462 DEBUG    handler] + Added ipfw rule. +
[2018-02-27 14:00:10.462 DEBUG    handler] +------------------+
[2018-02-27 14:00:10.462 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:00:10.463 DEBUG    handler] +           ipfw rule number: 65511           +
[2018-02-27 14:00:10.463 DEBUG    handler] +                 Action: drop                +
[2018-02-27 14:00:10.463 DEBUG    handler] + Rule: all from 192.168.0.1 to 192.168.0.252 +
[2018-02-27 14:00:10.463 DEBUG    handler] +                                             +
[2018-02-27 14:00:10.464 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:02:57.451 DEBUG    core] received message of type: TP_PROCESS_REQUEST
[2018-02-27 14:02:57.472 DEBUG    handler] +--------------------+
[2018-02-27 14:02:57.473 DEBUG    handler] + Deleted ipfw rule. +
[2018-02-27 14:02:57.473 DEBUG    handler] +--------------------+
[2018-02-27 14:02:57.473 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:02:57.474 DEBUG    handler] +           ipfw rule number: 65510           +
[2018-02-27 14:02:57.474 DEBUG    handler] +                 Action: pass                +
[2018-02-27 14:02:57.474 DEBUG    handler] + Rule: all from 192.168.0.1 to 192.168.0.251 +
[2018-02-27 14:02:57.474 DEBUG    handler] +                                             +
[2018-02-27 14:02:57.475 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:02:58.064 DEBUG    core] received message of type: TP_PROCESS_REQUEST
[2018-02-27 14:02:58.092 DEBUG    handler] +--------------------+
[2018-02-27 14:02:58.094 DEBUG    handler] + Deleted ipfw rule. +
[2018-02-27 14:02:58.095 DEBUG    handler] +--------------------+
[2018-02-27 14:02:58.095 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:02:58.095 DEBUG    handler] +           ipfw rule number: 65510           +
[2018-02-27 14:02:58.095 DEBUG    handler] +                 Action: pass                +
[2018-02-27 14:02:58.096 DEBUG    handler] + Rule: all from 192.168.0.1 to 192.168.0.251 +
[2018-02-27 14:02:58.096 DEBUG    handler] +                                             +
[2018-02-27 14:02:58.096 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:03:04.024 DEBUG    core] received message of type: TP_PROCESS_REQUEST
[2018-02-27 14:03:04.043 DEBUG    handler] +--------------------+
[2018-02-27 14:03:04.044 DEBUG    handler] + Deleted ipfw rule. +
[2018-02-27 14:03:04.044 DEBUG    handler] +--------------------+
[2018-02-27 14:03:04.044 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:03:04.045 DEBUG    handler] +           ipfw rule number: 65511           +
[2018-02-27 14:03:04.045 DEBUG    handler] +                 Action: drop                +
[2018-02-27 14:03:04.045 DEBUG    handler] + Rule: all from 192.168.0.1 to 192.168.0.252 +
[2018-02-27 14:03:04.045 DEBUG    handler] +                                             +
[2018-02-27 14:03:04.045 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:03:04.754 DEBUG    core] received message of type: TP_PROCESS_REQUEST
[2018-02-27 14:03:04.770 DEBUG    handler] +--------------------+
[2018-02-27 14:03:04.771 DEBUG    handler] + Deleted ipfw rule. +
[2018-02-27 14:03:04.771 DEBUG    handler] +--------------------+
[2018-02-27 14:03:04.771 DEBUG    handler] +---------------------------------------------+
[2018-02-27 14:03:04.772 DEBUG    handler] +           ipfw rule number: 65511           +
[2018-02-27 14:03:04.772 DEBUG    handler] +                 Action: drop                +
[2018-02-27 14:03:04.772 DEBUG    handler] + Rule: all from 192.168.0.1 to 192.168.0.252 +
[2018-02-27 14:03:04.772 DEBUG    handler] +                                             +
[2018-02-27 14:03:04.772 DEBUG    handler] +---------------------------------------------+
```

Please note that this PoC codes are not well tested and might need further improvements.

Please use it at your own risk!
