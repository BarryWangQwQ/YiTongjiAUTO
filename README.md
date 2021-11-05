# YiTongjiAUTO
### 一个可以自动化上报"易统计"的服务程序 (Python实现).  
#### A service that automates the reporting of "YiTongJi".
### ✅ 本地运行：
#### 拉取项目 https://github.com/BarryWangQwQ/YiTongjiAUTO.git  
#### 推荐使用Python3.9  
#### 修改源代码并运行 / 直接运行 YiTongJiAUTO.exe 使用命令进行配置
#### 需要获取: token  
### ⚙️ 如何获取 易统计的token ？
#### 1. PC端使用浏览器(推荐Chrome)访问易统计官网：https://www.ioteams.com/ncov/#/login
#### 2. 登录后 按F12 进入开发者调试工具.
#### 3. 进入Application栏目 找到ncov-access-token-h5对应的value, 其value即为token.
![Image text](https://gitee.com/xuben99/auto-punch/raw/master/img/img.png)
### 📝 CLI命令
| 命令 | 用途 |
| --- | --- |
| `run` | `部署服务` |
| `stop` | `关闭/停止服务` |
| `time set` | `设置打卡时间` |
| `add` | `向队列添加新的打卡对象` |
| `show` | `查看已记录的打卡队列` |
| `delete` | `删除打卡对象` |
| `describe` | `查看程序自述` |