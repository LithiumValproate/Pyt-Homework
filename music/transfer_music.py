import pandas as pd
import getpass
from pyncm import apis
from pyncm import GetCurrentSession, DumpSessionAsString, LoadSessionFromString

# ==========================================================
#                         用户配置区域
#                 请将你的 XLSX 文件路径填入下方
# ==========================================================
XLSX_FILE_PATH = 'Liked.xlsx'


# ==========================================================
def login(phone):
    """登录网易云音乐"""
    try:
        # 发送验证码
        print(f'正在向 {phone} 发送验证码...')
        send_result = apis.login.SetSendRegisterVerifcationCodeViaCellphone(phone, ctcode=86)
        if send_result.get('code') != 200:
            print(f'❌ 发送验证码失败: {send_result}')
            return False
        captcha = input('请输入收到的验证码: ').strip()
        # 验证验证码
        verify_result = apis.login.GetRegisterVerifcationStatusViaCellphone(phone, captcha, ctcode=86)
        if verify_result.get('code') != 200:
            print(f'❌ 验证码错误: {verify_result}')
            return False
        # 登录
        nickname = 'transfer_script'  # 随便填
        password = getpass.getpass('请输入你的网易云音乐密码: ')
        login_result = apis.login.SetRegisterAccountViaCellphone(phone, captcha, nickname, password)
        if login_result.get('code') == 200:
            print('✅ 验证码登录成功！')
            save = input('是否保存本次登录会话以便下次免登录？[y/N]: ').strip().lower()
            if save == 'y':
                session_str = DumpSessionAsString(GetCurrentSession())
                with open('netease_session.txt', 'w') as f:
                    f.write(session_str)
                print('已保存会话到 netease_session.txt')
            return True
        else:
            print(f'❌ 登录失败: {login_result}')
            return False

    except Exception as e:
        print(f'❌ 登录失败: {e}')
        print('请检查你的账号信息或尝试其他登录方式。')
        return False


def try_load_session():
    """尝试加载本地保存的会话"""
    try:
        with open('netease_session.txt', 'r') as f:
            session_str = f.read()
        LoadSessionFromString(session_str)
        print('✅ 已加载本地会话，无需再次登录。')
        return True
    except Exception:
        return False


def search_song_id(song_name, artist):
    """根据歌名和歌手搜索歌曲ID"""
    keyword = f'{song_name} {artist}'
    print(f'🔍 正在搜索: {keyword}')
    try:
        result = apis.cloudsearch.GetSearchResult(keyword=keyword, limit=1)
        if result['result']['songs']:
            song_id = result['result']['songs'][0]['id']
            found_name = result['result']['songs'][0]['name']
            found_artist = result['result']['songs'][0]['ar'][0]['name']
            print(f'  🎶 找到歌曲: {found_name} - {found_artist} (ID: {song_id})')
            return song_id, found_name, found_artist
        else:
            print(f'  ⚠️ 未找到歌曲: {song_name} - {artist}')
            return None, None, None
    except Exception as e:
        print(f'  ❌ 搜索时发生错误: {e}')
        return None, None, None


def main():
    """主函数"""
    phone_number = input('请输入手机号')
    # 优先尝试加载本地会话
    if try_load_session():
        logged_in = True
    else:
        logged_in = login(phone_number)
    if not logged_in:
        return

    # 2. 从 XLSX 文件读取歌曲列表
    song_ids_to_add = []
    # 存储原始歌曲和搜索结果的对比信息
    comparison_data = []
    
    try:
        # 使用 pandas 读取 Excel 文件
        df = pd.read_excel(XLSX_FILE_PATH)

        # 检查列名是否存在
        if 'TrackName' not in df.columns or 'ArtistName' not in df.columns:
            print(f'❌ 错误: Excel 文件 \'{XLSX_FILE_PATH}\' 必须包含 \'TrackName\' 和 \'ArtistName\' 两列。')
            return

        # 遍历 DataFrame 的每一行
        for index, row in df.iterrows():
            song_name = str(row['TrackName']).strip()
            artist = str(row['ArtistName']).strip()
            if song_name and artist and song_name != 'nan' and artist != 'nan':
                song_id, found_name, found_artist = search_song_id(song_name, artist)
                if song_id:
                    song_ids_to_add.append(str(song_id))
                    # 添加原始和搜索结果到比较数据
                    comparison_data.append({
                        '原歌曲名': song_name,
                        '原歌手': artist,
                        '搜索到的歌曲名': found_name,
                        '搜索到的歌手': found_artist,
                        '歌曲ID': song_id,
                        '状态': '✅ 已找到'
                    })
                else:
                    # 记录未找到的歌曲
                    comparison_data.append({
                        '原歌曲名': song_name,
                        '原歌手': artist,
                        '搜索到的歌曲名': '未找到',
                        '搜索到的歌手': '未找到',
                        '歌曲ID': '无',
                        '状态': '❌ 未找到'
                    })

    except FileNotFoundError:
        print(f'❌ 错误: 找不到 Excel 文件 \'{XLSX_FILE_PATH}\'。请检查文件路径是否正确。')
        return
    except Exception as e:
        print(f'❌ 读取 Excel 文件时发生错误: {e}')
        return

    if not song_ids_to_add:
        print('💨 Excel 文件中没有找到任何有效歌曲，程序结束。')
        return

    print(f'\n共找到 {len(song_ids_to_add)} 首歌曲准备导入。')
    
    # 显示比较表格
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        print("\n歌曲信息比较表格:")
        print(comparison_df.to_string(index=False))
        
        # 可选: 保存比较表格到Excel
        save_comparison = input('是否保存歌曲对比表格到Excel？[y/N]: ').strip().lower()
        if save_comparison == 'y':
            comparison_file = 'song_comparison.xlsx'
            comparison_df.to_excel(comparison_file, index=False)
            print(f'已保存对比表格到 {comparison_file}')

    new_playlist_name = input('请输入新歌单名称（默认 \'转移的喜欢\'）: ').strip() or '转移的喜欢'

    # 3. 创建新歌单
    try:
        print(f'正在创建新歌单: \'{new_playlist_name}\'...')
        create_result = apis.playlist.SetCreatePlaylist(name=new_playlist_name)
        if create_result['code'] == 200:
            playlist_id = create_result['id']
            print(f'✅ 歌单创建成功！ID: {playlist_id}')
        else:
            print(f'❌ 创建歌单失败: {create_result.get("message", "未知错误")}')
            return
    except Exception as e:
        print(f'❌ 创建歌单时发生严重错误: {e}')
        return

    # 4. 将歌曲添加到歌单
    try:
        print('正在将歌曲添加到歌单中...')
        add_result = apis.playlist.SetManipulatePlaylistTracks(song_ids_to_add, playlist_id, op='add')
        if add_result['code'] == 200:
            print(f'🎉 成功！{len(song_ids_to_add)} 首歌曲已全部添加到歌单 \'{new_playlist_name}\' 中！')
        else:
            print(f'❌ 添加歌曲失败: {add_result}')
    except Exception as e:
        print(f'❌ 添加歌曲时发生严重错误: {e}')


if __name__ == '__main__':
    main()
