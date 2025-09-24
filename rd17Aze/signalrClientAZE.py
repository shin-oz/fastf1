import logging

from fastf1.livetiming.client import SignalRClient # type: ignore

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# 完全なSignalRメッセージとして保存
client = SignalRClient(filename="250919FP1.txt", debug=True)
client.start()