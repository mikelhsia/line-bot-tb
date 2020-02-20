import sys
from PyPtt import PTT

PTT_ID = 'mikk'
PTT_PASSWORD = '19811128'

class PTT_BOT():
    ptt_bot = None

    def __init__(self):
        self.ptt_bot = PTT.API(
            language=PTT.i18n.language.CHINESE,
            log_level=PTT.log.level.DEBUG,
            # 預設 3 秒後判定此畫面沒有可辨識的目標
            screen_time_out=5,
            # 預設 10 秒後判定此畫面沒有可辨識的目標
            # 適用於需要特別等待的情況，例如: 剔除其他登入、發文等等
            # 建議不要低於 10 秒，剔除其他登入最長可能會花費約 6 ~ 7 秒
            # screen_long_timeout=15,
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

    def login_and_fetch(self, num=60):
        # 登入
        try:
            self.ptt_bot.login(PTT_ID, PTT_PASSWORD, kick_other_login=False)
        except PTT.exceptions.LoginError:
            self.ptt_bot.log('登入失敗')
            return
        except PTT.exceptions.WrongIDorPassword:
            self.ptt_bot.log('帳號密碼錯誤')
            return
        except PTT.exceptions.LoginTooOften:
            self.ptt_bot.log('請稍等一下再登入')
            return

        self.ptt_bot.log('登入成功')

        post_info = self.ptt_bot.get_post(
            'VC_Style',
            post_index=int(num)
        )

        if post_info is not None:
            if post_info.delete_status != PTT.data_type.post_delete_status.NOT_DELETED:
                if post_info.delete_status == PTT.data_type.post_delete_status.MODERATOR:
                    self.ptt_bot.log(f'[板主刪除][{post_info.author}]')
                elif post_info.delete_status == PTT.data_type.post_delete_status.AUTHOR:
                    self.ptt_bot.log(f'[作者刪除][{post_info.author}]')
                elif post_info.delete_status == PTT.data_type.post_delete_status.UNKNOWN:
                    self.ptt_bot.log(f'[不明刪除]')
                return

            if post_info.is_lock:
                self.ptt_bot.log('[鎖文]')
                return

            if not post_info.pass_format_check:
                self.ptt_bot.log('[不合格式]')
                # return

            self.ptt_bot.log('Board: ' + post_info.board)
            self.ptt_bot.log('AID: ' + post_info.aid)
            self.ptt_bot.log('index:' + str(post_info.index))
            self.ptt_bot.log('Author: ' + post_info.author)
            # self.ptt_bot.log('Date: ' + post_info.date)
            self.ptt_bot.log('Title: ' + post_info.title)
            self.ptt_bot.log('content: ' + post_info.content)
            self.ptt_bot.log('Money: ' + str(post_info.money))
            # self.ptt_bot.log('URL: ' + post_info.web_url)
            # self.ptt_bot.log('IP: ' + post_info.ip)
            # 在文章列表上的日期
            self.ptt_bot.log('List Date: ' + post_info.list_date)
            # self.ptt_bot.log('地區: ' + post_info.location)
            # Since 0.8.19
            self.ptt_bot.log('文章推文數: ' + post_info.push_number)

            if post_info.unconfirmed:
                # Since 0.8.30
                self.ptt_bot.log('待證實文章')

            push_count = 0
            boo_count = 0
            arrow_count = 0

            for push_info in post_info.push_list:
                if push_info.type == PTT.data_type.push_type.PUSH:
                    push_type = '推'
                    push_count += 1
                if push_info.type == PTT.data_type.push_type.BOO:
                    push_type = '噓'
                    boo_count += 1
                if push_info.type == PTT.data_type.push_type.ARROW:
                    push_type = '箭頭'
                    arrow_count += 1

                author = push_info.author
                content = push_info.content

                buffer = f'{author} 給了一個{push_type} 說 {content}'
                if push_info.ip is not None:
                    buffer += f'來自 {push_info.ip}'
                buffer += f'時間是 {push_info.time}'
                self.ptt_bot.log(buffer)

            self.ptt_bot.log(f'Total {push_count} Pushs {boo_count} Boo {arrow_count} Arrow')
            return post_info.content

    def logout(self):
        # 登出
        self.ptt_bot.logout()