import pytz
from datetime import datetime
from hoshino import Service, R

sv = Service('buy_potion_reminder', enable_on_default=True, help_='买药提醒')


@sv.scheduled_job('cron', hour='5')
async def hour_call1():
    pic = R.img("BuyPotion1.jpg").cqcode
    msg = f'骑士君，该上线买经验药水啦~\n{pic}'
    await sv.broadcast(msg, 'buy_potion_reminder')

@sv.scheduled_job('cron', hour='11')
async def hour_call2():
    pic = R.img("BuyPotion2.jpg").cqcode
    msg = f'骑士君，该上线买经验药水啦~\n{pic}'
    await sv.broadcast(msg, 'buy_potion_reminder')

@sv.scheduled_job('cron', hour='17')
async def hour_call3():
    pic = R.img("BuyPotion3.jpg").cqcode
    msg = f'骑士君，该上线买经验药水啦~\n{pic}'
    await sv.broadcast(msg, 'buy_potion_reminder')

@sv.scheduled_job('cron', hour='23')
async def hour_call4():
    pic = R.img("BuyPotion4.jpg").cqcode
    msg = f'骑士君，该上线买经验药水啦~\n{pic}'
    await sv.broadcast(msg, 'buy_potion_reminder')
