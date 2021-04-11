import re 
import os


base_dir='I:\\Current working projects\\VCS\\[Whitebox]_DTTS\\source'
source_dir = base_dir + "\\QLDauTu" #Source Path
output_path_file = base_dir + "\\..\\SQLi\\SQLi_QLDauTu"
report_path_file = base_dir + "\\..\\SQLi\\report\\SQLi_QLDauTu"


list_parameterizing_funcs = ['setParameter', 'setLong', 'setString', 'setProperties', 'setParameterList']
black_list_funcs = list_parameterizing_funcs

# function_name: e.g. "public function hihi(String) {"
def get_function_content(file_content, function_name):
    balance_ngoac_nhon = 1 # if meet '{': +1, if meet '}': -1. Value equals 0 when reaching the last '}' of a function
    start = file_content.find(function_name) + len(function_name)
    pos = start
    while True:
        pos += 1
        if file_content[pos] == '{':
            balance_ngoac_nhon += 1
        elif file_content[pos] == '}':
            balance_ngoac_nhon -= 1
        if balance_ngoac_nhon == 0:
            break

    return file_content[start:pos]

# Check if there are string concatenations in 2 formats:
    #  1: "string" + variable
    #  2: variable + "string"
def find_concats(func_content):
    ret = []
    concat_formats = [
                        r'\b[a-zA-Z_0-9\.\(\)]+\b\s{0,}\+\s{0,}"[^"]*"',
                        r'"[^"]*"\s{0,}\+\s{0,}\b[a-zA-Z_0-9\.\(\)]+\b'
                        ]
    for regx in concat_formats:
        tmp = re.findall(regx, func_content, re.IGNORECASE)
        if len(tmp) > 0:
            ret += tmp
    return ret


def escape_regx(text):
    for ch in '()[]{}-.?+':
        if ch in text:
            text = text.replace(ch,"\\"+ch)
    return text

'''
    Return
        -1: not vulnerable, or doesn't contain SQL query statement
        0: maybe vulnerable
        1: vulnerable
'''
def check_sqli(func_name, func_content):
    report = ""

    # check if there is SQL query:
    if re.search(r'"\s{0,}(?:Update|select|Insert|Delete)', func_content, re.IGNORECASE) == None:
        return -1, report

    # Check if there is string concatenation. Then check if it's vulnerable
    is_vuln_concat = False
    concats = find_concats(func_content)
    if len(concats) > 0:
        report += '\n-----------------------------------'
        report += '\nFound string concatenations in: ' +  func_name
        for concat in concats:
            regx = r'((?:\.' + r'\(|\.'.join(list_parameterizing_funcs) + r'\().*)' + escape_regx(concat) # concatenation that is in parameterizing functions
            # print(regx)
            tmp = re.search(regx, func_content, re.IGNORECASE)
            if tmp == None:
                is_vuln_concat = True
                report += '\n[Vulnerable]'
                report += '\nConcat string: {}'.format(concat)
                break
            else:
                report += '\n[Not vulnerable]'
                report += '\nConcat in set param mechanism: {}'.format(tmp[0])


    if is_vuln_concat:
        # check if function doesn't contains black listed functions
        for bl in black_list_funcs:
            if ('.' + bl + '(') in func_content:
                report += '\n[Function is MAYBE vulnerable]'
                return 0, report

        report += '\n[Function is VULNERABLE]'
        report += func_content
        return 1, report

    else:
        return -1, report

def write_file(filepath,content):
    with open(filepath, 'w', encoding="utf8", errors='ignore') as f:
        f.write(content)

def check_vulnerable(dirss):
    result = ''
    report = ''
    for root, dirs, files in os.walk(dirss):
        for file in files:
            is_file_name_printed = False
            if file.endswith('DAO.java'): # process file with specific name
                file_content = open(root + "\\" + file, 'r', encoding="utf8", errors='ignore').read()

                # find all public function that take String, DTO, or BO as arguments
                funcs = re.findall(r"public.*\([\w\s\d<>]{0,}(?:String|BO|DTO)[\w\d\s<>]{0,}\)\s{0,}{", file_content, re.IGNORECASE)

                for func in funcs:                    
                    func_content = get_function_content(file_content, func) # Get content of the function
                    is_vuln, tmp = check_sqli(func, func_content)
                    report += tmp
                    if is_vuln >= 0:
                        if not is_file_name_printed:
                            result += '\n====================================\n'
                            result += root + '\\' + file
                            result += '\n====================================\n'
                            is_file_name_printed = True

                        if is_vuln == 0:
                            result += '\n[Maybe Vulnerable]'
                        result += '\n\t{}'.format(func)
                        result += '\n\t\t{}'.format(func_content)
                        result += '\n\t}'
                        result += '\n--------------------------------------\n'
    return result, report

def main():
    result, report = check_vulnerable(source_dir)
    # print(result)
    write_file(output_path_file, result)
    write_file(report_path_file, report)

if __name__ == '__main__':
    main()