from functions.get_files_info import get_files_info

def run_test(dirname):
    results = get_files_info("calculator", dirname)
    if dirname == ".":
        dirname = "current"
    print(f"Result for {dirname} directory:")
    print(results)


run_test(".")
run_test("pkg")
run_test("/bin")
run_test("../")
