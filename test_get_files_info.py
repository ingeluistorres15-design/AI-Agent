from functions.get_files_info import get_files_info


def show(title, directory):
    result = get_files_info("calculator", directory)
    print(title)
    if result.startswith("Error"):
        print("    " + result)
    else:
        for line in result.splitlines():
            print("  " + line)


show("Result for current directory:", ".")
show("Result for 'pkg' directory:", "pkg")
show("Result for '/bin' directory:", "/bin")
show("Result for '../' directory:", "../")
