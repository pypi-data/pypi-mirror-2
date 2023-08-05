ChangeLog 书写约定
+++++++++++++++++++++++++++++

本约定用于定义 changelog 的书写格式，同样可以应用于版本管理系统内的提交日志信息格式.

ChangeLog 的第一行应该为作者信息，格式为::
	
	YYYY-MM-DD  John Doe  <johndoe@example.com>
	
其中日期与名字间必须为两个空格，名字与可选的邮箱地址之间亦为两个空格.

参考实例::
	
	2009-08-07  alec  <timbaby2008@gmail.com>
	
	* khan/notification.py : 完全重构，所有依赖必须立即更改.
	* khan/tests/test_notification.py: 重写
	* khan/util.py(requestTypes): 
		RequestTypes 重命名为 requestTypes
		requestTypes.XMLRPC 改名为 requestTypes.XMLPOST
		requestTypes.JSONRPC 改名为 requestTypes.JSONPOST
	+ khan/security/auth.py: 
		增加了 new_request_classifer() 函数, make_auth_middleware 默认使用 new_request_classifer 而不是 repoze.who 里的 default_request_classifer
	* setup.py: 更改原来 notification.py 定义的 egg entry point.
	
条目前的符号的意义
^^^^^^^^^^^^^^^^^^^^^^

*  **\+**  增加新特性
*  **\-**   bug 修正或者移除
*  **\***  bug 修正或改善
	
