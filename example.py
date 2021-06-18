from roomlib import Host

host = Host(PORT, USERS, PASSWORD)

for status in host.wait(TICK):
    sleep()

host.set_values(KEY1=VALUE1, KEY2=VALUE2, ... , KEYn=VALUEn)

host.sync()
host.sync(USERID)

host.get_value(KEY)

host.send(VALUE)
host.send(VALUE, [USERID])

host.finish()


####


from roomlib import Client

client = Client(PORT)

rooms = client.search()
status = client.join(ROOMID, PASSWORD)

client.set_values(KEY1=VALUE1, KEY2=VALUE2, ..., KEYn=VALUEn)

client.sync()

client.get_value(KEY)

client.set_receiver(FUNC)

client.exit()


####

## Request Format
{
   "command": "join/finish/sync",
   "user": {
       "id": "AAAAA",
       "port": 11111
   },
   "auth": {
       "password": ""
   },
   "values": {
       "key": "value"
   }
}

## Response Format
{
    "result": {
        "status": True or False,
        "msg": "AAAAA"
    }
}

###

- 50000 : tcp
- 50001 : udp