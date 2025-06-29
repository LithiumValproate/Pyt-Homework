import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime
import json

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
GUILD = int(os.getenv('GUILD_ID'))

# 配置意图和机器人
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 存储成员数据的文件
MEMBER_DATA_FILE = 'member_data.json'

# 存储成员数据的字典
member_data = {}

# 目标身份组ID
ROLE_ID = None  # 请在机器人准备就绪后设置


# 加载成员数据
def load_member_data():
    global member_data
    try:
        with open(MEMBER_DATA_FILE, 'r') as f:
            member_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        member_data = {}


# 保存成员数据
def save_member_data():
    with open(MEMBER_DATA_FILE, 'w') as f:
        json.dump(member_data, f)


@bot.event
async def on_ready():
    print(f'{bot.user} 已连接到Discord!')
    guild = bot.get_guild(GUILD)
    if guild is None:
        print(f"无法找到ID为{GUILD}的服务器")
        return

    # 加载成员数据
    load_member_data()

    # 初始化数据库中不存在的成员
    for member in guild.members:
        if str(member.id) not in member_data:
            member_data[str(member.id)] = {
                'join_date': member.joined_at.timestamp() if member.joined_at else datetime.datetime.now().timestamp(),
                'message_count': 0
            }

    save_member_data()


@bot.event
async def on_message(message):
    # 忽略机器人自己的消息
    if message.author.bot:
        return

    # 记录消息计数
    author_id = str(message.author.id)
    if author_id not in member_data:
        # 如果是新成员，记录其加入日期
        member_data[author_id] = {
            'join_date': message.author.joined_at.timestamp() if message.author.joined_at else datetime.datetime.now().timestamp(),
            'message_count': 1
        }
    else:
        member_data[author_id]['message_count'] += 1

    # 检查是否满足条件
    await check_role_eligibility(message.author)

    # 保存数据
    save_member_data()

    # 处理命令
    await bot.process_commands(message)


async def check_role_eligibility(member):
    member_id = str(member.id)
    if member_id not in member_data:
        return

    # 计算加入时间（天数）
    join_timestamp = member_data[member_id]['join_date']
    join_date = datetime.datetime.fromtimestamp(join_timestamp)
    days_since_join = (datetime.datetime.now() - join_date).days

    # 获取消息计数
    message_count = member_data[member_id]['message_count']

    # 检查用户是否拥有comres或rezus身份组
    excluded_roles = ['comres', 'rezus']
    has_excluded_role = any(role.name.lower() in excluded_roles for role in member.roles)

    if has_excluded_role:
        # 如果用户有排除的身份组，则不添加lives身份组
        return

    # 检查条件：加入超过7天且发言超过20条
    if days_since_join >= 7 and message_count >= 20:
        # 获取lives
        guild = member.guild
        role = guild.get_role(ROLE_ID)

        # 如果成员还没有这个身份组，就添加
        if role and role not in member.roles:
            try:
                await member.add_roles(role, reason='该成员加入服务器超过一周且发言超过20条')
                print(f"已将lives添加给 {member.name}")
            except discord.Forbidden:
                print(f"无权限将身份组添加给 {member.name}")
            except discord.HTTPException as e:
                print(f"添加身份组时出错: {e}")


@bot.command(name='stats')
async def stats(ctx, member: discord.Member = None):
    """显示成员的统计信息"""
    if member is None:
        member = ctx.author

    member_id = str(member.id)
    if member_id not in member_data:
        await ctx.send(f"{member.display_name} 的数据不存在。")
        return

    join_timestamp = member_data[member_id]['join_date']
    join_date = datetime.datetime.fromtimestamp(join_timestamp)
    days_since_join = (datetime.datetime.now() - join_date).days
    message_count = member_data[member_id]['message_count']

    await ctx.send(f"**{member.display_name}** 的统计信息:\n"
                   f"加入天数: {days_since_join}\n"
                   f"发言数量: {message_count}\n"
                   f"是否有资格获得lives: {'是' if days_since_join >= 7 and message_count >= 20 else '否'}")


@bot.command(name='leaderboard')
async def leaderboard(ctx, count: int = 10):
    """显示发言排行榜"""
    guild = ctx.guild
    sorted_members = sorted(member_data.items(), key=lambda x: x[1]['message_count'], reverse=True)

    embed = discord.Embed(title='发言排行榜', color=discord.Color.blue())

    for i, (member_id, data) in enumerate(sorted_members[:count], start=1):
        member = guild.get_member(int(member_id))
        if member:
            name = member.display_name
        else:
            name = f"未知成员 ({member_id})"

        embed.add_field(
            name=f"{i}. {name}",
            value=f"发言数: {data['message_count']}",
            inline=False
        )

    await ctx.send(embed=embed)


# 启动机器人
bot.run(TOKEN)
