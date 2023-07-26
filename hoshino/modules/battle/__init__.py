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
预约 123
挂树 2
－[清空公会战状态]    管理特权
- [清空下班表] 	清空下班表
－[查刀]    字面意思
'''.strip()
# - [清空下班表] 	清空下班表

sv = Service('battle', use_priv=priv.NORMAL, manage_priv=priv.ADMIN,
             visible=True, help_=sv_help, enable_on_default=True, bundle='查询')


# 目录-帮助 -------------------------------------------------------------------------------------------------------------------

@sv.on_fullmatch(["帮助下班"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


JSON_TEAM = (os.path.join(os.path.dirname(__file__), "battle.json"))

def readfile():
    with open(JSON_TEAM, "r", encoding='utf8') as f:
        content = f.read()
        data = json.loads(content)
    return data


zhaomu = readfile()


def savefile():
    with open(JSON_TEAM, "w", encoding='utf8') as f:
        json.dump(zhaomu, f, ensure_ascii=False)


# 目录-挂树--------------------------------------------------------------------------------------------------------------------


async def add_message_tree(gid, uid, ev, bot, message):
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
    else:
        msg = "已经在树上了TAT"
        await bot.send(ev, msg, at_sender=True)
        return

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


# 目录-出刀--------------------------------------------------------------------------------------------------------------------

async def add_message_chudao(gid, uid, ev, bot, message):
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
    else:
        msg = "已经在出刀哒"
        await bot.send(ev, msg, at_sender=True)
        return

@sv.on_prefix('出刀')
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

# 目录-合刀--------------------------------------------------------------------------------------------------------------------

async def add_message_hedao(gid, uid, ev, bot, message):
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
    else:
        msg = "已经在出刀哒"
        await bot.send(ev, msg, at_sender=True)
        return

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

# 目录-预约--------------------------------------------------------------------------------------------------------------------

# def add_message_ap(gid, uid, ev, bot, message):
#     if gid not in zhaomu:
#         zhaomu[gid] = {}
#     title = "预约人"
#     if title not in zhaomu[gid]:
#         zhaomu[gid][title] = {}
#     if uid not in zhaomu[gid]:
#         zhaomu[gid][title][uid] = message
#         savefile()
#         msg = "成功添加信息"
#         await bot.send(ev, msg, at_sender=True)
#         return
#     else 
#         msg = "已经在出刀哒“
#         await bot.send(ev, msg, at_sender=True)
#         return

# 目录-删除--------------------------------------------------------------------------------------------------------------------

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

# 目录-表格生成--------------------------------------------------------------------------------------------------------------------

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

def process_table(gid, title):

    msg = []
    qq = []
    for user, message in zhaomu[gid][title].items():
        msg.append(f"{user}: {message}")
        qq.append(user)

    if msg == []:
        if title == "合刀人":
            msg = "没有人合刀"
        if title == "出刀人":
            msg = "没有人出刀"
        if title == "挂树人":
            msg = "没有人挂树"

    return msg, qq

# 目录-查刀--------------------------------------------------------------------------------------------------------------------

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

    if isinstance(msg2, str):
        await bot.send(ev, msg2)
    else:
        new_msg2 = await render_forward_msg(msg2, user2, "合刀人")
        await bot.send_group_forward_msg(group_id=ev.group_id, messages=new_msg2)
    if isinstance(msg2, str):
        await bot.send(ev, msg2)
    else:
        new_msg3 = await render_forward_msg(msg3, user3, "出刀人")
        await bot.send_group_forward_msg(group_id=ev.group_id, messages=new_msg3)
    if isinstance(msg4, str):
        await bot.send(ev, msg4)
    else:
        new_msg4 = await render_forward_msg(msg4, user4, "树上人")
        await bot.send_group_forward_msg(group_id=ev.group_id, messages=new_msg4)

# 目录-上下班--------------------------------------------------------------------------------------------------------------------



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


# 目录-clear function--------------------------------------------------------------------------------------------------------------------

# @sv.on_fullmatch('清空下班表')
# @on_command('清空公会战状态', only_to_me=True)
# async def cancle_zhaomu(session):
#     zhaomu = {}
#     savefile()

#     await bot.send('删除成功')
