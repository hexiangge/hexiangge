import random
from langbot import WeChatBot, Message
from config import ADMIN_USER
from database import get_user_score, update_user_score, record_bet_history


class BettingPlugin(WeChatBot):
    def handle_message(self, message: Message):
        from_user = message.sender
        content = message.text

        user_score = get_user_score(from_user)

        if from_user == ADMIN_USER and content.startswith('加积分'):
            parts = content.split(' ')
            if len(parts) == 3:
                target_user = parts[1]
                try:
                    points = int(parts[2])
                    target_score = get_user_score(target_user)
                    new_score = target_score + points
                    update_user_score(target_user, new_score)
                    self.send_text(f'已为 {target_user} 增加 {points} 积分，当前积分为 {new_score}', from_user)
                except ValueError:
                    self.send_text('请输入正确的积分值', from_user)
            else:
                self.send_text('请使用格式：加积分 用户openid 积分值', from_user)
        elif content.startswith('排列5'):
            bet_content = content[3:].strip()
            if len(bet_content) == 5 and bet_content.isdigit():
                winning_numbers = ''.join(str(random.randint(0, 9)) for _ in range(5))
                is_win = bet_content == winning_numbers
                score_change = 100 if is_win else -20
                new_score = user_score + score_change
                if new_score < 0:
                    new_score = 0
                update_user_score(from_user, new_score)
                record_bet_history(from_user, '排列5', bet_content, winning_numbers, is_win, score_change)
                if is_win:
                    self.send_text(f'恭喜你猜对啦！中奖号码为 {winning_numbers}，增加100积分，当前积分: {new_score}', from_user)
                else:
                    self.send_text(f'很遗憾，猜错了。中奖号码为 {winning_numbers}，扣除20积分，当前积分: {new_score}', from_user)
            else:
                self.send_text('请使用格式：排列5 5位数字进行竞猜', from_user)
        elif content.startswith('足球'):
            bet_content = content[2:].strip()
            if bet_content in ['主胜', '客胜', '平局']:
                results = ['主胜', '客胜', '平局']
                winning_result = random.choice(results)
                is_win = bet_content == winning_result
                score_change = 80 if is_win else -15
                new_score = user_score + score_change
                if new_score < 0:
                    new_score = 0
                update_user_score(from_user, new_score)
                record_bet_history(from_user, '足球比赛胜负', bet_content, winning_result, is_win, score_change)
                if is_win:
                    self.send_text(f'恭喜你猜对啦！比赛结果为 {winning_result}，增加80积分，当前积分: {new_score}', from_user)
                else:
                    self.send_text(f'很遗憾，猜错了。比赛结果为 {winning_result}，扣除15积分，当前积分: {new_score}', from_user)
            else:
                self.send_text('请使用格式：足球 主胜/客胜/平局 进行竞猜', from_user)
        elif content.startswith('双色球'):
            parts = content[3:].strip().split(' ')
            if len(parts) == 7 and all(part.isdigit() for part in parts):
                red_bets = sorted([int(part) for part in parts[:6]])
                blue_bet = int(parts[6])
                if all(1 <= num <= 33 for num in red_bets) and 1 <= blue_bet <= 16:
                    red_winning = sorted(random.sample(range(1, 34), 6))
                    blue_winning = random.randint(1, 16)
                    is_win = red_bets == red_winning and blue_bet == blue_winning
                    score_change = 500 if is_win else -50
                    new_score = user_score + score_change
                    if new_score < 0:
                        new_score = 0
                    update_user_score(from_user, new_score)
                    bet_content = ' '.join(map(str, red_bets)) + ' ' + str(blue_bet)
                    winning_numbers = ' '.join(map(str, red_winning)) + ' ' + str(blue_winning)
                    record_bet_history(from_user, '双色球', bet_content, winning_numbers, is_win, score_change)
                    if is_win:
                        self.send_text(f'恭喜你猜对啦！中奖号码为 {winning_numbers}，增加500积分，当前积分: {new_score}', from_user)
                    else:
                        self.send_text(f'很遗憾，猜错了。中奖号码为 {winning_numbers}，扣除50积分，当前积分: {new_score}', from_user)
                else:
                    self.send_text('红球号码需在1 - 33之间，蓝球号码需在1 - 16之间，请重新输入')
            else:
                self.send_text('请使用格式：双色球 6个红球号码 1个蓝球号码 进行竞猜')
        elif content.startswith('大乐透'):
            parts = content[3:].strip().split(' ')
            if len(parts) == 7 and all(part.isdigit() for part in parts):
                front_bets = sorted([int(part) for part in parts[:5]])
                back_bets = sorted([int(part) for part in parts[5:]])
                if all(1 <= num <= 35 for num in front_bets) and all(1 <= num <= 12 for num in back_bets):
                    front_winning = sorted(random.sample(range(1, 36), 5))
                    back_winning = sorted(random.sample(range(1, 13), 2))
                    is_win = front_bets == front_winning and back_bets == back_winning
                    score_change = 800 if is_win else -80
                    new_score = user_score + score_change
                    if new_score < 0:
                        new_score = 0
                    update_user_score(from_user, new_score)
                    bet_content = ' '.join(map(str, front_bets)) + ' ' + ' '.join(map(str, back_bets))
                    winning_numbers = ' '.join(map(str, front_winning)) + ' ' + ' '.join(map(str, back_winning))
                    record_bet_history(from_user, '大乐透', bet_content, winning_numbers, is_win, score_change)
                    if is_win:
                        self.send_text(f'恭喜你猜对啦！中奖号码为 {winning_numbers}，增加800积分，当前积分: {new_score}', from_user)
                    else:
                        self.send_text(f'很遗憾，猜错了。中奖号码为 {winning_numbers}，扣除80积分，当前积分: {new_score}', from_user)
                else:
                    self.send_text('前区号码需在1 - 35之间，后区号码需在1 - 12之间，请重新输入')
            else:
                self.send_text('请使用格式：大乐透 5个前区号码 2个后区号码 进行竞猜')
        else:
            self.send_text('不支持的竞猜类型或指令，请重新输入')
