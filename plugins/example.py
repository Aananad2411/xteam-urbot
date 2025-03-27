from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from pyUltroid import *
from pytgcalls import filters as fl
from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls.types import ChatUpdate
from pytgcalls.types import GroupCallParticipant
from pytgcalls.types import StreamEnded
from pytgcalls.types import Update
from pytgcalls.types import UpdatedGroupCallParticipant

app = Client(
    'py-tgcalls',
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
)
call_py = PyTgCalls(app)


@app.on_message(filters.regex('!play'))
async def play_handler(_: Client, message: Message):
    await call_py.play(
        message.chat.id,
        'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4',
    )


@app.on_message(filters.regex('!record'))
async def record_handler(_: Client, message: Message):
    await call_py.record(
        message.chat.id,
        'record.mp3',
    )


@app.on_message(filters.regex('!cache'))
async def cache_handler(_: Client, _m: Message):
    print(call_py.cache_peer)


@app.on_message(filters.regex('!ping'))
async def ping_handler(_: Client, _m: Message):
    print(call_py.ping)


@app.on_message(filters.regex('!pause'))
async def pause_handler(_: Client, message: Message):
    await call_py.pause(
        message.chat.id,
    )


@app.on_message(filters.regex('!resume'))
async def resume_handler(_: Client, message: Message):
    await call_py.resume(
        message.chat.id,
    )


@app.on_message(filters.regex('!stop'))
async def stop_handler(_: Client, message: Message):
    await call_py.leave_call(
        message.chat.id,
    )


@app.on_message(filters.regex('!change_volume'))
async def change_volume_handler(_: Client, message: Message):
    await call_py.change_volume_call(
        message.chat.id,
        50,
    )


@app.on_message(filters.regex('!status'))
async def get_play_status(client: Client, message: Message):
    await client.send_message(
        message.chat.id,
        f'Current seconds {await call_py.time(message.chat.id)}',
    )


@call_py.on_update(
    fl.chat_update(
        ChatUpdate.Status.KICKED | ChatUpdate.Status.LEFT_GROUP,
    ),
)
async def kicked_handler(_: PyTgCalls, update: ChatUpdate):
    print(f'Kicked from {update.chat_id} or left')


@call_py.on_update(fl.stream_end())
async def stream_end_handler(_: PyTgCalls, update: StreamEnded):
    print(f'Stream ended in {update.chat_id}', update)


@call_py.on_update(
    fl.call_participant(GroupCallParticipant.Action.JOINED),
)
async def participant_handler(
    _: PyTgCalls,
    update: UpdatedGroupCallParticipant,
):
    print(f'Participant joined in {update.chat_id}', update)


@call_py.on_update()
async def all_updates(_: PyTgCalls, update: Update):
    print(update)

call_py.start()
idle()
