from hoshino import Service, priv
from hoshino.typing import CQEvent
from datetime import datetime
import os
import re
try:
    import ujson as json
except:
    import json

sv_help = '''公会战信息整合工具ver3.0.0
- [进/出刀] [信息] 		出刀，一个账号只能有一个出刀，取消出刀状态/结束出刀请用[取消出刀]
- [挂树] [信息]      挂树，下树请用[下树]
- [预约] [信息]      合到+信息,一个账号只能有一个预约信息，【取消预约】来取消。
- [合刀] [BOSS血量] [刀1] [刀2] 计算合刀后尾刀时间
- [补偿计算/转秒 <返还时间> <时间轴>] 【返还时间+空格】后必须换行
可接受的时间格式：以65秒为例，“065”，“65s”，“105”，“1:05”，“01：05”等均可。
例：输入       返回
“转秒 35       “35秒的时间轴：
119 公主凯露    0:24 公主凯露
1:13 似似花     0:18 似似花
01：05	露娜    0:10 露娜
0058 春花       0:03 春花“
54 水电”

- [清空下班表|清空下班] 	管理特权
- [清空查刀、清空预约、清空出刀、清空挂树] 	管理特权
- [查刀、查预约、查出刀、查挂树]    字面意思
'''.strip()
# - [清空公会战状态|清空公会战状态|清空状态|清空表格]    管理特
# - [清空下班表] 	清空下班表
# - [预约] [信息]      预约boss,一个账号只能预约一次,预约多个boss请在信息标注

sv = Service('battleV3', use_priv=priv.NORMAL, manage_priv=priv.ADMIN,
             visible=True, help_=sv_help, enable_on_default=True, bundle='查询')


# 目录-帮助 -------------------------------------------------------------------------------------------------------------------

