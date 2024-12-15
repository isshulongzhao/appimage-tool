# appimage-tool

`appimage-tool` 用于将可执行二进制文件快速转换为 AppImage 格式。

## 用法

./appimage-tool -h
![image](https://github.com/user-attachments/assets/ea8d61aa-3280-40f7-b276-7e5d609e7d17)

## 单个文件转换
./appimage-tool --path /root/tools/xinchuang/original/erfrp_s_X86_64 --arch x86_64

![image](https://github.com/user-attachments/assets/26da7ddc-d958-44eb-bd01-0db83ade46c2)

## 自动识别文件架构
如果不指定文件架构，`appimage-tool` 会通过 `file` 命令自动识别文件架构。若识别失败，默认会使用 `x86_64` 类型进行转换。

./appimage-tool --path /root/tools/xinchuang/original/erfrp_s_X86_64 

![image](https://github.com/user-attachments/assets/45779cd7-f6d2-46e4-875d-5346fff1743d)

## 批量转换
通过 `--list` 参数可以批量转换文件，其中 `list.txt` 中每一行都是二进制文件的路径。

./appimage-tool --list list.txt
![image](https://github.com/user-attachments/assets/0d6e0311-26b9-40b7-9b4a-a841e889c6b5)

