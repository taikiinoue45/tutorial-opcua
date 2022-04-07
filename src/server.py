import logging
import asyncio
import sys
import time
import random
sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod

@uamethod
def func(parent, value):
    return value * 2

async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://localhost:4840')

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, 'MyObject')
    mycount = await myobj.add_variable(idx, 'MyCount', 6.7) # 数値は初期値
    myclock = await myobj.add_variable(idx, "MyClock", 0.0)
    mytemperature = await myobj.add_variable(idx, "MyTemperature", 0.0)

    # Set MyVariable to be writable by clients
    await mycount.set_writable()
    await myclock.set_writable()
    await mytemperature.set_writable()
    await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(5)

           # データを送信（生成）した回数を0.1刻みでカウントして送る
            count = await mycount.get_value() + 0.1
            print('count: ' + str(count))
            _logger.info('Set value of %s(COUNT) to %.1f', mycount, count)
            await mycount.write_value(count)

            # CPUクロックを取得する
            # Cloud9では vcgencmd コマンドが使えないのでランダムな数値をダミーデータとして利用する
            await myclock.set_value(0.0)
            clock = await myclock.get_value() + random.randint(600000000,1500000000)
            _logger.info('Set value of %s(CLOCK) to %.1f', myclock, clock)
            print('clock: ' + str(clock))
            await myclock.write_value(clock)

            # CPU温度を取得する
            # Cloud9では vcgencmd コマンドが使えないのでランダムな数値をダミーデータとして利用する
            await mytemperature.set_value(0.0)
            temperature = await mytemperature.get_value() + random.uniform(30, 85)
            _logger.info('Set value of %s(TEMPERATURE) to %.1f', mytemperature, temperature)
            print('temperature: ' + str(temperature))
            await mytemperature.write_value(temperature)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)
