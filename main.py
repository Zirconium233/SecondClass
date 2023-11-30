import requests
import json
import configparser
import os
import traceback
cur_path = "./"
cfg_path = os.path.join(cur_path, "config.ini")
conf = configparser.ConfigParser()
conf.read(cfg_path, encoding="utf-8")
def update():
    conf.write(open(cfg_path, "w+", encoding="utf-8"))
def generate_combinations(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop() 

    backtrack(0, [])

    return result
def generate_combination_list(n):
    nums = list(range(1, n + 1))
    combinations = generate_combinations(nums)
    combinations = [combo for combo in combinations if combo]
    return combinations
class Answer:
    def __init__(self):
        self.url = "https://dekt.hfut.edu.cn/"
        self.netlearning = "/scReports/api/wx/netlearning/filter/condition"

        self.session = requests.Session()

        self.session.headers = {
            'Host': 'dekt.hfut.edu.cn',
            'Connection': 'keep-alive',
            'secret': conf.get("main", "secret"),
            'key_session': conf.get("main", "key_session"),
            'xweb_xhr': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8431',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wx1e3feaf804330562/89/page-frame.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.data = {
            "category":"",
            "columnType":"0",
        }
    def learn(self, id, ingnore=False):
        print(f"  学习文章id：{id}")
        if self.session.get(url=self.url+f"/scReports/api/wx/netlearning/{id}").status_code == 200:
            print("  打开文章成功")
        print("  等待30秒(等你妈直接答题)")
        questions = json.loads(self.session.get(url=self.url+f"/scReports/api/wx/netlearning/questions/{id}").text)
        if not ingnore:
            if questions["data"]["accquieCredit"] == True:
                print("  已经作答，跳过")
                return False
            elif questions["data"]["todayReach"] == True:
                print("  今日已经达到，拒绝继续答题")
                return False
        for question in questions["data"]["questions"]:
            print("  题目id：" + question["id"])
            if(question["queType"] == 1):
                print("    多选题，遍历多几次")
                for com in generate_combination_list(len(question["optionList"])):
                    ans = []
                    ansc = []
                    for i in com:
                        ans.append(question["optionList"][i-1]["id"])
                        ansc.append(question["optionList"][i-1]["optionContent"])
                    print("      作答：")
                    print("      ",ansc)
                    res = json.loads(self.session.post(url=self.url+f"/scReports/api/wx/netlearning/answer/{question['id']}", data=json.dumps(ans)).text)
                    print("      "+res["data"]["desc"])
                    if "错误" in res["data"]["desc"] :
                        continue
                    elif "恭喜" in res["data"]["desc"] :
                        break
                    else :
                        print("      这回复什么寄吧玩意")
                        return False
            elif (question["queType"] == 0):
                print("    单选题，好样的，直接遍历")
                for choice in question["optionList"]:
                    print("      选项内容：" + choice["optionContent"])
                    res = json.loads(self.session.post(url=self.url+f"/scReports/api/wx/netlearning/answer/{question['id']}", data=json.dumps([choice["id"]])).text)
                    print("      "+res["data"]["desc"])
                    if "错误" in res["data"]["desc"] :
                        continue
                    elif "恭喜" in res["data"]["desc"] :
                        break
                    else :
                        print("      这回复什么寄吧玩意")
                        return False
            else:
                print("这寄吧什么题啊")
            print("  题目通过。")
        return True
    def start(self, pages):
        for page in range(1,pages+1):
            passagelist = json.loads(self.session.post(url=self.url+f"/scReports/api/wx/netlearning/page/{page}/10", data=json.dumps(self.data)).text)
            for passage in passagelist["data"]["list"]:
                print("当前文章："+passage["id"])
                if passage["videoUrl"] != "" :
                    print("是视频，跳过先")
                elif passage["correct"] == "已完成":
                    print("已经完成，跳过")
                else:
                    print("满足条件，选定文章：" + passage["id"])
                    if self.learn(passage["id"]) :
                        print(f"积分加{passage['credits']}")
                    else :
                        print("答题失败，但没出事")
                        return
if __name__ == "__main__":
    print("----脚本开始----")
    print("首先现在只支持文章自动答题，视频理论上是一样的，\n但我实在忍受不了看3分钟视频去抓包测试，你可以自己试试看把视频用一样的方式处理")
    print("(改代码一个跳转就OK了，但我没测试能不能过先不说话)\n")
    print("secret="+conf.get("main", "secret")+"\n")
    print("key_session="+conf.get("main", "key_session")+"\n")
    c = input("确认无误开始: [y/n]")
    if c == 'y':
        try:
            ans = Answer()
            page = input("请输入最大搜索的页码：(直接回车就是2页)")
            if(page == ""):
                ans.start(2)
            else:
                ans.start(int(page))
            print("成功！")
        except Exception as e:
            print(e.__str__)
            print(traceback.format_exc())
    else:
        exit()