@sv.on_fullmatch(["会战帮助"])
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

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# 目录-建公会----------------------------------------------------------------------------------------------------------------
@sv.on_fullmatch('建会')
async def party_build(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    if uid == "80000000":
        msg = "匿名建个🔨公会"
        await bot.send(ev, msg)
        return
    if priv.get_user_priv(ev) < 21:
        await bot.send(ev, f'只能群管理设置呢 (:3[▓▓]')
        return
    if gid not in zhaomu:
        zhaomu[gid] = {}
        savefile()
        msg = "建立公会成功"
        await bot.send(ev, msg, at_sender=True)
    else:
        msg = "公会已经存在"
        await bot.send(ev, msg, at_sender=True)
    return

# 目录-群名----------------------------------------------------------------------------------------------------------------

async def find_name(bot, gid, uid):
    member_list = await bot.get_group_member_list(group_id=int(gid))
    for mem in member_list:
        if str(mem['user_id']) == uid:
            name = mem['card'] or mem['nickname'] or str(mem['user_id'])
            return name

# 目录-加入公会----------------------------------------------------------------------------------------------------------------

@sv.on_fullmatch('入会')
async def join_party(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    if uid == "80000000":
        msg = "匿名加个🔨公会"
        await bot.send(ev, msg)
        return
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    else:
        if uid not in zhaomu[gid]:
            name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
            zhaomu[gid][uid] = {
                '群名片': name,
                '出刀': "",
                '预约': "",
                '挂树': "",
                '打卡': 0,
                'SL': 0,
            }
            savefile()
            msg = "加入成功"
            await bot.send(ev, msg, at_sender=True)
        else:
            msg = "你已经在公会了亲~"
            await bot.send(ev, msg, at_sender=True)
    return

@sv.on_prefix('入会')
async def join_party_other(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    else:
        if uid not in zhaomu[gid]:
            name = await find_name(bot, gid, uid)
            print(name)
            zhaomu[gid][uid] = {
                '群名片': name,
                '出刀': "",
                '预约': "",
                '挂树': "",
                '打卡': 0,
                'SL': 0,
            }
            savefile()
            msg = "加入成功"
            await bot.send(ev, msg, at_sender=True)
        else:
            msg = "你已经在公会了亲~"
            await bot.send(ev, msg, at_sender=True)
    return

# 目录-退公会----------------------------------------------------------------------------------------------------------------

@sv.on_fullmatch('退会')
async def quit_party(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    if uid == "80000000":
        msg = "匿名退个🔨公会"
        await bot.send(ev, msg)
        return
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    else:
        if uid not in zhaomu[gid]:
            msg = "你不在公会哦~"
            await bot.send(ev, msg, at_sender=True)
        else:
            del zhaomu[gid][uid]
            savefile()
            msg = "退会成功~"
            await bot.send(ev, msg, at_sender=True)
    return

@sv.on_prefix('退会')
async def quit_party(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    else:
        if uid not in zhaomu[gid]:
            msg = "这位成员不在公会哦~"
            await bot.send(ev, msg, at_sender=True)
        else:
            del zhaomu[gid][uid]
            savefile()
            msg = "退会成功~"
            await bot.send(ev, msg, at_sender=True)
    return

# 目录-更改信息--------------------------------------------------------------------------------------------------------------------

async def update_message(bot, ev, gid, uid, name, message, title):
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    if uid not in zhaomu[gid]:
        msg = "你不在公会哦~"
        await bot.send(ev, msg, at_sender=True)
        return
    # zhaomu[gid][uid]['群名片'] = name
    if title == '挂树':
        zhaomu[gid][uid][title] = message
        savefile()
        msg = "成功添加信息，大家救救孩子"
        if message == '':
            msg = "成功下树，谢谢大家"
        await bot.send(ev, msg, at_sender=True)
        return
    zhaomu[gid][uid][title] = message
    savefile()
    msg = "成功添加信息"
    if message == '':
        msg = "成功清除信息"
    await bot.send(ev, msg, at_sender=True)
    return

# 目录-挂树--------------------------------------------------------------------------------------------------------------------

@sv.on_prefix('挂树')
async def ontree_handle(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    if uid == "80000000":
        msg = "匿名个🔨哦都挂树了"
        await bot.send(ev, msg)
        return
    message = ev.message.extract_plain_text()
    title = '挂树'
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    # if len(message.split()) != 2:
    #     await bot.finish(ev, sv.help)
    #     return
    if has_numbers(message):
        await update_message(bot, ev, gid, uid, name, message, title)

@sv.on_fullmatch('下树')
async def leave_tree(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    title = "挂树"
    if uid == "80000000":
        msg = "匿名下个🔨树"
        await bot.send(ev, msg)
        return
    message = ""
    title = '挂树'
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    await update_message(bot, ev, gid, uid, name, message, title)

@sv.on_prefix('下树')
async def leave_tree_other(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    title = '挂树'
    # name = await find_name(bot, gid, uid)
    name = ""
    message = ""
    await update_message(bot, ev, gid, uid, name, message, title)

# 目录-出刀--------------------------------------------------------------------------------------------------------------------

@sv.on_prefix('出刀', '进')
async def chudao_handle(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名出个🔨刀"
        await bot.send(ev, msg)
        return
    message = ev.message.extract_plain_text()
    if has_numbers(message):
        title = '出刀'
        name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
        await update_message(bot, ev, gid, uid, name, message, title)

@sv.on_fullmatch('取消出刀', '报刀')
async def clean_chudao(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名取消个🔨刀"
        await bot.send(ev, msg)
        return
    title = '出刀'
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    message = ""
    await update_message(bot, ev, gid, uid, name, message, title)

@sv.on_prefix('取消出刀', '报刀')
async def clean_chudao_other(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    title = '出刀'
    # name = await find_name(bot, gid, uid)
    name = ""
    message = ""
    await update_message(bot, ev, gid, uid, name, message, title)

# 目录-预约--------------------------------------------------------------------------------------------------------------------

# async def add_message_hedao(gid, uid, ev, bot, message):
#     if gid not in zhaomu:
#         zhaomu[gid] = {}
#     title = "合刀人"
#     if title not in zhaomu[gid]:
#         zhaomu[gid][title] = {}
#     if uid not in zhaomu[gid]:
#         zhaomu[gid][title][uid] = message
#         savefile()
#         msg = "成功添加信息"
#         await bot.send(ev, msg, at_sender=True)
#         return
#     else:
#         msg = "已经在出刀哒"
#         await bot.send(ev, msg, at_sender=True)
#         return

@sv.on_prefix('预约')
async def ap_handle(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    message = ev.message.extract_plain_text()
    # if len(message.split()) != 2:
    #     await bot.finish(ev, sv.help)
    #     return
    if has_numbers(message):
        title = '预约'
        name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
        await update_message(bot, ev, gid, uid, name, message, title)

@sv.on_fullmatch('取消预约')
async def disap_hedao(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    message = ""
    title = '预约'
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    await update_message(bot, ev, gid, uid, name, message, title)

@sv.on_prefix('取消预约')
async def disap_handle_other(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)

    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    message = ""
    title = '预约'
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    await update_message(bot, ev, gid, uid, name, message, title)

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

# 目录-表格生成--------------------------------------------------------------------------------------------------------------------

def render_forward_msg(msg_list: list, uids: list):
    forward_msg = []
    for msg, uid in zip(msg_list, uids):
        forward_msg.append({
            "type": "node",
            "data": {
                "name": str(list(msg.keys())[0]),
                "uin": str(uid),
                "content": list(msg.values())[0],
            }
        })
    return forward_msg

def process_table(gid, title):

    msg = []
    qq = []
    for member in zhaomu[gid].keys():
        if zhaomu[gid][member][title] != "":
            qq.append(member)
            msg1 = str(zhaomu[gid][member]["群名片"])
            msg2 = str(zhaomu[gid][member][title])
            msg.append({
                msg1: msg2
            })

    if msg == []:
        if title == "预约":
            msg = "没有人预约"
        if title == "出刀":
            msg = "没有人出刀"
        if title == "挂树":
            msg = "没有人挂树"

    return msg, qq

# 目录-查刀--------------------------------------------------------------------------------------------------------------------

async def send_detail(bot, ev, title):
    gid = str(ev.group_id)

    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    if len(zhaomu[gid].keys()) == 0:
        msg = "光杆司令查什么刀"
        await bot.send(ev, msg, at_sender=True)
        return
    msg, user = process_table(gid, title)
    print(msg, user)
    if isinstance(msg, str):
        await bot.send(ev, msg)
    else:
        new_msg = render_forward_msg(msg, user)
        await bot.send_group_forward_msg(group_id=ev.group_id, messages=new_msg)
    return

@sv.on_fullmatch(('查刀'))
async def check_out_all(bot, ev):
    await send_detail(bot, ev, "预约")
    await send_detail(bot, ev, "出刀")
    await send_detail(bot, ev, "挂树")

@sv.on_fullmatch(('查预约'))
async def check_out_ap(bot, ev):
    await send_detail(bot, ev, "预约")

@sv.on_fullmatch(('查出刀'))
async def check_out_chudao(bot, ev):
    await send_detail(bot, ev, "出刀")

@sv.on_fullmatch(('查挂树'))
async def check_out_tree(bot, ev):
    await send_detail(bot, ev, "挂树")


# 目录-合刀计算------------------------------------------------------------------------------------------------------------------
@sv.on_prefix("计算尾刀", "合刀")
async def feedback(bot, ev: CQEvent):
    cmd = ev.message.extract_plain_text()
    content = cmd.split()
    print(content)
    if len(content) != 3:
        await bot.finish(ev, sv.help)
    try:
        d1 = float(content[0])
        d2 = float(content[1])
        rest = float(content[2])
    except (ValueError, RuntimeError):
        await bot.finish(ev, '请输入：计算尾刀 刀1伤害 刀2伤害 剩余血量\n如：计算尾刀 50 60 70')
    if d1 + d2 < rest:
        await bot.finish(ev, "醒醒！这两刀是打不死boss的")
    dd1 = d1
    dd2 = d2
    if d1 >= rest:
        dd1 = rest
    if d2 >= rest:
        dd2 = rest
    res1 = (1 - (rest - dd1) / dd2) * 90 + 20
    # 1先出，2能得到的时间
    res2 = (1 - (rest - dd2) / dd1) * 90 + 20
    # 2先出，1能得到的时间
    res1 = round(res1, 2)
    res2 = round(res2, 2)
    res1 = min(res1, 90)
    res2 = min(res2, 90)
    reply = f"{d1}先出，另一刀可获得 {res1} 秒补偿刀\n{d2}先出，另一刀可获得 {res2} 秒补偿刀\n"
    if d1 >= rest or d2 >= rest:
        reply += "\n注："
        if d1 >= rest:
            reply += f"\n第一刀可直接秒杀boss，伤害按 {rest} 计算"
        if d2 >= rest:
            reply += f"\n第二刀可直接秒杀boss，伤害按 {rest} 计算"
    await bot.send(ev, reply)

# 目录-上下班(func)--------------------------------------------------------------------------------------------------------------------

async def delete_user_off(gid, uid, ev, bot, name):
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    title = "打卡"
    if uid not in zhaomu[gid]:
        msg = "不在公会里哦~"
        await bot.send(ev, msg, at_sender=True)
        return
    if zhaomu[gid][uid][title] == 0:
        await bot.send(ev, f'你并没有打卡哦', at_sender=True)
    else:
        zhaomu[gid][uid][title] = 0
        # zhaomu[gid][uid]['群名片'] = name
        savefile()
        await bot.send(ev, f'取消打卡~', at_sender=True)
    return

async def add_message_off(gid, uid, ev, bot, name):
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    title = "打卡"
    if uid not in zhaomu[gid]:
        msg = "不在公会里哦~"
        await bot.send(ev, msg, at_sender=True)
        return
    if zhaomu[gid][uid][title] > 0:
        if priv.get_user_priv(ev) < 21:
            await bot.send(ev, f'你今天已经打卡了', at_sender=True)
        else:
            await bot.send(ev, f'已经打卡了下个🔨班', at_sender=True)
    else:
        zhaomu[gid][uid][title] = 1
        # zhaomu[gid][uid]['群名片'] = name
        zhaomu[gid][uid]['出刀'] = ""
        zhaomu[gid][uid]['预约'] = ""
        savefile()
        await bot.send(ev, f'打卡成功，感谢公会战付出~', at_sender=True)
    return

async def process_table_off(bot, ev, gid, checker):
    if gid not in zhaomu:
        text = "公会没有建立哦qwq"
        await bot.send(ev, text)
        return
    msg = []
    if len(zhaomu[gid].keys()) == 0:
        text = "公会成员是零哦~~"
        await bot.send(ev, text)
        return
    for member in zhaomu[gid].keys():
        if zhaomu[gid][member]['打卡'] == checker:
            msg.append(zhaomu[gid][member]['群名片'])

    if msg == []:
        msg = "没有人下班TAT"

    if  isinstance(msg, str):
        await bot.send(ev, msg)
    else:
        new_msg = []
        if checker == 1:
            new_msg = [f'下班人数{len(msg)}:'] + msg
        else:
            new_msg = [f'在岗人数{len(msg)}:'] + msg
    await bot.send(ev, '\n'.join(new_msg))

# 目录-上下班(method)--------------------------------------------------------------------------------------------------------------------

@sv.on_fullmatch('下班', '打卡')
async def add_off(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    await add_message_off(gid, uid, ev, bot, name)

@sv.on_prefix('代刀下班', '下班', '打卡')
async def add_off_other(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    # name = await find_name(bot, gid, uid)
    name = ""
    await add_message_off(gid, uid, ev, bot, name)
    

@sv.on_fullmatch('取消下班', '取消打卡')
async def delete_single_off(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    await delete_user_off(gid, uid, ev, bot, name)

@sv.on_prefix('取消下班', '取消打卡')
async def delete_single_off_other(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    # name = await find_name(bot, gid, uid)
    name = ""
    await delete_user_off(gid, uid, ev, bot, name)

# 目录-SL(func)--------------------------------------------------------------------------------------------------------------------

async def restore_sl(gid, uid, ev, bot, name):
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    title = "SL"
    if uid not in zhaomu[gid]:
        msg = "不在公会里哦~"
        await bot.send(ev, msg, at_sender=True)
        return
    if zhaomu[gid][uid][title] == 0:
        await bot.send(ev, f'你SL还没使用哦', at_sender=True)
    else:
        zhaomu[gid][uid][title] = 0
        # zhaomu[gid][uid]['群名片'] = name
        savefile()
        await bot.send(ev, f'恢复SL次数~', at_sender=True)
    return

async def add_message_sl(gid, uid, ev, bot, name):
    if gid not in zhaomu:
        msg = "请建立公会先！！！指令：建会"
        await bot.send(ev, msg, at_sender=True)
        return
    title = "SL"
    if uid not in zhaomu[gid]:
        msg = "不在公会里哦~"
        await bot.send(ev, msg, at_sender=True)
        return
    if zhaomu[gid][uid][title] > 0:
        await bot.send(ev, f'你已经没有SL了', at_sender=True)
    else:
        zhaomu[gid][uid][title] = 1
        # zhaomu[gid][uid]['群名片'] = name
        savefile()
        await bot.send(ev, f'SL已记录', at_sender=True)
    return

# 目录-SL(method)--------------------------------------------------------------------------------------------------------------------

@sv.on_fullmatch('SL', 'sl', 'Sl', 'sL')
async def add_sl(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    await add_message_sl(gid, uid, ev, bot, name)

@sv.on_prefix('SL', 'sl', 'Sl', 'sL')
async def add_sl_other(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    # name = await find_name(bot, gid, uid)
    await add_message_sl(gid, uid, ev, bot, name)
    

@sv.on_fullmatch('取消SL', '取消sl', '取消Sl', '取消sL')
async def delete_single_sl(bot, ev):
    gid = str(ev.group_id)
    uid = str(ev.user_id)
    name = ev.sender['card'] or ev.sender['nickname'] or str(uid)
    if uid == "80000000":
        msg = "匿名个🔨"
        await bot.send(ev, msg)
        return
    await restore_sl(gid, uid, ev, bot, name)

@sv.on_prefix('取消SL', '取消sl', '取消Sl', '取消sL')
async def delete_single_sl_other(bot, ev):
    gid = str(ev.group_id)
    search_match = re.match(r'\[CQ:at,qq=([0-9]+)\] ?(\S*)', str(ev.message))
    try:
        uid = search_match.group(1)
    except:
        await bot.send(ev, f'请输入正确的格式RUA！”')
        return
    # name = await find_name(bot, gid, uid)
    await restore_sl(gid, uid, ev, bot, name)


# 目录-查班--------------------------------------------------------------------------------------------------------------------

@sv.on_fullmatch('查看下班','查询下班','查看下班表', '查询下班表')
async def check_off(bot, ev):
    gid = str(ev.group_id)
    checker = 1
    await process_table_off(bot, ev, gid, checker)

    

@sv.on_fullmatch('查看未打卡')
async def check_on(bot, ev):
    gid = str(ev.group_id)
    checker = 0
    await process_table_off(bot, ev, gid, checker)

# 目录-clear function--------------------------------------------------------------------------------------------------------------------

async def clear_form(bot, ev, title):
    gid = str(ev.group_id)
    if gid in zhaomu:
        for member in zhaomu[gid]:
            if title == "打卡" or title == "SL":
                zhaomu[gid][member][title] = 0
            else:
                zhaomu[gid][member][title] = ""
        savefile()
        return

@sv.on_fullmatch('清空下班表','清空下班')
async def cancle_zhaomu(bot, ev):
    if priv.get_user_priv(ev) < 21:
        await bot.send(ev, f'只能群管理设置呢 (:3[▓▓]')
        return
    await clear_form(bot, ev, "出刀")
    await clear_form(bot, ev, "预约")
    await clear_form(bot, ev, "挂树")
    await clear_form(bot, ev, "打卡")
    await clear_form(bot, ev, "SL")
    await bot.send(ev, '删除成功~~')
    return

@sv.on_fullmatch('清空公会战状态', '清空状态', '清空表格', '清空查刀')
# @on_command('清空公会战状态', only_to_me=True)
async def clear_checkout_all(bot, ev):
    if priv.get_user_priv(ev) < 21:
        await bot.send(ev, f'只能群管理设置呢 (:3[▓▓]')
        return
    await clear_form(bot, ev, "出刀")
    await clear_form(bot, ev, "预约")
    await clear_form(bot, ev, "挂树")
    await bot.send(ev, '删除成功~~')
    return

@sv.on_fullmatch('清空预约')
# @on_command('清空公会战状态', only_to_me=True)
async def clear_checkout_all(bot, ev):
    if priv.get_user_priv(ev) < 21:
        await bot.send(ev, f'只能群管理设置呢 (:3[▓▓]')
        return
    await clear_form(bot, ev, "预约")
    await bot.send(ev, '删除成功~~')
    return

@sv.on_fullmatch('清空出刀')
# @on_command('清空公会战状态', only_to_me=True)
async def clear_checkout_all(bot, ev):
    if priv.get_user_priv(ev) < 21:
        await bot.send(ev, f'只能群管理设置呢 (:3[▓▓]')
        return
    await clear_form(bot, ev, "出刀")
    await bot.send(ev, '删除成功~~')
    return

@sv.on_fullmatch('清空挂树')
# @on_command('清空公会战状态', only_to_me=True)
async def clear_checkout_all(bot, ev):
    if priv.get_user_priv(ev) < 21:
        await bot.send(ev, f'只能群管理设置呢 (:3[▓▓]')
        return
    await clear_form(bot, ev, "挂树")
    await bot.send(ev, '删除成功~~')
    return



@sv.scheduled_job('cron', hour='4')
async def auto_delete_form():
    print("test")
    if zhaomu == {}:
        return
    for group in zhaomu:
        for member in zhaomu[group]:
            zhaomu[group][member]["出刀"] = ""
            zhaomu[group][member]["预约"] = ""
            zhaomu[group][member]["挂树"] = ""
            zhaomu[group][member]["打卡"] = 0
            zhaomu[group][member]["SL"] = 0
    savefile()
    msg = "test"
    await sv.broadcast(msg, 'battleV3')
