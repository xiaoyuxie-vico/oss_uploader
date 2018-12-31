# 使用Alfred上传图片到阿里OSS

由于七牛云不能使用而改用阿里云，迫切需要使用Alfred来简化上传图片到阿里oss然后获得url的过程，参考[CQHui的oss_upload项目](https://github.com/CQHui/oss_upload/blob/master/clipboard_data.py)重构了相关代码。

## 环境
- Mac OS
- python 2.7


## 功能
- 上传剪切板中的图片到oss，获得url或者markdown的url格式（2018.12.31）；
- 待补充：
    - 上传本地文件；
    - 重命名文件；
    - 修改保存在oss的路径；

## 使用方法

1. 下载代码到本地：
```
git clone https://github.com/xiaoyuxie-vico/oss_uploader.git
```

2. 进入`oss_uploader`文件夹，双击`oss.alfredworkflow`；

3. 进入`oss_uploader`文件夹，修改`oss_uploader.py`中的配置信息，包括：
```
kargs = {
    'access_key_id': '<你的AccessKeyId>',
    'access_key_secret': '<你的AccessKeySecret>',
    'bucket_name': '<你的Bucket名>',
    'endpoint': 'http://oss-cn-hangzhou.aliyuncs.com',  # example
}
```
可以参考阿里官方链接[如何获取AccessKeyId和AccessKeySecret
](https://help.aliyun.com/knowledge_detail/48699.html)查找自己的相关信息。

4. 进入`Alfred`的`workflow`中的`oss`，双击`oss`进入脚本路径设置，配置如下：
```
python /PATH/oss_uploader/oss_uploader.py
```

5. 截图保存到剪切版，可以使用[截图(Jietu)-快速标注、便捷分享的截屏工具](https://itunes.apple.com/cn/app/%E6%88%AA%E5%9B%BE-jietu-%E5%BF%AB%E9%80%9F%E6%A0%87%E6%B3%A8-%E4%BE%BF%E6%8D%B7%E5%88%86%E4%BA%AB%E7%9A%84%E6%88%AA%E5%B1%8F%E5%B7%A5%E5%85%B7/id1059334054?mt=12)进行操作；

5. 使用快捷键如`option + space`进入`Aflred`，输入`oss`如一切正常会显示`上传ing`，之后选择`Single url`或者`Url for markdown`获取需要的格式，详细如下：
    - `Single url`: url;
    - `Url for markdown`: ![](url)

## 其他
后续功能还会完善，如有疑问可联系xiaoyuxie.vico@gmail.com
