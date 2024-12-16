import os
import subprocess
import sys

import argparse


def create_directories(name):
    dirs = [
        f"./appimage/{name}/usr/bin",
        f"./appimage/{name}/usr/lib",
        f"./appimage/{name}/usr/share/applications",
        f"./appimage/{name}/usr/share/icons/hicolor/256x256/apps",
        f"./appimages",
    ]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def copy_files(name, path):
    """修改依赖文件内容,设置权限并拷贝到相应目录"""
    # 使用 sys._MEIPASS 获取打包后的解压路径
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = '.'  # 如果不是打包后运行，使用当前目录

    # 获取相关文件路径
    desktop_file = os.path.join(base_path, "yilai", "myapp.desktop")
    app_run_file = os.path.join(base_path, "yilai", "AppRun")

    # 修改文件内容
    os.system(f"sed -i 's|^Exec=.*|Exec=/usr/bin/{os.path.basename(path)}|' {desktop_file}")
    replacement_line = f'exec "${{HERE}}/usr/bin/{os.path.basename(path)}" "$@"'
    os.system(f"sed -i '/^exec/c\\{replacement_line}' {app_run_file}")

    # 拷贝依赖文件
    os.system(f"cp {os.path.join(base_path, 'yilai', 'myapp.png')} ./appimage/{name}/myapp.png")
    os.system(f"cp {app_run_file} ./appimage/{name}/AppRun")
    os.system(f"cp {desktop_file} ./appimage/{name}/myapp.desktop")
    os.system(f"cp {path} ./appimage/{name}/usr/bin")

    # 设置文件可执行权限
    os.chmod(f"./appimage/{name}/AppRun", 0o755)
    os.chmod(f"./appimage/{name}/usr/bin/{os.path.basename(path)}", 0o755)


def build_appimage(name, arch, path):
    """使用 appimagetool 打包 AppImage"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = '.'

    # 使用 sys._MEIPASS 获取解压后的 appimagetool 路径
    appimage_tool = os.path.join(base_path, 'dabao', 'appimagetool-x86_64.AppImage')
    runtime_file = os.path.join(base_path, 'dabao', f'runtime-{arch}')
    appimage_file = f"./appimages/{os.path.basename(path)}.AppImage"

    if not os.path.exists(appimage_tool):
        print(f"错误: 找不到 {appimage_tool} 文件，请确保 AppImage 工具存在。")
        sys.exit(1)

    # 调用 appimagetool 打包 AppImage
    result = subprocess.run(
        [appimage_tool, "--runtime-file", runtime_file, f"./appimage/{name}/", appimage_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(f"错误: 打包 AppImage 失败: {result.stderr.decode('utf-8')}")
        sys.exit(1)


def build_appimages(list):
    with open(f"{list}", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            path = line.strip()
            if not os.path.exists(path):
                print(f"警告: 文件路径 {path} 不存在，跳过该项。")
                continue
            print(f"正在处理: {path}")
            appname = os.path.basename(path)
            result = subprocess.run(["file", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')  # 解码为字符串

            if "x86-64" in output:
                arch = "x86_64"
            elif "aarch64" in output:
                arch = "aarch64"
            else:
                print(f"警告: 文件 {path} 的架构类型未知，默认使用x86_64架构打包。")
            create_directories(appname)
            copy_files(appname, path)
            print(appname, arch, path)
            build_appimage(appname, arch, path)
            print(f"打包成功，AppImage 文件位于 ./appimages/{appname}.AppImage")


def main():
    global arch
    parser = argparse.ArgumentParser(description='AppImage格式文件快速转换工具')
    parser.add_argument('--path', type=str, help='指定二进制文件路径')
    parser.add_argument('--arch', type=str, help='架构类型,不指定时可自动识别')
    parser.add_argument('--list', type=str, help='指定一个txt文件批量转换')
    args = parser.parse_args()
    if not (args.path or args.list):
        print("错误：必须选择 --path 或 --list 中的一个。")
        sys.exit(1)

    if args.path and args.list:
        print("错误：只能选择 --path 或 --list 中的一个，而不能同时选择。")
        sys.exit(1)
    arch = "x86_64"
    if args.path:
        path = args.path
        appname = os.path.basename(path)
        if not args.arch:
            result = subprocess.run(["file", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')  # 解码为字符串
            if "x86-64" in output:
                arch = "x86_64"
            elif "aarch64" in output:
                arch = "aarch64"
        # 创建相关目录
        create_directories(appname)
        # 修改依赖文件内容,设置权限并拷贝到相应目录
        copy_files(appname, path)
        # 打包为 AppImage
        build_appimage(appname, arch, path)
        # 移动生成的 AppImage 文件
        print(f"打包成功，AppImage 文件位于 ./appimages/{appname}.AppImage")
    elif args.list:
        build_appimages(args.list)


if __name__ == "__main__":
    banner = """
     ______      _ ______      _ _____ __         ______            __    
  / ____/_  __(_) ____/_  __(_) ___// /_  ____ /_  __/___  ____  / /____
 / /   / / / / / /   / / / / /\__ \/ __ \/ __ `// / / __ \/ __ \/ / ___/
/ /___/ /_/ / / /___/ /_/ / /___/ / / / / /_/ // / / /_/ / /_/ / (__  ) 
\____/\__,_/_/\____/\__,_/_//____/_/ /_/\__,_//_/  \____/\____/_/____/  
                                                                        
                                                        version: 0.1
                                                        author: cuicuisha
    ex:./appimage-tool --path ./frp 
    ex:./appimage-tool --list ./list.txt 
    ex:./appimage-tool --path ./cuicuisha --arch x86_64

    """
    print(banner)
    main()

