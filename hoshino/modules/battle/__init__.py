from hoshino import Service, priv
import os
try:
    import ujson as json
except:
    import json

sv_help = '''公会战信息整合工具ver1.0.0
- [预约] [信息]      预约boss,一个账号只能预约一次,预约多个boss请在信息标注
- [进] [信息] 		出刀，一个账号只能有一个出刀，取消出刀状态/结束出刀请用[取消出刀]
- [挂树] [信息]      挂树，下树请用[下树]
- [合刀] [信息]      合到+信息,一个账号只能有一个合刀信息，【取消合刀】来取消。

例子：合刀 123
预约 1,2,3
挂树 2
－【清空公会战状态】    管理特权
－【查刀】    字面意思
'''.strip()
# - [清空下班表] 	清空下班表

sv = Service('battle', use_priv=priv.NORMAL, manage_priv=priv.ADMIN,
             visible=True, help_=sv_help, enable_on_default=True, bundle='查询')


@sv.on_fullmatch(["帮助下班"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


JSON_TEAM = (os.path.join(os.path.dirname(__file__), "battle.json"))


async def render_forward_msg(msg_list: list, uids: list, name):
    forward_msg = []
    for msg, uid in zip(msg_list, uids):
        forward_msg.append({
            "type": "node",
            "data": {
                "name": str(name),
                "uin": str(uid),
                "content": msg
            }
        })
    return forward_msg


def readfile():
    with open(JSON_TEAM, "r", encoding='utf8') as f:
        content = f.read()
        data = json.loads(content)
    return data


zhaomu = readfile()


def savefile():
    with open(JSON_TEAM, "w", encoding='utf8') as f:
        json.dump(zhaomu, f, ensure_ascii=False)


# def add_message(gid, uid, ev, bot):
#     if gid not in zhaomu:
#         zhaomu[gid] = {}

#     if uid not in zhaomu[gid]:
#         zhaomu[gid][uid] = {}
#         message = "下班"
#         zhaomu[gid][uid] = message
#         savefile()
#         msg = "成功添加至下班栏上～\n发送[查询下班表]可以查看别人的下班"
#         await bot.send(ev, msg, at_sender=True)
#         return
#     else 
#         msg = "你早下班了发个🔨信息哼"
#         await bot.send(ev, msg, at_sender=True)
#         return
def add_message_tree(gid, uid, ev, bot, message):
    if gid not in zhaomu:
        zhaomu[gid] = {}
    title = "树上人"
    if title not in zhaomu[gid]:
        zhaomu[gid][title] = {}
    if uid not in zhaomu[gid]:
        zhaomu[gid][title][uid] = message
        savefile()
        msg = "成功添加信息，大家救救孩子"
        await bot.send(ev, msg, at_sender=True)
        return
    else 
        msg = "已经在树上了TAT“
        await bot.send(ev, msg, at_sender=True)
        return

def add_message_chudao(gid, uid, ev, bot, message):
    if gid not in zhaomu:
        zhaomu[gid] = {}
    title = "出刀人"
    if title not in zhaomu[gid]:
        zhaomu[gid][title] = {}
    if uid not in zhaomu[gid]:
        zhaomu[gid][title][uid] = message
        savefile()
        msg = "成功添加信息"
        await bot.send(ev, msg, at_sender=True)
        return
    else 
        msg = "已经在出刀哒“
        await bot.send(ev, msg, at_sender=True)
        return

def add_message_hedao(gid, uid, ev, bot, message):
    if gid not in zhaomu:
        zhaomu[gid] = {}
    title = "合刀人"
    if title not in zhaomu[gid]:
        zhaomu[gid][title] = {}
    if uid not in zhaomu[gid]:
        zhaomu[gid][title][uid] = message
        savefile()
        msg = "成功添加信息"
        await bot.send(ev, msg, at_sender=True)
        return
    else 
        msg = "已经在出刀哒“
        await bot.send(ev, msg, at_sender=True)
        return

def add_message_ap(gid, uid, ev, bot, message):
    if gid not in zhaomu:
        zhaomu[gid] = {}
    title = "预约人"
    if title not in zhaomu[gid]:
        zhaomu[gid][title] = {}
    if uid not in zhaomu[gid]:
        zhaomu[gid][title][uid] = message
        savefile()
        msg = "成功添加信息"
        await bot.send(ev, msg, at_sender=True)
        return
    else 
        msg = "已经在出刀哒“
        await bot.send(ev, msg, at_sender=True)
        return

def delete_user(gid, uid, title):
    if gid not in zhaomu:
        return False

    if title not in zhaomu[gid]:
        return False

    if uid not in zhaomu[gid][title]:
        return False

    del zhaomu[gid][title][uid]

    savefile()

    return True

# def delete_user(gid, uid):
#     if gid not in zhaomu:
#         return False

#     if uid not in zhaomu[gid]:
#         return False

#     del zhaomu[gid][uid]

#     savefile()

#     return True


def process_table(gid, title):
    print(zhaomu)

    msg = []
    qq = []
    for user, message in zhaomu[gid][title].items():
        msg.append(f"{user}: {message}")
        qq.append(user)

    if msg == []:
        msg = "表是空的哦qwq"

    return msg, qq


@sv.on_prefix('挂树')
# @sv.on_fullmatch('下班')
async def ontree_handle(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    if uid == "80000000":
        msg = "匿名个🔨哦都挂树了"
        await bot.send(ev, msg)
        return
    message = ev.message.extract_plain_text()
    if len(message.split()) != 2:
        await bot.finish(ev, sv.help)
        return
    add_message_tree(gid, uid, ev, bot, message)

@sv.on_fullmatch('下树')
# @sv.on_fullmatch('下班')
async def leave_tree(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    title = "树上人"

    if uid == "80000000":
        msg = "匿名下个🔨树"
        await bot.send(ev, msg)
        return
    ok = delete_user(gid, uid, title)
    if ok:
        msg = "成功～"
    else:
        msg = "没找你惹qwq是不是记错了？"
    await bot.send(ev, msg, at_sender=True)

@sv.on_prefix('进')
# @sv.on_fullmatch('下班')
async def chudao_handle(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名个🔨哦都挂树了"
        await bot.send(ev, msg)
        return
    message = ev.message.extract_plain_text()
    if len(message.split()) != 2:
        await bot.finish(ev, sv.help)
        return
    add_message_chudao(gid, uid, ev, bot, message)

@sv.on_fullmatch('取消出刀')
# @sv.on_fullmatch('下班')
async def leave_chudao(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    title = "出刀人"

    if uid == "80000000":
        msg = "匿名取消个🔨刀"
        await bot.send(ev, msg)
        return
    ok = delete_user(gid, uid, title)
    if ok:
        msg = "成功～"
    else:
        msg = "没找你惹qwq是不是记错了？"
    await bot.send(ev, msg, at_sender=True)

@sv.on_prefix('合刀')
# @sv.on_fullmatch('下班')
async def hedao_handle(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    message = ev.message.extract_plain_text()
    if len(message.split()) != 2:
        await bot.finish(ev, sv.help)
        return
    add_message_hedao(gid, uid, ev, bot, message)

@sv.on_fullmatch('取消合刀')
# @sv.on_fullmatch('下班')
async def leave_hedao(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    title = "合刀人"

    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    ok = delete_user(gid, uid, title)
    if ok:
        msg = "成功～"
    else:
        msg = "没找你惹qwq是不是记错了？"
    await bot.send(ev, msg, at_sender=True)

@sv.on_prefix('预约')
# @sv.on_fullmatch('下班')
async def ap_handle(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    message = ev.message.extract_plain_text()
    if len(message.split()) != 2:
        await bot.finish(ev, sv.help)
        return
    add_message_ap(gid, uid, ev, bot, message)

@sv.on_fullmatch('取消预约')
# @sv.on_fullmatch('下班')
async def leave_hedao(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    title = "预约人"

    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    ok = delete_user(gid, uid, title)
    if ok:
        msg = "成功～"
    else:
        msg = "没找你惹qwq是不是记错了？"
    await bot.send(ev, msg, at_sender=True)

# @sv.on_fullmatch(('查看下班表', '查询下班表'))
# async def query_table(bot, ev):

@sv.on_fullmatch(('查刀'))
async def query_table(bot, ev):

    gid = str(ev.group_id)

    if gid not in zhaomu:
        text = "表是空的哦qwq"
        await bot.send(ev, text)
        return

    msg1, user1 = process_table(gid, "预约人")
    msg2, user2 = process_table(gid, "合刀人")
    msg3, user3 = process_table(gid, "出刀人")
    msg4, user4 = process_table(gid, "树上人")
    new_msg1 = await render_forward_msg(msg1, user1, "预约人")
    new_msg2 = await render_forward_msg(msg2, user2, "合刀人")
    new_msg3 = await render_forward_msg(msg3, user3, "出刀人")
    new_msg4 = await render_forward_msg(msg4, user4, "树上人")
    msg = new_msg1+new_msg2+new_msg3+new_msg4
    
    await bot.send_group_forward_msg(group_id=ev.group_id, messages=msg)

# @sv.on_fullmatch('取消下班')
# async def delete_single_zhaomu(bot, ev):

#     gid = str(ev.group_id)
#     uid = str(ev.user_id)

#     if uid == "80000000":
#         msg = "匿名你取消下班个🔨哦"
#         await bot.send(ev, msg)
#         return

#     ok = delete_user(gid, uid)

#     if ok:
#         msg = "取消下班成功～"
#     else:
#         msg = "下班表没找你惹qwq是不是记错了？"

#     await bot.send(ev, msg, at_sender=True)


# @sv.on_fullmatch('清空下班表')
@on_command('清空公会战状态', only_to_me=True)
async def cancle_zhaomu(session):
    zhaomu = {}
    savefile()

    await bot.send('删除成功')
# async def cancle_zhaomu(bot, ev):

#     gid = str(ev.group_id)
#     uid = str(ev.user_id)

#     if uid == "80000000":
#         msg = "匿名你取消下班个🔨哦"
#         await bot.send(ev, msg)
#         return

#     ok = delete_user(gid, uid)

#     if ok:
#         msg = "取消下班成功～"
#     else:
#         msg = "下班表没找你惹qwq是不是记错了？"

