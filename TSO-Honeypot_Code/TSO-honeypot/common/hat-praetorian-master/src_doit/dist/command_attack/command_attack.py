import asyncio
import click
import contextlib
import sys

from hat import aio
from hat.drivers import tcp
from hat.drivers.iec60870 import apci
from hat.drivers.iec60870 import iec104


@click.command()
@click.option('--host', type=str, default=None, required=True)
@click.option('--port', type=int, default=None, required=True)
@click.option('--asdu', type=int, default=None, required=True)
@click.option('--io', type=int, default=None, required=True)
@click.option('--value', type=click.Choice(['OFF', 'ON']), default=None, 
              required=True)
def main(host, port, asdu, io, value):

    with contextlib.suppress(asyncio.CancelledError):
        aio.run_asyncio(async_main(host, port, asdu, io, value))


async def async_main(host, port, asdu, io, value):
    print(f'trying to connect to {host}:{port}')
    conn_apci = await apci.connect(
            addr=tcp.Address(host=host,
                             port=port))
    conn = iec104.Connection(conn_apci)

    print(f'connected to {host}:{port}')
    cmd_value = iec104.DoubleValue[value]
    cmd = iec104.DoubleCommand(
        value=cmd_value,
        select=False,
        qualifier=0)
    cmd_msg = iec104.CommandMsg(
        is_test=False,
        originator_address=0,
        asdu_address=asdu,
        io_address=io,
        command=cmd,
        is_negative_confirm=False,
        time=None,
        cause=iec104.CommandReqCause.ACTIVATION)

    try:
        conn.send([cmd_msg])
        print(f'command sent asdu={asdu} io={io} value={cmd_value}')

        print('waiting command response...')
        msg = None
        while not isinstance(msg, iec104.CommandMsg):
            msgs = await conn.receive()
            msg = msgs[0]

        success = 'SUCCESS' if not msg.is_negative_confirm else 'FAILURE'
        print(f'received command response {success}')
    finally:
        await aio.uncancellable(conn.async_close())


if __name__ == '__main__':
    sys.exit(main())
