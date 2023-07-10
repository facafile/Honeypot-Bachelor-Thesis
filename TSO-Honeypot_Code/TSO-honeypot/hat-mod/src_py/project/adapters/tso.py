from datetime import datetime
import hat.aio
import hat.event.common
import hat.gui.common
import hat.util
import logging
import itertools

json_schema_id = None
json_schema_repo = None


async def create_subscription(conf):
    return hat.event.common.Subscription([('tso', )])


async def create_adapter(conf, event_client):
    logging.info("Creating TSO adapter")
    adapter = Adapter()

    adapter._async_group = hat.aio.Group()
    adapter._event_client = event_client
    adapter._sessions = set()
    adapter._state = {}
    for asdu, io in (
            list(itertools.product([0, 1, 2, 3, 4, 5, 6], [0, 1]))
            + list(itertools.product([10, 11, 12, 13, 20], [0, 1, 2, 3, 4]))
            + list(itertools.product([30], [0, 1, 2, 3, 4, 5, 6, 7]))):
        adapter._state[f"{asdu}:{io}"] = '[]'
        adapter._state[f"{asdu}:{io}-timestamp"] = '-'

    adapter._async_group.spawn(adapter._main_loop)
    return adapter


class Adapter(hat.gui.common.Adapter):

    @property
    def async_group(self):
        return self._async_group

    async def create_session(self, juggler_client):
        session = Session(
            juggler_client,
            self._async_group.create_subgroup())
        self._sessions.add(session)
        return session

    async def _main_loop(self):
        while True:
            try:
                events = await self._event_client.receive()
                for event in events:
                    #self._state = {'tso': event.payload.data}
                    asdu_address = event.payload.data["asdu_address"]
                    io_address = event.payload.data["io_address"]
                    self._state[f"{asdu_address}:{io_address}"] = str([float(v) for v in event.payload.data["value"]])
                    self._state[f"{asdu_address}:{io_address}-timestamp"] = str(datetime.now())
                for session in self._sessions:
                    if session.is_open:
                        session.notify_state_change(self._state)
                # logging.info("TSO adapter data fetched and registered... " + str(self._state))
            except Exception as ex:
                logging.error("Adapter: " + str(ex))


class Session(hat.gui.common.AdapterSession):

    def __init__(self, juggler_client, group):
        self._juggler_client = juggler_client
        self._async_group = group

    @property
    def async_group(self):
        return self._async_group

    def notify_state_change(self, state):
        self._juggler_client.set_local_data(state)
