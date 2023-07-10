from pathlib import Path
import asyncio
import click
import contextlib
import datetime
import logging
import logging.config
import random
import sys

from hat import aio
from hat import json
from hat.drivers import tcp
from hat.drivers.iec60870 import apci
from hat.drivers.iec60870 import iec104


mlog: logging.Logger = logging.getLogger(__name__)

default_conf_path = Path('relay.yaml')


@click.command()
@click.option('--conf-path', type=Path,
              default=None)
def main(conf_path):
    conf = json.decode_file(conf_path)

    logging.config.dictConfig(conf['log'])

    with contextlib.suppress(asyncio.CancelledError):
        aio.run_asyncio(async_main(conf))


async def async_main(conf):
    slave = await create_slave(conf)
    await slave.wait_closed()


async def create_slave(conf):
    slave = Slave()
    slave._conf = conf
    srv = await apci.listen(
        connection_cb=slave._on_connection,
        addr=tcp.Address(host='0.0.0.0',
                         port=conf['iec104_slave_port']))
    mlog.info('iec104 slave listens on port %s ...', conf['iec104_slave_port'])
    slave._srv = srv
    slave._conns = {}
    slave._async_group = aio.Group()
    slave._async_group.spawn(aio.call_on_cancel, srv.async_close)

    slave._name_to_asdu_io = {
        i['name']: (i['type'], i['asdu'], i['ioa'])
        for i in conf['points']}
    slave._actual_state = conf['default_state']
    slave._states = {i['name']: i for i in conf['states']}
    slave._sim_group = None
    await slave._restart_simulations()
    return slave


class Slave(aio.Resource):

    @property
    def async_group(self):
        return self._async_group

    def _on_connection(self, conn_apci):
        conn = iec104.Connection(conn_apci)
        mlog.debug('received connection %s', conn_apci.info)
        self._conns[conn] = conn_apci
        self._async_group.spawn(self._receive_loop, conn)

    async def _receive_loop(self, conn):
        try:
            while True:
                msgs = await conn.receive()
                mlog.debug('received messages: %s', msgs)
                for msg in msgs:
                    if isinstance(msg, iec104.InterrogationMsg):
                        self._process_interrogate(conn, msg)
                    if isinstance(msg, iec104.CommandMsg):
                        conn.send([_cmd_req_to_resp(msg)])
                        await self._process_trigger(conn, msg)

        except ConnectionError:
            mlog.debug('connection %s closed', self._conns[conn].info)
        finally:
            self._conns.pop(conn)
            await conn.async_close()

    async def _sim_loop(self, point_conf):
        mlog.debug('starting simulation %s', point_conf['name'])
        while True:
            await asyncio.sleep(point_conf['refresh_period'])
            if not self._conns:
                continue
            data = self._gen_data(point_conf)
            if not data:
                mlog.error('data %s cannot be simulated', point_conf['name'])
                return
            for conn in self._conns:
                conn.send([data])
            mlog.debug('sent data %s', point_conf['name'])

    async def _restart_simulations(self):
        if self._sim_group and not self._sim_group.is_closed:
            await self._sim_group.async_close()
            mlog.debug('simulations stopped')
        self._sim_group = self._async_group.create_subgroup()
        for point_conf in self._states[self._actual_state]['points']:
            if point_conf['type'] in ['random_numeric',
                                      'random_string']:
                self._sim_group.spawn(self._sim_loop, point_conf)

    def _process_interrogate(self, conn, msg):
        conn.send([msg._replace(
            is_negative_confirm=False,
            cause=iec104.CommandResCause.ACTIVATION_CONFIRMATION)])
        resp_data = []
        for p_conf in self._states[self._actual_state]['points']:
            data = self._gen_data(
                p_conf, cause=iec104.DataResCause.INTERROGATED_STATION)
            if not data:
                continue
            resp_data.append(data)
        conn.send(resp_data)
        conn.send([msg._replace(
            is_negative_confirm=False,
            cause=iec104.CommandResCause.ACTIVATION_TERMINATION)])

    async def _process_trigger(self, conn, msg):
        new_state = self._get_triggered_state(msg)
        if not new_state or new_state == self._actual_state:
            return
        mlog.info('trigger to state %s by %s', new_state, msg)
        self._actual_state = new_state
        spont_data = []
        for point_conf in self._states[self._actual_state]['points']:
            data = self._gen_data(point_conf)
            if not data:
                continue
            spont_data.append(data)
        mlog.debug("sent spont data: %s", spont_data)
        conn.send(spont_data)
        await self._restart_simulations()

    def _gen_data(self, point_conf, cause=iec104.DataResCause.SPONTANEOUS):
        asdu_type, asdu, io = self._name_to_asdu_io[point_conf['name']]
        if asdu_type not in ['M_DP_TA',
                             'M_ME_NC']:
            return
        if point_conf['type'] == 'constant':
            value = point_conf['value']
        elif point_conf['type'] == 'random_numeric':
            value = _gen_random_numeric_value(point_conf)
        elif point_conf['type'] == 'random_string':
            value = _gen_random_string_value(point_conf)
        else:
            raise NotImplementedError()
        if value is True:
            mlog.warning("value %s %s", value, point_conf)
        return iec104.DataMsg(
            is_test=False,
            originator_address=0,
            asdu_address=asdu,
            io_address=io,
            data=_type_value_to_data(asdu_type, value),
            time=_time_from_asdu_type(asdu_type),
            cause=cause)

    def _get_triggered_state(self, msg):
        if not isinstance(msg, iec104.CommandMsg):
            return
        for state in self._states.values():
            for trigger in state['trigger_conditions']:
                type_asdu_io = self._name_to_asdu_io.get(trigger['point_name'])
                if not type_asdu_io:
                    return
                _, asdu, io = type_asdu_io
                if (isinstance(msg.command, iec104.DoubleCommand) and
                    msg.asdu_address == asdu and
                    msg.io_address == io and
                        msg.command.value.name == trigger['value']):
                    return state['name']


def _type_value_to_data(asdu_type, value):
    if asdu_type == 'M_DP_TA':
        return iec104.DoubleData(
            value=iec104.DoubleValue[value],
            quality=iec104.IndicationQuality(
                invalid=False,
                not_topical=False,
                substituted=False,
                blocked=False))
    if asdu_type == 'M_ME_NC':
        return iec104.FloatingData(
            value=iec104.FloatingValue(
                value=value),
            quality=iec104.MeasurementQuality(
                invalid=False,
                not_topical=False,
                substituted=False,
                blocked=False,
                overflow=False))
    raise Exception(f'asdu type {asdu_type} not implemented')


def _time_from_asdu_type(asdu_type):
    if asdu_type.endswith('NA'):
        return
    return iec104.time_from_datetime(
        datetime.datetime.now(datetime.timezone.utc))


def _gen_random_numeric_value(point_conf):
    return round(random.uniform(*point_conf['interval']),
                 point_conf['num_decimals'])


def _gen_random_string_value(point_conf):
    return random.choice(point_conf['interval'])


def _cmd_req_to_resp(msg):
    return msg._replace(
        cause=iec104.CommandResCause.ACTIVATION_CONFIRMATION,
        is_negative_confirm=False)


if __name__ == '__main__':
    sys.exit(main())
