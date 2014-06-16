weiboParser
===========

这个python项目主要进行新浪微博上的信息抓取，提供如下两个抓取功能:

- 抓取任意数量的ID的最近n天内的原创微博，n可以用户指定，最终以excel的形式保存下来。
- 抓取满足过滤条件的微博，需要给定ID、起始日期、结束日期和关键词，返回结果同样保存在excel。
  
被抓取下的信息包含如下的字段：
- weiboID
- 微博内容
- 赞数
- 转发数
- 评论数

change sth

程序结构如下：
- activityApp.py : 程序入口 提示输入信息
- weibo/weiboCNParser : 抓取weibo信息的类。
- utils：提供写入excel的接口
- pyDatabase：提供与数据库的接口 -- 待补充
