import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv(".env")
_TOKEN_ = os.getenv("TOKEN")
_GUILD_ID_ = int(os.getenv("GUILD_ID"))
_CHANNEL_ = int(os.getenv("CHAN_ID"))
ROLE_0 = "news"  # 自动分配的角色
ROLE_1 = "tukas"  # 回答正确后分配的角色

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


class QuizView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 不会自动超时

    @discord.ui.button(label="3", style=discord.ButtonStyle.secondary, custom_id="quiz_3")
    async def option_3(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("不正解です。", ephemeral=True)

    @discord.ui.button(label="4", style=discord.ButtonStyle.secondary, custom_id="quiz_4")
    async def option_4(self, button: discord.ui.Button, interaction: discord.Interaction):
        role_0 = discord.utils.get(interaction.guild.roles, name=ROLE_0)
        role_1 = discord.utils.get(interaction.guild.roles, name=ROLE_1)
        if role_1:
            await interaction.user.add_roles(role_1)
            await interaction.user.remove_roles(role_0)
            await interaction.response.send_message("正解です！ロールを付与しました。", ephemeral=True)
        else:
            await interaction.response.send_message("ロールが見つかりません。", ephemeral=True)

    @discord.ui.button(label="5", style=discord.ButtonStyle.secondary, custom_id="quiz_5")
    async def option_5(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("不正解です。", ephemeral=True)


@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user} (ID: {client.user.id})')


@client.event
async def on_member_join(member):
    if member.guild.id != _GUILD_ID_:
        return

    guild = member.guild
    chan = guild.get_channel(_CHANNEL_)

    # 1) 自动分配 news 角色
    news_role = discord.utils.get(guild.roles, name=ROLE_0)
    if news_role:
        await member.add_roles(news_role)

    # 2) 在验证频道发欢迎+题目
    if chan:
        await chan.send(
            f"👋 ようこそ、{member.mention} さん！**{guild.name}** へ参加ありがとうございます！\n"
            f"あなたには仮のロール **{ROLE_0}** が付与されました。\n"
            f"こちらのチャンネルで `2+2 = ?` の質問に答えて、正式なロール **{ROLE_1}** を取得してください。",
            view=QuizView()
        )

    # 也尝试私信
    try:
        await member.send(
            f"ようこそ、**{guild.name}** へ！\n"
            f"あなたには仮のロール **{ROLE_0}** が付与されました。\n"
            f"{chan.mention} チャンネルで `2+2 = ?` の質問に答えると、ロール **{ROLE_1}** が取得できます。",
            view=QuizView()
        )
    except discord.Forbidden:
        pass

@client.event
async def on_message(message):
    # 忽略机器人自身的消息
    if message.author == client.user:
        return

    # 只有具有管理角色权限的用户可以使用此命令
    if message.content == "!check_no_role" and message.author.guild_permissions.manage_roles:
        guild = message.guild
        # 查找仅具有默认 @everyone 角色的成员
        members_no_role = [member for member in guild.members if len(member.roles) <= 1]
        if members_no_role:
            response_lines = ["以下成员目前无其他角色："]
            for member in members_no_role:
                response_lines.append(f"- {member.mention} ({member.name}#{member.discriminator})")
            response = "\n".join(response_lines)
        else:
            response = "所有成员都至少拥有一个额外角色。"
        await message.channel.send(response)


client.run(_TOKEN_)
