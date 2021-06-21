from roomlib import Host

host = Host(NAME, PORT, USERS, PASSWORD)

while True:
    if host.wait(TICK, PORT):
        break

host.get_value(KEY)

host.set_values(KEY1=VALUE1, KEY2=VALUE2, ... , KEYn=VALUEn)

host.sync()

host.send(VALUE, [USERID])

host.finish()


####


from roomlib import Client

client = Client(PORT)

rooms = client.search(TICK, PORT)
status = client.join(ROOMID, PASSWORD)

client.get_value(KEY)

client.set_values(KEY1=VALUE1, KEY2=VALUE2, ..., KEYn=VALUEn)

client.sync()

client.finish()


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
    "command": "AAAAA"
    "result": {
        "status": True or False,
        "msg": "AAAAA"
    }
}

###