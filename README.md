# GDOU_srun_login
## for GDOUer to auto connect their new god damn network
## 广东海洋大学版 支持无线接入
#### 支持edge,chrome浏览器 （仅提供windows下程序)
##### 内存占用 < 30mb
> how?  <br>
  do not use 10.129.1.1 but 1.1.1.1 instead.  <br>
  use playwright(better than selenium).  <br>
  you can now avoid problems for requests.  <br>
  but require more memory.  <br>

```python
#main function
browser = playwright.chromium.launch(headless=True, channel=msedge)
context = browser.new_context()
page = context.new_page()
print('url: ' + testurl)
page.goto(testurl)
print('account: ' + account)
page.locator("[placeholder=\"请输入账号\"]").fill(account)  # .type(account)
print('password: ' + len(password) * '*')
page.locator("[placeholder=\"请输入密码\"]").fill(password)
page.locator("xpath=//*[@id='protocol']").click()
print('submit')
page.locator("text=登录").click()
browser.close()

```
I use requests to replace ping3  <br>
~~provide log out function~~  <br>
it still there  <br>
![Jc4kL.jpeg](https://i.328888.xyz/2023/03/15/Jc4kL.jpeg)
