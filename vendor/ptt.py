import sys
from PyPtt import PTT

def ptt_init():
    ID = 'mikk'
    PASSWORD = '19811128'

    ptt_bot = PTT.API(
        language=PTT.i18n.language.CHINESE,
        log_level=PTT.log.level.DEBUG,
        # 預設 3 秒後判定此畫面沒有可辨識的目標
        screen_time_out=5,
        # 預設 10 秒後判定此畫面沒有可辨識的目標
        # 適用於需要特別等待的情況，例如: 剔除其他登入、發文等等
        # 建議不要低於 10 秒，剔除其他登入最長可能會花費約 6 ~ 7 秒
        screen_long_timeout=15,
        # 預設 60 秒後判定此畫面沒有可辨識的目標
        # 適用於貼文等待的情況，建議不要低於 60 秒
        screen_post_timeout=120,
        # (預設值) PTT1
        # host=PTT.data_type.host_type.PTT1,
        host=PTT.data_type.host_type.PTT2,
        # host=PTT.data_type.host_type.LOCALHOST,
        # (預設值) WEBSOCKET
        # connect_mode=PTT.connect_core.connect_mode.WEBSOCKET,
        # connect_mode=PTT.connect_core.connect_mode.TELNET,
        # (預設值) 23
        # port=8888
    )

    # 登入
    try:
        ptt_bot.login(ptt_id, password)
    except PTT.exceptions.LoginError:
        ptt_bot.log('登入失敗')
        sys.exit()
    except PTT.exceptions.WrongIDorPassword:
        ptt_bot.log('帳號密碼錯誤')
        sys.exit()
    except PTT.exceptions.LoginTooOften:
        ptt_bot.log('請稍等一下再登入')
        sys.exit()

    ptt_bot.log('登入成功')

    # 登出
    ptt_bot.logout()