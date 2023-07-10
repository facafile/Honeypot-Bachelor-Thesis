import asyncio
from time import sleep
from hat.drivers import iec104
import hat.aio
import hat.event.common
import hat.gateway.common
import datetime
import logging

json_schema_id = None
json_schema_repo = None
device_type = 'tso'

async def create(conf, event_client, event_type_prefix):
    logging.info("Creating TSO device")
    device = TSODevice()
    device._async_group = hat.aio.Group()
    device._event_client = event_client
    device._event_type_prefix = event_type_prefix
    device._async_group.spawn(device._main_loop)
    logging.info("TSO device created")
    return device

class TSODevice(hat.gateway.common.Device):
    @property
    def async_group(self):
        return self._async_group

    async def _main_loop(self):
        logging.info("TSO device connecting...")
        while True:
            try:
                connection = await iec104.connect(
                    iec104.Address('10.0.0.30', 12345))
                break
            except:
                await asyncio.sleep(0.5)

        while True:
            try:
                for data in (await connection.receive()):
                    self._event_client.register([
                        hat.event.common.RegisterEvent(
                            event_type=(*self._event_type_prefix,
                            'gateway', 'tso'),
                            source_timestamp=None,
                            payload=hat.event.common.EventPayload(
                                type=hat.event.common.EventPayloadType.JSON,
                                data={
                                    "asdu_address": data.asdu_address,
                                    "io_address": data.io_address,
                                    "time": data.time,
                                    "value": data.value
                                }
                            )
                        )
                    ])
                # logging.info("TSO device data fetched and registered... " + str(data))
            except Exception as ex:
                logging.info(str(ex))
                await asyncio.sleep(0.5)
