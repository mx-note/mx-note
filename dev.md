# mx-note api docs

默认账号：admin
默认密码：123456
默认端口：6600

## 读
### 列出note下的所有文件夹/分类

```/api/v1/list/floder```

类：列出

返回:
```json
[
  {
    "author": "admin",
    "createTime": "1761598621",
    "description": "\u4ee3\u7801",
    "floder": "codes",
    "level": 1
  },
  {
    "author": "system",
    "createTime": "1761598621",
    "description": "\u9ed8\u8ba4\u5206\u7c7b",
    "floder": "default",
    "level": 0
  }
]
```

### 获取note的详细信息
```/api/v1/list/getNoteInfo```

类：列出

需要的参数:
- flodername: 文件夹名称(必须)
- notename: 笔记名称(必须)

返回：
```json
{
  "author": "system",
  "createTime": "1761598621",
  "description": "\u8fd9\u662f\u7cfb\u7edf\u9ed8\u8ba4\u7684\u7b14\u8bb0",
  "father-floder": "default",
  "level": 0
}
```
