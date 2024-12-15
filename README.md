# appimage-tool

`appimage-tool` 用于将可执行二进制文件快速转换为 AppImage 格式。

## 用法

./appimage-tool -h

![1734265109649](https://github.com/user-attachments/assets/18a5834e-061b-473a-88c0-d2ca3edf8c88)

## 单个文件转换

./appimage-tool --path /root/tools/xinchuang/original/erfrp_s_X86_64 --arch x86_64

![1734265052398](https://github.com/user-attachments/assets/7903f0a1-967e-423f-99fd-554eb13a00b9)

## 自动识别文件架构
如果不指定文件架构，`appimage-tool` 会通过 `file` 命令自动识别文件架构。若识别失败，默认会使用 `x86_64` 类型进行转换。

![1734264880578](https://github.com/user-attachments/assets/745acf96-447e-4e7c-8e26-bfeab26fa707)

## 批量转换
通过 `--list` 参数可以批量转换文件，其中 `list.txt` 中每一行都是二进制文件的路径。

./appimage-tool --list list.txt

![1734264941760](https://github.com/user-attachments/assets/961e0b7d-171f-4518-8f44-926e7bfaede6)

